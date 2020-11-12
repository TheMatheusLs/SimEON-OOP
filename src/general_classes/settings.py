from enum import Enum, auto


###  Definições
RANDOM_SEED = 42            # Semente aleatória
MAX_LEN_SECTIONS = 60_000   # Tamanho máximo para cada seção

TOPOLOGY_PATH = lambda file: f".\\topologies\\{file}.json"


###  Classes enumeradas
# Tipos de simulação
class Simulation_Type(Enum):
    Single_simulation = auto()
    All_RWA_algorithms = auto()

# Tipos de topologia
class Topology_Type(Enum):
    Finland_12 = auto()
    Japan_14 = auto()
    NSFNET_14 = auto()
    Ring_5 = auto()

class LinkCostType(Enum):
    minHops = auto()
    minLength = auto()