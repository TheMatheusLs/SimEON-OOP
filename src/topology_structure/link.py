from src.general_classes.settings import LinkCostType


class Link:
    def __init__(self, origin_node: int = -1, destination_node: int = -1, length: float = 0, num_sections: int = 0, parent = None, *args, **kwargs) -> None:

        self.parent = parent

        self.origin_node = origin_node
        self.destination_node = destination_node
        self.length = length
        self.num_sections = num_sections

        self.isBroken = False

        self.Status = [None for _ in range(self.parent.get_num_slots())]

        self.linkCostType = LinkCostType.minHops

    
    def get_origin_node(self) -> int:
        """Retorna o nó de origem

        Returns:
            int: Nó de origem
        """
        return self.origin_node

    
    def get_destination_node(self) -> int:
        """Retorna o nó de destino

        Returns:
            int: Nó de destino
        """
        return self.destination_node