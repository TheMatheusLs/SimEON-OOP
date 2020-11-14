

class Connection:
    def __init__(self, route = 0, si: int = -1, sf: int = -1, td: float = float('inf'), parent = None, *args, **kwargs):
        
        self.parent = parent

        self.route = route
        self.si = si
        self.sf = sf
        self.tDesc = td

    def getFirstSlot(self) -> int:
	    return self.si

    def getLastSlot(self) -> int:
	    return self.sf
    
    def incFirstSlot(self, x: int) -> None:
	    assert((self.si + x >= 0) and (self.si + x < self.parent.topology.get_num_slots()))

    def incLastSlot(self, x: int) -> None:
	    assert((self.sf + x >= 0) and (self.sf + x < self.parent.topology.get_num_slots()))

    def expandLeft(self) -> None:
        assert(self.getFirstSlot() > 0)
        self.parent.topology.occupySlot(self, self.getFirstSlot() - 1)
        self.incFirstSlot(-1)

    def expandRight(self) -> None:
        assert(self.getLastSlot() < self.parent.topology.get_num_slots() - 1)
        self.parent.topology.occupySlot(self, self.getLastSlot() + 1)
        self.incLastSlot(+1)
    
    def compressLeft(self) -> None:
        self.parent.topology.releaseSlot(self, self.getFirstSlot())
        self.incFirstSlot(+1)
    
    def compressRight(self) -> None:
        self.parent.topology.releaseSlot(self, self.getLastSlot())
        self.incLastSlot(-1)
    
    def getRoute(self):
	    return self.route

    def setTimeDesc(self, time):
        assert(time > self.parent.schedule.getSimTime())
        self.tDesc = time

    def getTimeDesc(self):
	    return self.tDesc