import sys
from types import ModuleType, FunctionType
from gc import get_referents
from collections import deque, defaultdict

# --------------------------------------------------------------
# Custom Tree Data Structure
# Probably not very fast
# TODO: Error Handling


class NullData:
    pass


class TreeNode(object):
    def __init__(self, data, children=NullData) -> list:
        self.data = data
        if children is not NullData:
            self.attach(children)

    def __getitem__(self, index):
        return self.children[index]

    def attach(self, children):
        self.children = deque()
        for each in children:
            self.children.append(TreeNode(each))


class Tree(object):
    def __init__(self, new_nodes=NullData, new_children=NullData) -> list:
        """Creates a tree and takes lists for new nodes and, optionally, their children.
           Uses NullData in place of None so that None may be used as placeholders."""
        if new_nodes is not NullData:
            self.nodes = deque()
            for index, value in enumerate(new_nodes):
                if new_children is not NullData:
                    self.nodes.append(
                        TreeNode(value, new_children[index]))

    def __getitem__(self, index):
        return self.nodes[index]

    def __len__(self):
        return len(self.nodes)


# --------------------------------------------------------------
# Undirected Graph Data Structure
# From https://www.bogotobogo.com/python/python_graph_data_structures.php
# Might be more than I need, but oh well. Tweaked to add multiple weights.

class Vertex:
    """Vertex Class uses a dictionary to keep track of what vertices to
    which it is connected, as well as the weight of each connecting edge.

    Arguments:
    node = the name or ID of the Vertex being added to the Graph"""

    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]


class Graph:
    """Graph Class creates a dictionary that comprises of all Vertices
    within the created Graph. To create a Graph, invoke the function
    add_vertex() and add_edge()."""

    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        """Returns Vertex.__str__ for each Vertex in the Graph when iterated."""
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        """Creates a new instance of the Vertex class within the Graph.
        Vertex Class uses a dictionary to keep track of vertices to which it is
        connected, as well as the weight of each edge.

        Arguments:
        node = the name or ID of the Vertex being added to the Graph"""
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost=0):
        """Adds an edge between two nodes and it's associated weight.

        Arguments:
        frm = Source node
        to = Destination node
        cost = Edge Weight."""
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

# --------------------------------------------------------------
# More Comprehensive getsize function
# From Russia Must Remove Putin @ https://stackoverflow.com/questions/449560/how-do-i-determine-the-size-of-an-object-in-python
# Super detailed answer and explaination


BLACKLIST = type, ModuleType, FunctionType


def getsize(obj):
    """sum size of object & members."""
    if isinstance(obj, BLACKLIST):
        raise TypeError(
            'getsize() does not take argument of type: ' + str(type(obj)))
    seen_ids = set()
    size = 0
    objects = deque([obj])
    while objects:
        need_referents = deque()
        for obj in objects:
            if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                seen_ids.add(id(obj))
                size += sys.getsizeof(obj)
                need_referents.append(obj)
        objects = get_referents(*need_referents)
    return size

# --------------------------------------------------------------
# Imperial to Metric


def imperialToMetric(imperial, mode):
    """Converts input imperial to metric based on mode
    Mode 0 is inches to cm
    Mode 1 is lbs to kg"""
    metric = 0
    match mode:
        case 0:
            metric = imperial * 2.54
        case 1:
            metric = imperial * 0.453592

    return metric


# --------------------------------------------------------------
# Base10 to Base62 Coverter for NPC UUID
# From Baishampayan Ghose @ https://stackoverflow.com/questions/1119722/base-62-conversion
# Also includes a decoder that I don't think I'll need
BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode(num, alphabet=BASE62):
    """Encode a positive number into Base X and return the string.

    Arguments:
    - `num`: The number to encode
    - `alphabet`: The alphabet to use for encoding
    """
    if num == 0:
        return alphabet[0]
    arr = deque()
    arr_append = arr.append  # Extract bound-method for faster access.
    _divmod = divmod  # Access to locals is faster.
    base = len(alphabet)
    while num:
        num, rem = _divmod(num, base)
        arr_append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)
