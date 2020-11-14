from src.general_classes.settings import Routing_Type
from src.general_classes.route import Route


class Routing:
    def __init__(self, parent, *args, **kwargs) -> None:

        self.parent = parent
        
        self.save_route()
        
        self.KYEN = 3
    
    
    def save_route(self):
        if(self.parent.definitions.routing_algorithm == Routing_Type.Dijkstra.value):
            for origin_node in range(self.parent.topology.num_nodes):
                for destination_node in range(self.parent.topology.num_nodes):
                    if origin_node != destination_node:
                        route = self.Dijkstra(origin_node, destination_node)
                    else:
                        route = None
                    self.parent.topology.set_route(origin_node, destination_node, route)


    def Dijkstra(self, origin_node: int, destination_node: int) -> Route:
        """Calcula a menor rota entre a origem e o destino

        Args:
            origin_node (int): Nó de origem
            destination_node (int): Nó destino

        Returns:
            Route: Retorna uma rota mais curta
        """
        
        k = -1
        r = []

        num_node = self.parent.topology.get_num_nodes()

        CustoVertice = [0.0 for _ in range(num_node)]
        Precedente = [0 for _ in range(num_node)]
        Precedente = [0 for _ in range(num_node)]
        Precedente = [0 for _ in range(num_node)]
        PathRev = [0 for _ in range(num_node)]
        Status = [None for _ in range(num_node)]
        
        routeDJK = None

        networkDisconnected = False

        #Busca para todos os pares de nó a rota mais curta:
        for inter_node in range(num_node):
            if(inter_node != origin_node):
                CustoVertice[inter_node] = float('inf')
            else:
                CustoVertice[inter_node] = 0.0
            Precedente[inter_node] = -1
            Status[inter_node] = 0

        num_node_control = num_node

        while (num_node_control > 0 and not networkDisconnected):
            min_value = float('inf')

            for i_node in range(num_node):
                if (Status[i_node] == 0 and CustoVertice[i_node] < min_value):
                    min_value = CustoVertice[i_node]
                    k = i_node

            if k == destination_node:
                break

            Status[k] = 1

            num_node_control -= 1

            outputLinkFound = False

            for j_node in range(num_node):
                link = self.parent.topology.getLink(k, j_node)

                if ((link is not None) and (link.getCost() < float('inf')) and (self.parent.topology.isNodeWorking(link.get_origin_node())) and (self.parent.topology.isNodeWorking(link.get_destination_node()))):
                    outputLinkFound = True

                    if ((Status[j_node] == 0) and (CustoVertice[k] + link.getCost() < CustoVertice[j_node])):
                        CustoVertice[j_node] = CustoVertice[k] + link.getCost()
                        Precedente[j_node] = k
            if not outputLinkFound:
                networkDisconnected = True

        if not networkDisconnected:
            PathRev[0] = destination_node
            hops = 0
            j = destination_node
            while(j != origin_node):
                hops += 1
                PathRev[hops] = Precedente[j]
                j = Precedente[j]

            r.clear()

            for h in range(hops + 1):
                r.append(PathRev[hops - h])
            routeDJK = Route(r, self) 
        
        del CustoVertice, Precedente, Status, PathRev
        return routeDJK