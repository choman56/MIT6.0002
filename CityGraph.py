#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 15:04:56 2016.

@author: guttag, revised egrimson
revised: Clarke Homan (include distance within edge) Oct 26, 2020

"""

class Node(object):

    def __init__(self, name):
        '''
        Args:
            name (str): DESCRIPTION.

        Returns:
            None.

        '''
        self.name = name
    def getName(self):
        """
        Fetch node name method.

        Returns
        -------
            str: Node name.

        """
        return self.name
    def __str__(self):
        return self.name

class Edge(object):
    """Class to model edge."""

    def __init__(self, src, dest, distance=1):
        """
        Edge creation method.

        Assumes src and dest are nodes.
        Distance is an integer.
        """
        self.src = src
        self.dest = dest
        self.distance = distance

    def getSource(self):
        '''

        Returns:
            TYPE: DESCRIPTION.

        '''
        return self.src

    def getDestination(self):
        return self.dest

    def getDistance(self):
        return self.distance

    def __str__(self):
        return self.src.getName() + '->' + self.dest.getName()

class Digraph(object):
    """edges is a dict mapping each node to a list of
    its children"""
    def __init__(self):
        self.edges = {}
    def addNode(self, node):
        if node in self.edges:
            raise ValueError('Duplicate node')
        else:
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        distance = edge.getDistance()
        if not (src in self.edges and dest in self.edges):
            raise ValueError('Node not in graph')
        self.edges[src].append([dest, distance])
    def childrenOf(self, node):
        if type(node) == list:
            return self.edges[node[0]]
        else:
            return self.edges[node]
    def hasNode(self, node):
        return node in self.edges
    def getNode(self, name):
        for n in self.edges:
            if n.getName() == name:
                return n
        raise NameError(name)
    def __str__(self):
        result = ''
        for src in self.edges:
            for dest in self.edges[src]:
                result = result + src.getName() + '->'\
                         + dest.getName() + '\n'
        return result[:-1] #omit final newline

class Graph(Digraph):
    def addEdge(self, edge):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.addEdge(self, rev)
    
def buildCityGraph(graphType):
    g = graphType()
    for name in ('Boston', 'Providence', 'New York', 'Chicago',
                 'Denver', 'Phoenix', 'Los Angeles'):  # Create 7 nodes
        g.addNode(Node(name))
    g.addEdge(Edge(g.getNode('Boston'), g.getNode('Providence'), 50))
    g.addEdge(Edge(g.getNode('Boston'), g.getNode('New York'), 216))
    g.addEdge(Edge(g.getNode('Providence'), g.getNode('Boston'), 50))
    g.addEdge(Edge(g.getNode('Providence'), g.getNode('New York'), 182))
    g.addEdge(Edge(g.getNode('New York'), g.getNode('Chicago'), 792))
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Denver'), 1006))
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Phoenix'), 1758))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('Phoenix'), 821))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('New York'), 1782))
    g.addEdge(Edge(g.getNode('Los Angeles'), g.getNode('Boston'), 2987))
    g.addEdge(Edge(g.getNode('New York'), g.getNode('Providence'), 182))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('Boston'), 1975))
    g.addEdge(Edge(g.getNode('Phoenix'), g.getNode('Los Angeles'), 373))
    return g


def printPath(path):
    """Assumes path is a list of nodes"""
    result = ''
    for i in range(len(path)):
        if i > 0:
            nodePrt = path[i]
            result = result + str(nodePrt[0].getName())
        else:
            result = result + str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result

def pathCost(path):
    """
    Calculate culmulative 'cost' for a given path.

    Sums the cost attributes for each of the city nodes. Each list element
    is a list of 2 elements, with the first sublist element being the city
    node and the 2nd element being the cost (distance but could represent
    other costs). The first path element is a source city node and not a list.
    All subsequent path list items are 2 element city and cost lists.

    Args
    ----
        path (LIST): Assumes path is actually a list of nodes

    Returns
    -------
        Cost (int)

    """
    cost = 0
    if path is not None:
        for i in range(1, len(path)):
            cost += path[i][1]

    return cost


def DFS(graph, start, end, path, shortest, toPrint = False):
    """Assumes graph is a Digraph; start and end are nodes;
          path and shortest are lists of nodes
       Returns a shortest path from start to end in graph"""
    path = path + [start]

    if toPrint:
        print('Current DFS path:', printPath(path))

    if type(start) == list:
        nodeptr = start[0]
        if nodeptr ==  end:
            return path
    else:    
        if start == end:
            return path

    for node in graph.childrenOf(start):
        if node[0] not in path: #avoid cycles
            if shortest == None or len(path) < len(shortest):
                newPath = DFS(graph, node, end, path, shortest,
                              toPrint)
                if shortest is None:
                    shortest = newPath.copy()
                elif newPath is not None:
                    currentPathDistance = pathCost(shortest)
                    newPathDistance = pathCost(newPath)
                    if newPathDistance < currentPathDistance:
                        shortest = newPath.copy()
        elif toPrint:
            print('Already visited', node)
    return shortest
    
def shortestPath(graph, start, end, toPrint = False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    return DFS(graph, start, end, [], None, toPrint)

def testSP(source, destination):
    g = buildCityGraph(Digraph)
    sp = shortestPath(g, g.getNode(source), g.getNode(destination),
                      toPrint = True)
    if sp != None:
        print('Shortest path from', source, 'to',
              destination, 'is', printPath(sp), 'with', pathCost(sp), 'distance')
    else:
        print('There is no path from', source, 'to', destination)

testSP('Chicago', 'Boston')
print()
#testSP('Boston', 'Phoenix')
#print()

printQueue = True 

def BFS(graph, start, end, toPrint = False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    initPath = [start]
    pathQueue = [initPath]
    while len(pathQueue) != 0:
        #Get and remove oldest element in pathQueue
        if printQueue:
            print('Queue:', len(pathQueue))
            for p in pathQueue:
                print(printPath(p))
        tmpPath = pathQueue.pop(0)
        if toPrint:
            print('Current BFS path:', printPath(tmpPath))
            print()
        lastNode = tmpPath[-1]
        if lastNode == end:
            return tmpPath
        for nextNode in graph.childrenOf(lastNode):
            if nextNode not in tmpPath:
                newPath = tmpPath + [nextNode]
                pathQueue.append(newPath)
    return None

def shortestPath(graph, start, end, toPrint = False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    return BFS(graph, start, end, toPrint)
    
# testSP('Boston', 'Phoenix')