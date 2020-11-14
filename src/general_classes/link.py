from src.general_classes.settings import LinkCostType, SLOT_FREE, SLOT_USED
import src.general_classes.general as General

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


    def setAsBroken(self) -> None:
        """Configura o link como quebrado
        """
        self.isBroken = True


    def setAsWorking(self) -> None:
        """Configura o link como funcionando
        """
        self.isBroken = False


    def getCost(self) -> float:
        """Retorna o custo do link a depender da métrica escolhida

        Returns:
            float: Custo do link
        """
        if self.isBroken:
            return float('inf')

        if self.linkCostType == LinkCostType.minHops: #Assuming MinHops
            return 1.0
        else:
            if self.linkCostType == LinkCostType.minLength: #Assuming MinDist
                return self.length
            else:
                raise ValueError("A métrica usada está incompátivel")
        

    def initialise(self) -> None:
        """Inicia o link com todos os slots livres
        """
        self.Status = [SLOT_FREE for _ in range(self.parent.num_slots)]


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

    
    def isSlotOccupied(self, slot: int) -> bool:
        if(self.Status[slot] == SLOT_USED):
            return True
        return False


    def releaseSlot(self, slot: int) -> None:
        assert(self.isSlotOccupied(slot))
        self.Status[slot] = SLOT_FREE


    def occupySlot(self, slot: int) -> None:
        assert(self.isSlotFree(slot))
        self.Status[slot] = SLOT_USED
    

    def isSlotFree(self, slot: int) -> bool:
        return not self.isSlotOccupied(slot)


    def calcSignal(self, signal) -> None:
        # Link structure: fiber - Amp - fiber - Amp ... fiber - Amp
        # Assuming a link with equal gain distribution
        signalPower = signal.getSignalPower()
        asePower = signal.getAsePower()
        nonLinearPower = signal.getNonLinearPower()
    
        Lsec = self.length / self.num_sections
        gLsec = 1.0 / (General.dBtoLinear(Lsec * signal.Alpha)) # Fiber Gain
        gAmp = 1.0 / gLsec # Amplifier Gain
        # Consideration of the link Sections:
        for _ in range(self.num_sections):
            # Fibre:
            signalPower *= gLsec
            asePower *= gLsec
            nonLinearPower *= gLsec
            nonLinearPower += 0.0 #Alterar esse 0.0 para a potência fornecida pela seção
            # Amplifier:
            signalPower *= gAmp
            asePower *= gAmp
            asePower += signal.pASE(signal.fn, gAmp)
            nonLinearPower *= gAmp
        
        signal.setSignalPower(signalPower)
        signal.setASEPower(asePower)
        signal.setNonLinearPower(nonLinearPower)
    

    def get_all_slots_status(self) -> list:
        """Retorna os estados para todos os slots

        Returns:
            list: Todos os slots e seus estados
        """
        return self.Status