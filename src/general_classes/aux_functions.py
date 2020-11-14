from src.general_classes.settings import Topology_Type, TOPOLOGY_PATH, Routing_Type, Spectrum_Type

def topology_full_path(topology_value: int) -> str:
    
    for key, value in Topology_Type.__members__.items():
        if topology_value == value.value:
            return TOPOLOGY_PATH(key)
    
    raise ValueError("Invalid choice")


def gen_filename_report(topology_select: int, routing_select: int, spectrum_select: int) -> str:

    topology_name = [key for key, value in Topology_Type.__members__.items() if value.value == topology_select][0]

    routing_name = [key for key, value in Routing_Type.__members__.items() if value.value == routing_select][0]

    spectrum_name = [key for key, value in Spectrum_Type.__members__.items() if value.value == spectrum_select][0]

    return f"{topology_name}_{routing_name}_{spectrum_name}"