from enum import Enum, auto


###  Definições
RANDOM_SEED = 42            # Semente aleatória
MAX_LEN_SECTIONS = 60_000   # Tamanho máximo para cada seção
BER = 0.001         
POLARIZATION = 2
SLOT_FREE = 0
SLOT_USED = 1
RAND_MAX = 32767
ROLLOFF = 0.0

TOPOLOGY_PATH = lambda file: f".\\topologies\\{file}.json"
TRAFFIC_PATH = ".\\traffics\\traffic_1.json"
REPORT_FOLDER = ".\\report\\"

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

class Routing_Type(Enum):
    Dijkstra = auto()

class Spectrum_Type(Enum):
    FirstFit = auto()

class TiebreakerAlgorithm(Enum):
    FirstFit = auto()
    Random = auto()

class EventType(Enum):
    UNKNOWN = auto()
    Req = auto()
    Desc = auto()
    Exp = auto()
    Comp = auto()


rcl_func = lambda x: 1.0 / x if x != 0 else float("inf")