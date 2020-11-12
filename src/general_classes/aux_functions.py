from src.general_classes.settings import Topology_Type, TOPOLOGY_PATH

def topology_full_path(topology_value: int) -> str:
    
    for key, value in Topology_Type.__members__.items():
        if topology_value == value.value:
            return TOPOLOGY_PATH(key)
    
    raise ValueError("Invalid choice")