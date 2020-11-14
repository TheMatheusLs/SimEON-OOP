import json
import random
from src.general_classes.settings import RAND_MAX, BER, POLARIZATION
import src.general_classes.general as General

class Traffic:
    def __init__(self,  traffic_path, parent, *args, **kwargs) -> None:

        self.parent = parent

        print('Request Traffic Intensities:', end=' ')

        self.Vtraffic = []

        try:
            with open(traffic_path) as traffic_file:
                traffic_info = json.load(traffic_file)

                for rate_bps in traffic_info["Rates"]:
                        
                    self.addTraffic(rate_bps)

                    print(f"{rate_bps:.2e} ", end="")
                print()
        except Exception as e:
            print(e)

        self.BER = BER
        self.polarization = POLARIZATION

    def addTraffic(self, rate_bps: float) -> None:
        """Adiciona o tráfego no vetor

        Args:
            rate_bps (float): Tráfego atual
        """
        self.Vtraffic.append(rate_bps)
    

    def sourceDestinationTrafficRequest(self) -> tuple:

        origin_node = random.randint(0, RAND_MAX) % self.parent.topology.get_num_nodes()
        destination_node = random.randint(0, RAND_MAX) % (self.parent.topology.get_num_nodes() - 1)

        if destination_node >= origin_node:
            destination_node += 1

        if ((origin_node < 0) or (origin_node >= self.parent.topology.get_num_nodes()) or (destination_node < 0) or (destination_node >= self.parent.topology.get_num_nodes()) or (destination_node == origin_node)):
            print("Erro in SDPair")
            input()

        return origin_node, destination_node


    def bitRateTrafficRequest(self) -> float:
        """Retorna um dos tráfegos dado inicialmente

        Returns:
            float: Tráfego em bps
        """
        aux = General.uniform(0, len(self.Vtraffic))
        return self.Vtraffic[aux] 
    

    def setBER(self, ber: float) -> float:
        """Configura o novo BER

        Args:
            ber (float): Novo BER

        Returns:
            float: [description]
        """
        self.BER = ber


    def getBER(self) -> float:
        """Retorna o BER

        Returns:
            float: BER
        """
        return self.BER
    

    def setPolarization(self, p: int) -> None:
        """Configura a Polarização

        Args:
            p (int): Nova polarização
        """
        self.polarization = p


    def getPolarization(self) -> int:
        """Retorna a Polarização

        Returns:
            int: Polarização 
        """
        return self.polarization