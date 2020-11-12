from src.topology_structure.topology import Topology
from src.general_classes.aux_functions import topology_full_path
from src.general_classes.settings import *

class SingleSimulation:
    def __init__(self, topology_choise, *args, **kwargs) -> None:
        
        #Armazena o tipo de topologia usada
        self.topology_choise = topology_choise

        # Cria os objetos para cada classe
        self.topology = Topology(topology_full_path(self.topology_choise), self)