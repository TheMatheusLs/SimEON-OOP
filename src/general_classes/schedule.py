from src.general_classes.event import Event


class Schedule:
    def __init__(self, parent, *args, **kwargs):

        self.parent = parent


    def initialise(self):
        """Inicializa as variáveis
        """
        self.first_event = None
        self.sim_time = 0.0


    def setSimTime(self, time: float) -> None:
        """Configura o tempo de simulação

        Args:
            time (float): Tempo de simulação novo
        """
        self.sim_time = time
    

    def getSimTime(self) -> float:
        """Retorna o tempo de simulação

        Returns:
            float: Tempo de simulação
        """
        return self.sim_time
    

    def scheduleEvent(self, event: Event) -> None:
        """Programa o próximo evento

        Args:
            event (Event): Próximo evento
        """
        evtAux = self.first_event
        evtAnt = None

        while(evtAux != None):
            if(event.getTime() < evtAux.getTime()):
                break
            else:
                evtAnt = evtAux
                evtAux = evtAux.getNextEvent()
            
        event.setNextEvent(evtAux)
        if(evtAnt == None):
            self.first_event = event
        else:
            evtAnt.setNextEvent(event)


    def getCurrentEvent(self) -> Event:
        """Retorna o evento atual

        Returns:
            Event: Vento atual
        """
        curEvt = self.first_event
        if(self.first_event != None):
            self.setSimTime(curEvt.getTime())
            self.first_event = self.first_event.getNextEvent()
        
        return curEvt
    

    def isEmpty(self) -> bool:
        return (self.first_event == None)