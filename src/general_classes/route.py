
class Route:
    def __init__(self, path: list = [], parent: object = None, *args, **kwargs) -> None:

        self.parent = parent

        self.Path = []

        for p in path:
            self.Path.append(p)

        #Expand

        # Links que constroe essa rota
        self.links = self.parent.parent.topology.get_links(self)

        # Todas as rotas com fazem conflito com essa rota
        self.conflict_routes = []
        # Slots disponíveis para essa rota (Lambda)

        self.count_slot_unable = [0 for _ in range(self.parent.parent.topology.get_num_slots())]
    
    def set_conflict_routes(self) -> None:
        """Verifica a rota compartilham o link com outra, armazena as que compartilham
        """
        for link in self.links:
            for route in self.parent.parent.topology.get_all_routes():
                if ((route != self) and route != None):
                    if link in route.links:
                        self.conflict_routes.append(route)


    def increment_occupied_slot(self, slot: int) -> None:
        """Incrementa o slot que está ocupado por essa rota e em todas as rotas que fazem conflito com essas.

        Args:
            slot (int): Índice do slot
        """
        self.count_slot_unable[slot] += 1

        for route in self.conflict_routes:
            route.count_slot_unable[slot] += 1

    def decreases_occupied_slot(self, slot: int) -> None:
        """Decrementa o slot que está ocupado por essa rota e em todas as rotas que fazem conflito com essas.

        Args:
            slot (int): Índice do slot
        """
        self.count_slot_unable[slot] -= 1

        for route in self.conflict_routes:
            route.count_slot_unable[slot] -= 1

    def get_count_slot_unable(self) -> list:
        return self.count_slot_unable

    def getOrN(self) -> int:
        assert(len(self.Path) > 0)
        return self.Path[0]

    def getDeN(self) -> int:
	    return self.Path[-1]

    def getNumHops(self) -> int:
        return len(self.Path) - 1

    def getNumNodes(self) -> int:
        return len(self.Path)

    def getNode(self, pos:int) -> int:
        assert((pos >= 0) and (pos < len(self.Path)))
        return self.Path[pos]

