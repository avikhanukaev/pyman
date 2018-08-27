class GraphNode:
    """
    This class is responsible for the representation and functionality
    of single node of graph. This class is *Helper* class for the search
    algorithms and especially for the Dijkstra shortest path algorithm.

    Important note
    --------------
    This class is not a general class and is constructed to be used inside the
    Dijkstra search algorithm. It can be used with all similar algorithms, but
    should not be used as general graph node for other graph applications.
    """

    def __init__(self, data='', parent='', distance=60000, visited=False):
        """
        Default c'tor.

        :param data: str, the data that is holded inside the graph. Note that
        the data not necessarily is string - it can be other type also - but it
        should be comparable data type.

        :param parent: parent node is used in search algorithm on graphs. It is
        the node that leads to the current node.

        :param distance: int, it is the current distance of the node from
        specified node. Once again, as stated in the class description - this
        parameter is very important for search algorithm by may not have any
        importance in other algorithms and graph applications.

        :param visited: bool, is node is already visited by algorithm or not.
        """
        self.data = data
        self.parent = parent
        self.distance = distance
        self.visited = visited

        self.adj = {}
        '''This is the list of an adjacent nodes. For ease of use, I've decided 
        to implement this list with the dictionary data structure where the key 
        is nodes name (identified by node data property) and the value is the 
        score (or the distance) of edge from current node to the specified node 
        in key.
        
        For example, if the current node is node 'a' and graph that contains 
        that node has the following edges {a,b}, {a,c}, {a,d} and each edge has
        score of 12, 4 and 100 respectively, then the adjecent list of that node 
        will look as follows: { 'a' : 12, 'b' : 4, 'c' : 100 }'''

    def add_adj(self, data, edge_distance):
        """
        This function is responsible to add new node and distance score to
        current nodes adj. list.

        This function should be called during the parsing process of the graph
        and the construction of the entire graph.

        :param data: str, the name of another node.

        :param edge_distance: int, the score of the edge from current node to
        that node.

        :return: None
        """
        self.adj[data] = edge_distance

    def get_all_adj(self):
        """
        This function returns list representation of the adj. list. Each object
        inside that list has the following format [node, score].

        For example
        -----------

        Assume that the current node is 'a' and it has 2 adj. nodes {'b', 'c'}
        and edges {'a', 'b'} and {'a', 'c'} has scores of 3, 4 respectively.
        Then, such function will return the following list:
            [ ['b', 3], ['c', 4] ].


        :return: List of adj. nodes and scores of edges to that list.
        """
        list_of_adj_nodes = []
        for k, v in self.adj:
            list_of_adj_nodes.append([k, v])
        return list_of_adj_nodes

    def __eq__(self, other):
        """
        Comparator between nodes. It compares based on the data type.
        :param other: GraphNode, another object of GraphNode.
        :return: True, if and only if self.Data == other.Data.
        """
        return self.data == other.data


class DijkstraAlgorithm:
    """
    This class responsible for the implementation of the Dijkstra search
    algorithm.


    Short introduction:
    -------------------

    Dijkstra's algorithm is an algorithm for finding the shortest paths between
    nodes in a graph, which may represent, for example, road networks. It was
    conceived by computer scientist Edsger W. Dijkstra in 1956 and published
    three years later.


    Example:
    --------

    Assume the following graph given as tuple of G = (V, E, w) where V is set
    of vertices, E is the set of edges and w: E -> N is the weight function (the
    score function on each edge).

    It is important to node that:
        (a) The graph is undirected graph (for directed graphs there are other
        algorithms);
        (b) The weight function w is *positive* function.

    The given graph is:
        (a) V = {'a', 'b', 'c', 'd'}
        (b) E = { {'a', 'b'}, {'b', 'd'}, {'a', 'c'}, {'c', 'd'} }
        (c) w: E -> N is :
                {'a', 'b'} --> 1
                {'a', 'c'} --> 2
                {'b', 'd'} --> 3
                {'c', 'd'} --> 4

    Basically, if we draw the graph we will have the following picture:

                                    (a)
                                    /  \
                                   /    \
                                1 /      \  2
                                 /        \
                                /          \
                              (b)          (c)
                                \           /
                                 \         /
                                3 \       / 4
                                   \     /
                                    \   /
                                    (d)

    Now, assume that we want the shortest path possible from node 'a' to node
    'd'. We have two possible options.

        (1) p1 = { {'a', 'b'}, {'b', 'd'} } which will score total of 1 + 3 = 4.
        (2) p2 = { {'a', 'c'}, {'c', 'd'} } which will score total of 2 + 4 = 6.

    So, the shortest path is p1.

    The current algorithm of Dijkstra will return the shortest path from node
    to node. In our case, it will return p1.


    Usage of the class
    ------------------

    We will demonstrate usage of the algorithm on the previous example. First of
    all we should construct the query object. It is done as follows -

        dj_algorithm = DijkstraAlgorithm(['a', 'b', 'c', 'd'],
                                        [   ['a', 'b', 1],
                                            ['a', 'c', 2],
                                            ['b', 'd', 3],
                                            ['c', 'd', 4]   ])

    Next, we may query by using the following command

        shortest_path = dj_algorithm.find_shortest_path('a', 'd')

    The shortest_path is the list that will have the following form

        shortest_path = ['a', 'b', 'd']

    This means that we go from 'a' to 'b' and from 'b' to 'd' to reach the
    shortest path.


    The main ideas behind the design of class
    -----------------------------------------

    The idea is that we supply a reprehension of the graph. We will supply the
    pythonian list of all vertices (for example ['a', 'b', 'c', 'd']). The list
    of vertices will contain the data/name if each vertex and not the GraphNode
    object. We also supply the list of all edges and their scores/ (for example
    [ ['a', 'b', 1], ['a', 'c', 3], ...]). The class will construct inner
    representation of the graph. By this inner representation of the graph we
    will be able to query the graph for any number of times we want and whenever
    we want so.

    The idea behind such implementation is to make the class general and for
    general purpose. First of all, there are a lot of programs that uses graphs
    and computations on graph and each such program may have its own repr.
    for a graph. I wanted to make this algorithm general and the G = (V, E)
    representation is convenient mathematical representation of graph. In my
    opinion it is easier to convert some representation of graph into the (V, E)
    representation than adapt the algorithm for a particular use.

    Another point behind such design is that in large constant graphs we have
    single object during all program and we may query it as many times as
    we want without the re-construction of the graph each time. I think, that
    for good example, it may be useful for games, maps and navigation  - where
    we have constant large map, we represent it as graph and then query it as
    many times as we want.
    """

    def __init__(self, vertices, edges):
        """
        The default c'tor.
        :param vertices: List of all vertices. For example ['a', 'b', 'c', ...].
        :param edges: List of all edges and their scores [ ['a', 'b', 1'],
        ['a', 'c', 2], ... ]
        """
        self.nodes = {}

        for v in vertices:
            nv = GraphNode(data=v)
            self.nodes[v] = nv

        for e in edges:
            self.nodes[e[0]].add_adj(e[1], e[2])
            self.nodes[e[1]].add_adj(e[0], e[2])

    def reset(self):
        """
        This function resets graph internal data and prepares it to another
        query.
        :return: None
        """
        for k in self.nodes:
            self.nodes[k].parent = ''
            self.nodes[k].distance = 60000
            self.nodes[k].visited = False

    def get_min_vertex(self):
        """
        This function returns the vertex with that is not visited yet and has
        minimal distance score. It is the minimal distance score from particular
        vertex. This function is mainly used during the query of the algorithm.
        :return: vertex with minimal score.
        """
        min_distance = 60000
        min_vertex = ''
        for v in self.nodes:
            if self.nodes[v].distance < min_distance and \
                    not self.nodes[v].visited:
                min_vertex = v
                min_distance = self.nodes[v].distance
        return min_vertex

    def find_shortest_path(self, from_v, to_v):
        """
        The main function of the algorithm. It computes and returns the shortest
        path from from_v to to_v.
        :param from_v: str, the name/data of the original node.
        :param to_v: str, the name/data of the target node.
        :return: List of nodes [from_v, ..., to_v] that is the shortest path.
        """
        self.reset()
        self.nodes[from_v].distance = 0

        v = self.get_min_vertex()
        self.nodes[v].visited = True
        while v != to_v:
            for e in self.nodes[v].adj:
                if not self.nodes[e].visited:
                    if self.nodes[e].distance > (
                            self.nodes[v].distance + self.nodes[v].adj[e]):
                        self.nodes[e].distance = self.nodes[v].distance + \
                                                 self.nodes[v].adj[e]
                        self.nodes[e].parent = v
            v = self.get_min_vertex()
            self.nodes[v].visited = True

        path = []
        while v != from_v:
            path.append(v)
            v = self.nodes[v].parent
        path.append(v)

        path.reverse()

        return path


"""

# Example. To use it, undo the comments.
# --------------------------------------


dj_algorithm = DijkstraAlgorithm(['a', 'b', 'c', 'd'],
                                 [['a', 'b', 1],
                                  ['a', 'c', 2],
                                  ['b', 'd', 3],
                                  ['c', 'd', 4]])

path = dj_algorithm.find_shortest_path('a', 'd')

print(path)

"""
