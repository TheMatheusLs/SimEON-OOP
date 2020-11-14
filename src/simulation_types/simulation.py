from src.general_classes.topology import Topology
from src.general_classes.aux_functions import topology_full_path, gen_filename_report
from src.general_classes.traffic import Traffic
from src.general_classes.definitions import Definitions
from src.general_classes.schedule import Schedule
from src.general_classes.heuristics import Heuristic
from src.general_classes.assignment import Assignment
from src.general_classes.connection import Connection
from src.general_classes.routing import Routing
from src.general_classes.event import Event
from src.general_classes.settings import REPORT_FOLDER, TRAFFIC_PATH, EventType
import src.general_classes.modulation as Modulation
import src.general_classes.general as General
import numpy as np
import math
from datetime import datetime

class Simulation:
    def __init__(self, topology_choise, *args, **kwargs) -> None:
        
        #Armazena o tipo de topologia usada
        self.topology_choise = topology_choise

        # Cria os objetos para cada classe
        self.topology = Topology(topology_full_path(self.topology_choise), self)
        self.traffic = Traffic(TRAFFIC_PATH, self)
        self.definitions = Definitions(manual_input = False, parent = self)
        self.schedule = Schedule(self)
        self.heuristics = Heuristic(self)

        self.topology.init_control_route_RCL()

        # Inicializa todas as classes
        self.topology.initialise()
        self.definitions.initialise()
        self.schedule.initialise()

        # Encontra as todas as rotas usando o algoritmo escolhido
        self.routing = Routing(self)   

        # Cria a lista de conflito entre as rotas
        self.topology.create_conflict_routes()

        # Escreve todas as rotas na tela
        self.topology.print_all_routes()

        print("Start Of Simulation: \n")

        date_form = datetime.now().strftime('%d-%m-%Y_%H-%M')
        self.csv_file_name = f"{date_form}_{gen_filename_report(self.topology_choise, self.definitions.routing_algorithm, self.definitions.Spectrum_algorithm)}.csv"
    

    def simulate(self, laNet) -> tuple:
        """Executa uma simulação para uma carga da rede.

        Args:
            laNet (float): Carga da rede em Erlang

        Returns:
            tuple: Dados da simulação
        """
        print(f"\nSimulation for laNet = {laNet}")

        # Inicializa todas as classes
        self.topology.initialise()
        self.definitions.initialise()
        self.schedule.initialise()

        # Cria o evento para ser a primeira requisição
        event = Event(self)

        # Atribui o tempo para a simulação
        event.setRequestEvent(self.schedule.getSimTime())

        # Programa o evento dentro do cronograma
        self.schedule.scheduleEvent(event)

        print(f"Simulating...")

        # Executa as requisições de 0 até o valor máximo selecionado
        while (self.definitions.get_num_req() < self.definitions.get_num_req_max()):

            curEvent = self.schedule.getCurrentEvent()

            if (curEvent.getType() == EventType.Req): # Chegou uma requisição

                self.ConnectionRequest(curEvent)

                IAT = General.exponential(laNet) #Inter-arrival time

                curEvent.setRequestEvent(self.schedule.getSimTime() + IAT) #Reuse the same Event Object

                assert(event.getType() == EventType.Req)
                assert(event.getConnection() == None)
                self.schedule.scheduleEvent(curEvent)
            else:
                if curEvent.getType() == EventType.Desc: #Desconnection Request
                    self.ConnectionRelease(curEvent)
                    del curEvent
                else:
                    if (curEvent.getType() == EventType.Exp):
                        #assert(ExpComp) #Um evento deste tipo so pode ocorrer se ExpComp=true;
                        self.heuristics.ExpandConnection(curEvent.getConnection())
                        #DefineNextEventOfCon(curEvent)
                        self.schedule.scheduleEvent(curEvent)
                    else:
                        if (curEvent.getType() == EventType.Comp):
                            #assert(ExpComp) #Um evento deste tipo so pode ocorrer se ExpComp=true;
                            self.heuristics.CompressConnection(curEvent.getConnection())
                            #DefineNextEventOfCon(curEvent)
                            self.schedule.scheduleEvent(curEvent)

        self.FinaliseAll(laNet)

        return ()
    
    
    def ConnectionRequest(self, event: Event) -> None:
        """Estabelece uma requisão para o evento

        Args:
            event (Event): Evento
        """
        self.definitions.numReq += 1

        origin_node, destination_node = self.traffic.sourceDestinationTrafficRequest()

        assert(self.topology.valid_node(origin_node) and self.topology.valid_node(destination_node))

        bps = self.traffic.bitRateTrafficRequest()

        ber = self.traffic.getBER()

        polarization = self.traffic.getPolarization()

        assignment = Assignment(origin_node, destination_node, self)

        M = 4

        DO = True
        while ((M>1) or (DO)):
            DO = False
            assignment.setNumSlots(math.ceil(Modulation.bandwidthQAM(M, bps, polarization) / self.definitions.slotBW))
            assignment.setOSNRth(Modulation.getSNRbQAM(M, ber))

            #Roteamento:
            self.heuristics.Routing(assignment)

            if ( (assignment.getRoute() != None) and ( self.topology.valid_node(assignment.getOrN())) and (self.topology.valid_node(assignment.getDeN()))):

                # Escolhe a alocação do espectro de acordo com o algorimo selecionado
                self.heuristics.spectrum_allocation(assignment)

                if ( (assignment.getSlot_inic() != -1) and (assignment.getSlot_fin() != -1)):
                    # Request was accepted
                    
                    newConnection = Connection(assignment.getRoute(), assignment.getSlot_inic(), assignment.getSlot_fin(), self.schedule.getSimTime() + General.exponential(self.definitions.mu))

                    self.topology.connect(newConnection)

                    evtNewCon = Event(self)
                    evtNewCon.setReleaseEvent(evtNewCon, newConnection)

                    self.schedule.scheduleEvent(evtNewCon)

                    break

            M -= 1   

        if M == 1:
            self.definitions.numReq_Bloq += 1    
        
        del assignment
    

    def ConnectionRelease(self, evt: Event) -> None:
        """Libera as conexões

        Args:
            evt (Event): Evento
        """
        connection = evt.getConnection()
        self.topology.releaseConnection(connection)
        del connection


    def FinaliseAll(self, laNet) -> None:
        print(f"Simulation Time = {self.schedule.getSimTime()}")
        print(f"numReq = {self.definitions.numReq}")

        print(f"nu0 = {laNet}")
        pbReq = self.definitions.numReq_Bloq / self.definitions.numReq
        print(f"PbReq = {pbReq}")
        #PbSlots = self.definitions.numSlots_Bloq / self.definitions.numSlots_Req
        #print(f"PbSlots = {PbSlots}")
        HopsMed = self.definitions.numHopsPerRoute / (self.definitions.numReq - self.definitions.numReq_Bloq)
        print(f"HopsMed = {HopsMed}")
        print(f"netOcc = {self.definitions.netOccupancy}")
        print()

        with open(f"{REPORT_FOLDER}{self.csv_file_name}", 'a') as result_file:
            result_file.writelines(f"{laNet},{pbReq},{HopsMed},{self.definitions.netOccupancy}\n")

        evtPtr = self.schedule.getCurrentEvent()

        # Libera todas as conexões
        while (evtPtr != None):
            con = evtPtr.getConnection()
            if con != None: # This is a Connection
                self.topology.releaseConnection(con)
                del con
            del evtPtr
            evtPtr = self.schedule.getCurrentEvent()

        assert(not self.topology.areThereOccupiedSlots())
        assert(self.schedule.isEmpty())