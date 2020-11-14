
from src.general_classes.settings import REPORT_FOLDER, TRAFFIC_PATH
from src.simulation_types.simulation import Simulation
import numpy as np

class SingleSimulation(Simulation):
    def __init__(self, topology_choise, *args, **kwargs) -> None:
        
        # Inicia o classe super 
        super().__init__(topology_choise)

        with open(f"{REPORT_FOLDER}{self.csv_file_name}", 'w') as result_file:
            result_file.writelines("laNet,pbReq,HopsMed,netOccupancy\n")
        
        self.all_laNet_data = []
        for laNet in np.linspace(self.definitions.LaNetMin, self.definitions.LaNetMax, self.definitions.Npontos):
            # Executa a simulação para incrementos da carga selecionada
            laNet_data = self.simulate(laNet)
            self.all_laNet_data.append(laNet_data)