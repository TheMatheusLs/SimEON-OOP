from src.general_classes.settings import EventType
from src.general_classes.connection import Connection   

class Event:
    def __init__(self, parent, *args, **kwargs):
        
        self.parent = parent

    def setRequestEvent(self, time: float) -> None:
        """Configura os eventos e a conexão

        Args:
            time (float): Tempo de evento
        """
        self.time = time
        self.type_req = EventType.Req
        self.setNextEvent(None)
        self.setConnection(None)
    
    def setTime(self, time) -> None:
        self.time = time

    def setType(self, event_type) -> None:
        self.type_req = event_type

    def setNextEvent(self, event) -> None:
        """Configura o próximo evento

        Args:
            event (Event): Próximo evento
        """
        self.next_event = event

    def getNextEvent(self):
        """Retorna o próximo evento

        Returns:
            Event: Próximo evento
        """
        return self.next_event

    def setConnection(self, connection: Connection) -> None:
        """Configura a conexão

        Args:
            connection (Connection): Conexão
        """
        self.connection = connection

    def getTime(self) -> float:
        """Retorna o tempo do evento

        Returns:
            float: Tempo do evento atual
        """
        return self.time
    
    def getType(self) -> EventType:
        return self.type_req

    def setReleaseEvent(self, event, newConnection):
        event.setTime(newConnection.getTimeDesc())
        event.setType(EventType.Desc)
        event.setNextEvent(None)
        event.setConnection(newConnection)

    def getConnection(self) -> None:
        return self.connection 