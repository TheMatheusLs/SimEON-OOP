from src.general_classes.settings import Routing_Type, Spectrum_Type
from src.general_classes.interface_functions import print_class_enum

class Definitions:
    def __init__(self, manual_input: bool = True, parent = None, *args, **kwargs) -> None:

        self.parent = parent

        self.routing_algorithm = print_class_enum(Routing_Type)
        
        self.Spectrum_algorithm = print_class_enum(Spectrum_Type)

        print(f"*Traffic Parameters:")

        if manual_input:
            self.mu = int(input("Insert Connection Deactivation Rate: (Default: 1): "))
            self.LaNetMin = int(input("LaNet Min = "))
            self.LaNetMax = int(input("LaNet Max = "))
            self.Npontos = int(input("#Points in the Graph = "))
            self.numReq = int(input("Insert Number of Requests: (Recommended: > 1000000): "))
        else:
            self.mu = 1
            self.LaNetMin = 200
            self.LaNetMax = 300
            self.Npontos = 5
            self.numReq = 100_000 

        self.LaPasso = (self.LaNetMax - self.LaNetMin) // (self.Npontos - 1)

        self.set_num_req_max(self.numReq)

        self.is_WDM_simulator = True

        if self.is_WDM_simulator:
            # Slot usando o tamanho de taxa máximo para sempre solicitar um único slot.
            self.slotBW = max(self.parent.traffic.Vtraffic)
        else:
            # A linha abaixo é usada para redes elásticas. Slot com capacidade para 12.5Ghz
            self.slotBW = 12_500_000_000

        
    def initialise(self) -> None:
        """Inicializa as váriaveis
        """
        self.numReq = 0.0
        self.numReq_Bloq = 0.0
        self.numSlots_Req = 0.0
        self.numSlots_Bloq = 0.0
        self.numHopsPerRoute = 0.0
        self.netOccupancy = 0.0
    
    
    def get_num_req(self) -> int:
        """Retorna o número de requisições

        Returns:
            int: Número de requisições
        """
        return self.numReq


    def get_num_req_max(self) -> int:
        """Retorna o número máximo de requisições

        Returns:
            int: Número máximo de requisições
        """
        return self.numReqMax


    def set_num_req_max(self, numReqMax: int) -> None:
        """Configura o número máximo de requisições

        Args:
            numReqMax (int): Número máximo 
        """
        self.numReqMax = numReqMax

