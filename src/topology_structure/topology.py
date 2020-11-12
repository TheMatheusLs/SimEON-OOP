import json
import math
from src.general_classes.settings import MAX_LEN_SECTIONS
from src.topology_structure.link import Link

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
                num_sections = math.ceil(length // MAX_LEN_SECTIONS)

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

        self.All_routes = [None for _ in range(self.num_nodes * self.num_nodes)]
    

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


