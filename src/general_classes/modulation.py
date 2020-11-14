
from src.general_classes.settings import ROLLOFF

def bandwidthQAM(M: int, Rbps: float, pol: float) -> float:
    return ((1.0 + ROLLOFF)* Rbps) / (pol * M)

def getSNRbQAM(M: int, ber: float) -> float:
    return 0 #TODO: Arruamar essa função as modulações não estão sendo aplicada corretamente. Sempre irá retornar 0

def getsnrbQAM(M: int, ber: float):
    print("Modulation::Consertar isso aqui")
    return 0.0
