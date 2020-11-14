import random
import math
from src.general_classes.settings import RAND_MAX


def uniform(x_min: int, x_max: int) -> int:

    va = random.randint(0, RAND_MAX) / RAND_MAX
    va += va / RAND_MAX
    va += va / RAND_MAX

    while ((va <= 0) or (va >= 1.0 - (RAND_MAX ** (-3)))):
        va = random.randint(0, RAND_MAX) / RAND_MAX
        va += va / RAND_MAX
        va += va / RAND_MAX
    
    if ((type(x_min) == type(1)) and (type(x_max) == type(1))):
        return math.floor(x_min + va * (x_max - x_min))
    else:
        return (x_min + va * (x_max - x_min))

def dBtoLinear(x: float) -> float:
    return 10 ** (x/10)

def linearWTodBm(powerWatts: float) -> float:
    return 10 * math.log(powerWatts * 1000, 10)

def linearTodB(x: float) -> float:
    return 10 * math.log(x,10)

def exponential(L: float) -> float:
	return float ( - math.log( 1 -  uniform(0.0, 1.0)) / L ) 