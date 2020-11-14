import json
import math
import numpy as np
from src.general_classes.settings import MAX_LEN_SECTIONS, SLOT_USED, SLOT_FREE, rcl_func
from src.general_classes.link import Link
from src.general_classes.route import Route
from src.general_classes.signal import Signal

class Topology:
    def __init__(self, topology_path, parent, *args, **kwargs) -> None:

        self.parent = parent
        self.topology_path = topology_path

        # Carrega as configurações do arquivo de topologia
        self.load_topology(self.topology_path)

    
    def load_topology(self, topology_path) -> None:

        # Ler todas as informações da topologia e armazena
        try:
            with open(topology_path) as topology_file:
                topology_info = json.load(topology_file)

            #Adquire o número de slots
            self.num_slots = topology_info["NumberOfSlots"]

            # Adquire o número de nós
            self.set_num_nodes(topology_info["NumberOfNodes"])
            
            # Vetor para armazenar a ocupação global dos slots
            self.global_slot_ocupation = [0 for _ in range(self.num_slots)]

            
            aux_num_link = 0
            for info_link in topology_info["Links"]:
                origin_node = info_link["OriginNode"]
                destination_node = info_link["DestinationNode"]
                length = info_link["LinkLength"]
                num_sections = math.ceil(length / MAX_LEN_SECTIONS)

                link = Link(origin_node, destination_node, length, num_sections, self)

                if self.is_valid_link(link):
                    self.insert_link(link)
                    aux_num_link += 1
            
            # Adquire o número de enlaces
            self.num_links = aux_num_link

            print(f"Number Of Nodes: {self.num_nodes}")
            print(f"Number Of Links: {self.num_links}")
            print(f"Number Of Slots: {self.num_slots}")
                    
        except Exception as e:
            print(f"Could not load topology. {e}")


    def set_num_nodes(self, num_nodes: int) -> None:
        """Configura o número de nós, carrega a topologia e os nós em funcionamento

        Args:
            num_nodes (int): Número de nós na rede
        """
        self.num_nodes =  num_nodes

        #Cria um a estrutura para armazenar os links 
        self.link_topology = [None for _ in range(self.num_nodes * self.num_nodes)]

        # Cria a estrutura para armazenar o estado de funcionamento dos nós
        self.node_isworking =  [True for i_node in range(self.num_nodes)]

        self.all_routes = [None for _ in range(self.num_nodes * self.num_nodes)]
    

    def get_num_slots(self) -> int:
        """Retorna o número de slots

        Returns:
            int: Número de slots
        """
        return self.num_slots

    
    def get_num_nodes(self) -> int:
        """Retorna o número de nós

        Returns:
            int: Número de nós
        """
        return self.num_nodes


    def get_num_links(self) -> int:
        """Retorna o número de links

        Returns:
            int: Número de links
        """
        return self.num_links

    
    def is_valid_link(self, link: Link) -> bool:
        """Verifica se um link é válido

        Args:
            link (Link): Link a ser verificado

        Returns:
            bool: Verdadeiro se o link for válido
        """
        return ( self.is_valid_node(link.get_origin_node()) and self.is_valid_node(link.get_destination_node()) )

    
    def is_valid_node(self, node: int) -> bool:
        """Verifica se um nó é válido

        Args:
            node (int): Nó a ser verificado

        Returns:
            bool: Verdadeiro se o nó for válido
        """
        return (node >= 0 and node < self.get_num_nodes())


    def insert_link(self, link: Link) -> None:
        """Insere um link na topologia

        Args:
            link (Link): Link para ser inserido
        """
        if self.is_valid_link(link):
            self.link_topology[link.get_origin_node() * self.num_nodes + link.get_destination_node()] = link


    def init_control_route_RCL(self) -> None:

        self.control_route_RCL = []
        self.control_route_RCL_storage = []

        for route in self.all_routes:
            if route != None:
                self.control_route_RCL.append(route.count_slot_unable)
                self.control_route_RCL_storage.append([ rcl_func(self.num_slots) for _ in route.count_slot_unable.copy()])
            else:
                self.control_route_RCL.append(None)
                self.control_route_RCL_storage.append([ 0 for _ in range(self.num_slots)])


    def initialise(self) -> None:
        """ Inicializa a topologia da rede
        """
        for o_node in range(self.num_nodes):
            for d_node in range(self.num_nodes):    
                if self.link_topology[o_node * self.num_nodes + d_node] != None:
                    self.link_topology[o_node * self.num_nodes + d_node].initialise()

    def print_all_routes(self) -> None:
        """Escreve todas as rotas no console
        """
        for o_node in range(self.num_nodes):
            for d_node in range(self.num_nodes):
                if o_node != d_node:
                    print(f"\n[origin Node = {o_node}  destination Node = {d_node}]")
                    for p in range(len(self.getRoutes(o_node, d_node).Path)):
                        print(f"Route({p}): ", end=' ')
                        route = self.getRoutes(o_node, d_node).Path
                        self.printRoute(route)
                        break ## Forcando a sair do loop para ficar igual a simulação do codeblocks


    def printRoute(self, route: Route) -> None:
        """Escreve uma rota no console

        Args:
            route (Route): Rota a ser mostrada no console
        """
        hops = len(route) - 1
        print(f"hops = {hops}: ", end='')
        for h in range(hops + 1):
            print(route[h], end=" - " if h != hops else '')
        print()


    def setNumNodes(self, num_nodes: int) -> None:
        """Configura o número de nós, carrega a topologia e os nós em funcionamento

        Args:
            num_nodes (int): Número de nós na rede
        """
        self.num_nodes =  num_nodes

        self.link_topology = [None for _ in range(self.num_nodes * self.num_nodes)]

        self.node_isworking =  []

        for i_node in range(self.num_nodes):
            self.node_isworking.append(True)

            for j_node in range(self.num_nodes):
                self.link_topology[i_node * self.num_nodes + j_node] = None #Link(parent = self)

        self.all_routes = [None for _ in range(self.num_nodes * self.num_nodes)]


    def clearRoutes(self, origin_node: int, destination_node: int) -> None:
        """Limpa as rotas entre o nó de origem e destinos

        Args:
            origin_node (int): Nó de origem
            destination_node (int): Nó de destino
        """
        self.all_routes[origin_node * self.num_nodes + destination_node] = None


    def getRoutes(self, origin_node: int, destination_node: int) -> Route:
        """Retorna as rotas entre a origem e o destino

        Args:
            origin_node (int): Nó de origem
            destination_node (int): Nó de destino

        Returns:
            Route: Rotas
        """
        return self.all_routes[origin_node * self.num_nodes + destination_node]


    def set_route(self, origin_node: int, destination_node: int, route: Route) -> None:
        """Adiciona a rota entre a origem e o destino

        Args:
            origin_node (int): Nó de origem
            destination_node (int): Nó de destino
            route (Route): Rota a ser adicionadas       
        """
        self.clearRoutes(origin_node, destination_node)
        self.addRoute(origin_node, destination_node, route)


    def addRoute(self, origin_node: int, destination_node: int, route: Route) -> None:
        """Adiciona uma rota 

        Args:
            origin_node (int): Nó de origem
            destination_node (int): Nó de destino
            route (Route): Rota
        """
        self.all_routes[origin_node * self.num_nodes + destination_node] = route


    def getLink(self, origin_node: int, destination_node: int) -> Link:
        """Recupera o link entre dois nós

        Args:
            origin_node (int): Nó de origem
            destination_node (int): Nó de destino

        Returns:
            Link: Link retornado
        """
        if not (self.valid_node(origin_node) and self.valid_node(destination_node)):
            print(f"Error in Topology::getLink() {origin_node} {destination_node}")
        return self.link_topology[origin_node * self.num_nodes + destination_node]


    def isNodeWorking(self, node: int) -> bool:
        """Verifica se o nó está em funcionamento

        Args:
            node (int): Nó para ser verificado

        Returns:
            bool: Verdadeiro caso o nó esteja em funcionamento
        """
        return self.node_isworking[node]


    def valid_node(self, node: int) -> bool:
        """Verifica se um nó é válido

        Args:
            node (int): Nó a ser verificado

        Returns:
            bool: Verdadeiro se o nó for válido
        """
        return (node >= 0 and node < self.get_num_nodes())


    def valid_link(self, link: Link) -> bool:
        """Verifica se um link é válido

        Args:
            link (Link): Link a ser verificado

        Returns:
            bool: Verdadeiro se o link for válido
        """
        return ( self.valid_node(link.get_origin_node()) and self.valid_node(link.get_destination_node()) )


    def checkSlotDisp(self, route: Route, slot: int) -> bool:

        for c in range(route.getNumHops()):
            L_or = route.getNode(c)
            L_de = route.getNode(c+1)
            link = self.getLink(L_or, L_de)

            if self.valid_link(link):
                pass

            if link.isSlotOccupied(slot):
                return False
        return True


    def checkSlotNumberDisp(self, route: Route, numSlots: int):
        numContiguousSlots = 0

        for slot in range(self.get_num_slots() - numSlots): # Só está olhando o número de slot da requisição. Modificando para olhar em todos os slots da rota
            if self.checkSlotDisp(route, slot):
                numContiguousSlots += 1
            else:
                numContiguousSlots = 0
            
            if numContiguousSlots == numSlots:
                return True
        return False
    

    def checkOSNR(self, route, OSNRth):

        signal = Signal(self)
        signal.initialise()

        for c in range(route.getNumHops()):
            L_or = route.getNode(c)
            L_de = route.getNode(c+1)
            link = self.getLink(L_or,L_de)
            link.calcSignal(signal)
        
        if(signal.getOSNR() > OSNRth):
            return True
        return False


    def connect(self, connection) -> None:
        #Insert connection into the network
        route = connection.getRoute()

        for c in range(route.getNumHops()):
            if self.valid_node(route.getNode(c)):
                L_or = route.getNode(c)
                L_de = route.getNode(c+1)
                link = self.getLink(L_or, L_de)
                assert(self.valid_link(link))

                for slot in range(connection.getFirstSlot(), connection.getLastSlot() + 1):
                    link.occupySlot(slot) # Aqui o slot é ocupado

                    route.increment_occupied_slot(slot)

                    # Incrementa o uso do slot na possição global
                    self.global_slot_ocupation[slot] += 1

        origin_node = route.getOrN()
        destination_node = route.getDeN()

        empty_slot_current_route = (np.array(route.count_slot_unable) == 0)

        slots_empty_sum = sum(empty_slot_current_route)

        self.control_route_RCL_storage[origin_node * self.num_nodes + destination_node] = [ rcl_func(slots_empty_sum) if is_empty else 0 for is_empty in empty_slot_current_route]

        self.parent.definitions.numHopsPerRoute += route.getNumHops()
        self.parent.definitions.netOccupancy += ((connection.getLastSlot() - connection.getFirstSlot() + 1) * route.getNumHops())
    

    def releaseConnection(self, connection) -> None: #Connection* conn0x622ef00x622ef0ection
        route = connection.getRoute()
        #release all slots used for the Connection

        for c in range(route.getNumHops()):
            L_or = route.getNode(c)
            L_de = route.getNode(c+1)
            link = self.getLink(L_or, L_de)
            assert(self.valid_link(link)) #Acrescentei

            for slot in range(connection.getFirstSlot(), connection.getLastSlot() + 1):
                link.releaseSlot(slot)

                route.decreases_occupied_slot(slot)

                # Decrementa o uso do slot na possição global
                self.global_slot_ocupation[slot] -= 1
        
        origin_node = route.getOrN()
        destination_node = route.getDeN()

        empty_slot_current_route = (np.array(route.count_slot_unable) == 0)

        slots_empty_sum = sum(empty_slot_current_route)

        self.control_route_RCL_storage[origin_node * self.num_nodes + destination_node] = [ rcl_func(slots_empty_sum) if is_empty else 0 for is_empty in empty_slot_current_route]


    def releaseSlot(self, connection, slot: int) -> None: #Release slot s in all links of connection
        route = connection.getRoute()
        #release all slots used for the Connection

        for c in range(route.getNumHops()):
            L_or = route.getNode(c)
            L_de = route.getNode(c+1)
            link = self.getLink(L_or, L_de)
            link.releaseSlot(slot)


    def occupySlot(self, connection, slot: int) -> None: # occupy slot s in all links of connection
        #Insert connection into the network
        route = connection.getRoute()

        for c in range(route.getNumHops()):
            L_or = route.getNode(c)
            L_de = route.getNode(c + 1)
            link = self.getLink(L_or, L_de)
            link.occupySlot(slot)
        
        
    def areThereOccupiedSlots(self) -> bool:
        #if (self.valid_link(link)):
        for origin_node in range(self.num_nodes):
            for destination_node in range(self.num_nodes):
                link = self.link_topology[origin_node * self.num_nodes + destination_node]

                if link != None: #There is a link between nodes oN and dN
                    for slot in range(self.get_num_slots()):
                        if link.isSlotOccupied(slot):
                            return True
        return False


    def get_links(self, route: Route) -> list:
        """Retorna os links que constroem a rota informada

        Args:
            route (Route): Rota

        Returns:
            list: Links que formam a rota 
        """
        links = []

        for node in range(route.getNumHops()):
            link_origin = route.getNode(node)
            link_destination = route.getNode(node + 1)
            link = self.getLink(link_origin, link_destination)
            if self.valid_link(link):
                links.append(link)

        return links

    
    def get_slots_avalable(self, links: Link) -> list:

        slots = []

        for index_slot in range(self.get_num_slots()):
            slots.append(None)
            for link in links:
                if not link.isSlotFree(index_slot):
                    slots[index_slot] = SLOT_USED
                    break
            if slots[index_slot] == None:
                slots[index_slot] = SLOT_FREE                    

        return slots
    
    def get_all_routes(self) -> list:
        """Retorna a lista com todas as rotas armazenadas na topologia

        Returns:
            list: Lista das rotas
        """
        return self.all_routes

    def create_conflict_routes(self) -> None:

        for route in self.get_all_routes():
            if route != None:
                route.set_conflict_routes()