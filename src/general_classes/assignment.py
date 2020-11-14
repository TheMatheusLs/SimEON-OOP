from src.general_classes.route import Route
from src.general_classes.settings import *


class Assignment:
    def __init__(self, origin_node: int, destination_node: int, parent, route: Route = None, si: int = -1, sf: int = -1, ns: int = -1, osnrTh: float = 0.0, *args, **kwargs):
        
        self.parent = parent

        self.origin_node = origin_node
        self.destination_node = destination_node
        self.route = route
        self.slot_inic = si
        self.slot_fin = sf
        self.ns = ns
        self.osnrTh = osnrTh

    def getOrN(self) -> None:
        return self.origin_node

    def getDeN(self)-> int:
        return self.destination_node

    def setRoute(self, route: Route) -> None:
        self.route = route

    def getRoute(self) -> Route:
        return self.route

    def setSlot_inic(self, si: int) -> None:
        if si == SLOT_USED: # Se o slot será marcado como usado ele deve está livre
            assert((self.getSlot_inic() == SLOT_FREE) or (self.getSlot_inic() == -1))
        else: # Caso contrario, para marcar o slot como livre ele deve está ocupado anteriormente
            assert((self.getSlot_inic() == SLOT_USED) or (self.getSlot_inic() == -1))
        self.slot_inic = si
    
    def getSlot_inic(self) -> int:
        return self.slot_inic

    def setSlot_fin(self, sf: int) -> None:
        if sf == SLOT_USED: # Se o slot será marcado como usado ele deve está livre
            assert((self.getSlot_fin() == SLOT_FREE) or (self.getSlot_fin() == -1))
        else: # Caso contrario, para marcar o slot como livre ele deve está ocupado anteriormente
            assert((self.getSlot_fin() == SLOT_USED) or (self.getSlot_fin() == -1))
        self.slot_fin = sf

    def getSlot_fin(self) -> int:
        return self.slot_fin

    def setNumSlots(self, ns: int) -> None:
        self.numSlots = ns

    def getNumSlots(self) -> int:
        return self.numSlots

    def setOSNRth(self, osnr: float) -> None:
        self.osnrTh = osnr

    def getOSNRth(self) -> float:
        return self.osnrTh
