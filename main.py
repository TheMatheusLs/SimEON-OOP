import logging
import time
from src.general_classes.settings import RANDOM_SEED, Simulation_Type, Topology_Type
from src.general_classes.interface_functions import print_class_enum
from src.simulation_types.single_simulation import SingleSimulation

LOG_FORMAT = "%(asctime)s | %(levelname)s - %(message)s" 
logging.basicConfig(filename = "simulation.log", level = logging.DEBUG, format = LOG_FORMAT, filemode = 'w')
logger = logging.getLogger()

logger.info(f"Simulando com a seed = {RANDOM_SEED}")

class Main:
    def __init__(self, *args, **kwargs) -> None:

        # Escolhe o tipo de simulação
        self.simulation_choise = print_class_enum(Simulation_Type)

        self.topology_choise = print_class_enum(Topology_Type)

        ## Seleção do tipo de simulação
        if self.simulation_choise == Simulation_Type.Single_simulation.value:
            logger.info("Running the single simulation")
            print("Running the single simulation\n")

            SingleSimulation(self.topology_choise)
    

        if self.simulation_choise == Simulation_Type.All_RWA_algorithms.value:
            logger.info("Running the all RWA algorithms simulation")
            print("Running the all RWA algorithms simulation\n")


if __name__ == "__main__":
    # Salva o tempo inicial
    init_time = time.time()
    
    # Executa o algoritimo principal
    Main()

    #Salva o tempo final
    end_time = time.time()

    # Finaliza o código
    print(f"Finish Simulation! With {end_time - init_time:.2f} seconds")
    logger.info(f"Finish Simulation! With {end_time - init_time:.2f} seconds")