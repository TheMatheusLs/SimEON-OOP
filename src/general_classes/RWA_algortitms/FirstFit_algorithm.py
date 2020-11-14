from src.general_classes.assignment import Assignment


def FirstFit(assignment: Assignment) -> tuple:
        """Algoritmo FirstFit. Seleciona o primeiro slot disponivel para a rota

        Args:
            assignment (Assignment): Pedido de requisição

        Returns:
            tuple: Slot inicial e slot final
        """
        route = assignment.getRoute()
        num_slots_req = assignment.getNumSlots()

        # 0 significa que o slot está livre
        busy_slots= [0 for _ in range(assignment.parent.topology.get_num_slots())]

        for link in route.links:
            for index_slot, slot_by_link in enumerate(link.Status):
                busy_slots[index_slot] |= slot_by_link

        current_free_slots = 0

        for index_slot in range(assignment.parent.topology.get_num_slots() - num_slots_req + 1):
            if not busy_slots[index_slot]:
                current_free_slots += 1
            else:
                current_free_slots = 0

            if current_free_slots == num_slots_req:
                return (index_slot - num_slots_req + 1), index_slot

        return -1, -1