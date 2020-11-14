
import random
from src.general_classes.settings import *
from src.general_classes.assignment import Assignment
from src.general_classes.RWA_algortitms.FirstFit_algorithm import FirstFit
import numpy as np


class Heuristic:
    def __init__(self, parent, *args, **kwargs) -> None:

        self.parent = parent

    def Routing(self, assignment):
        #routeSet = self.parent.routing.Dijkstra(assignment.getOrN(), assignment.getDeN())

        #self.parent.topology.set_route(assignment.getOrN(), assignment.getDeN(), routeSet) #Modificação do arquivo c++
        routeSet = self.parent.topology.getRoutes(assignment.getOrN(), assignment.getDeN()) #Modificação do arquivo c++

        #Routing.Yen(assignment.getOrN(), assignment.getDeN(), parent.routing.KYEN)

        # Comentando porque só há uma rota
        #for route in routeSet.Path:
        netLayer = self.parent.topology.checkSlotNumberDisp(routeSet, assignment.getNumSlots()) #TODO: ERRO AQUI
        phyLayer = self.parent.topology.checkOSNR(routeSet, assignment.getOSNRth())

        if(netLayer and phyLayer):
            assignment.setRoute(routeSet)

    ## ************* Heuristicas para roteamento RWA ***************** ##
    def spectrum_allocation(self, assignment: Assignment) -> None:

        if self.parent.definitions.is_WDM_simulator: # Verifica se é feita uma simulação em WDM
            assert(assignment.getNumSlots() == 1)

        if Spectrum_Type.FirstFit.value == self.parent.definitions.Spectrum_algorithm:
            starting_slot, final_slot  = FirstFit(assignment)

        # Valia se os slots são validos e insere
        if (starting_slot != -1) and (final_slot != -1):
            assignment.setSlot_inic(starting_slot)
            assignment.setSlot_fin(final_slot)

    def ExpandConnection(self, con) -> None:
        #Expand an edge slot according to the following policy:
        self.ExpandRandomly(con) # Remove o slot da direita ou da esquerda com igual probabilidade.


    def ExpandRandomly(self, con) -> None: # Remove aleatoriamente o slot da direita ou da esquerda.
        if(random.randint(0, RAND_MAX) % 2 == 0):
            con.expandLeft() # Expand to the left
        else:
            con.expandRight() # Expand to the rigth


    def CompressConnection(self, con) -> None:
        """Compress an edge slot according to the following policy:

        Args:
            con (Connection): Conexão
        """
        self.CompressRandomly(con) #Remove o slot da direita ou da esquerda com igual probabilidade.


    def CompressRandomly(self, con) -> None:
        """Remove aleatoriamente o slot da direita ou da esquerda.

        Args:
            con (Connection): Conexão
        """
        if(random.randint(0, RAND_MAX) % 2 == 0): # Compress to the left
            con.compressLeft()
        else:
            con.compressRight() # Compress to the rigth;