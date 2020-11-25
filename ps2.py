# 6.0002 Problem Set 5
# Graph optimization
# Name:  Clarke A. Homan
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
"""
    The load_map function is provided as an argument the filename (with path
    if necessary) of the 'map file'. The map file is a text file with the
    following specification:
        Each text line in the file represents an edge specification
            Each edge specification has four numbers. The first number is the
            source (starting) building number. The second number is the
            destination (ending) building number. The third number represents
            the total distance between the buildings. The fourth number
            represents the distance between the two buildings that are outside
            'in the cold'. There is a restriction that the fourth number cannot
            exceed the third number, as there cannot be a edge (path) where the
            outside distance between building exceeds the total distance
            between buildings.

    Buildings will be represented as 'nodes' within the digraph. Paths between
    buildings will be represented as 'edges' connecting nodes within the graph.
    Each path edge that connects two nodes will have two properties. One
    property will be the 'total distance' between the two nodes. The other
    property will be the 'outside distance' between the two nodes.

    The digraph is presented as a Python dictionary where each dictionary
    element's primary key is a building node. The 'value' that each node
    dictionary element contains is a list of edges objects, defining a path
    (source node, destination node, total distance)

    Within the digraph, each node that has a path (edge) defined to another
    node lists that node dictionary element containing a list of edges
    (objects) to the directly connected node(s). Each edge object contains a
    total distance and outside distance between the node element and the node
    its directly connected to.

    When a building number (either source or destination) is encountered within
    a text line extracted from the supplied file that has not been already
    defined (encountered) and defined within the digraph, a node object will be
    created and added to the digraph. Edges from the source node to a newly
    encounterd destination node will be added to the digraph's node dictionary
    edge list.

    New source and destination nodes will be added to the digraph's source node
    dictionary with a 'null' edge list. New destination nodes will be added to
    the digraphs node dictionary as well.
    
    Map datafile parser supports comments with leading character in line being
    '#'

"""
#


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parse the map file and constructs a directed graph.

    Parameters
    ----------
        map_filename : name of the map file

    Assumes
    -------
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns
    -------
        a Digraph representing the map
    """

    # TODO
    buildingDict = Digraph()
    print("Loading building map from file...")
    inFile = open(map_filename, 'r')
    found1stLine = False
    while not found1stLine:
        nextLineStr = inFile.readline()
        nextLineStr = nextLineStr.strip()
        if nextLineStr[0] == '#':
            continue
        else:
            found1stLine = True
            break
        
    if nextLineStr == '':   # test for empty file
        buildingDict = {}
        inFile.close()  # close file
        return buildingDict
    #
    # load first map datafile text line
    #
    sourceBuildingNum, destinationBuildingNum, totalDistanceStr, \
        outsideDistanceStr = nextLineStr.split(' ')
    sourceBldgNode = Node(sourceBuildingNum)
    destinationBldgNode = Node(destinationBuildingNum)
    #
    #  Test to see if outside distance is not greater than total distance in
    #  edge
    #
    totalDistance = int(totalDistanceStr)
    outsideDistance = int(outsideDistanceStr)
    if outsideDistance > totalDistance:
        raise ValueError('Outside distance greater than total distance \
                             on edge')
    #
    #  Since the map file is being initially read and the Digraph is empty,
    #  no need to test to see if nodes already entered in digraph. Will need to
    #  test for this case in subsequent lines read from file.
    #
    buildingDict.add_node(sourceBldgNode)
    buildingDict.add_node(destinationBldgNode)
    buildingEdge = WeightedEdge(sourceBldgNode, destinationBldgNode,
                                totalDistance, outsideDistance)
    buildingDict.add_edge(buildingEdge)

    #
    # Process the rest of the datafile, building nodes and edges on the fly and
    # adding them to the building dictionary.
    #
    endofFile = False
    while not endofFile:
        nextLineStr = inFile.readline()  # fetch next map element info
        nextLineStr = nextLineStr.strip()
        if nextLineStr == '':            # if no more map info, quit looping
            endofFile = True
            break
        if nextLineStr[0] == '#':
            continue

        sourceBuildingNum, destinationBuildingNum, totalDistanceStr, \
            outsideDistanceStr = nextLineStr.split(' ')
        sourceBldgNode = Node(sourceBuildingNum)
        destinationBldgNode = Node(destinationBuildingNum)
        #
        #  test to see if src node is not already entered into buildingDict
        #
        if sourceBldgNode not in buildingDict.edges:
            buildingDict.add_node(sourceBldgNode)
        #
        #  test to see if dest node is not already entered into buildingDict
        #
        if destinationBldgNode not in buildingDict.edges:
            buildingDict.add_node(destinationBldgNode)
        #
        #  Test to see if outside distance is not greater than total distance
        #  in edge
        #
        totalDistance = int(totalDistanceStr)
        outsideDistance = int(outsideDistanceStr)
        if outsideDistance > totalDistance:
            raise ValueError('Outside distance greater than total distance \
                             on edge')
        buildingEdge = WeightedEdge(sourceBldgNode, destinationBldgNode,
                                    totalDistance,
                                    outsideDistance)
        buildingDict.add_edge(buildingEdge)

    inFile.close()  # close file
    return buildingDict  # return building dictionary

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
# see below in 'main' module
#


#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
# The objective of this set of modules (get_best_path() and directed_dfs() )
# is to implement an optimized depth first search solution for providing the
# shortest path between two MIT buildings, subject to distance maximums
# constrainsts.
#

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters
    ----------
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns
    -------
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    if start == end:  # check to see if end of the current path trail
        return path  # if at the end of the path, return what you got as a path

    startNode = Node(start)
    endNode = Node(end)
    currShortestPath = []

    if not (digraph.has_node(startNode)):
        raise ValueError('Start node:', start, 'not in digraph')
    if not (digraph.has_node(endNode)):
        raise ValueError('End node:', end, 'not in digraph')

    for edge in digraph.get_edges_for_node(startNode):
        edgeDestNode = edge.get_destination()
        NextNodeName = edgeDestNode.get_name()

    #
    # Check to see if next destination node was already discovered in the last
    # best path
        if (len(best_path) != 0) and (NextNodeName in best_path[:-1]):
            continue

        if len(path) == 0:
            currentPathList = [start, NextNodeName]
            totalDistSoFar = edge.get_total_distance()
            totalOutDistSoFar = edge.get_outdoor_distance()
        else:
            if NextNodeName not in path[0]:  # check to avoid cycles
                currentPathList = path[0].copy()
                currentPathList.append(NextNodeName)
                totalDistSoFar = path[1] + edge.get_total_distance()
                totalOutDistSoFar = path[2] + edge.get_outdoor_distance()
            else:
                # print('Already visited node:', NextNodeName)
                continue  # skip this edge, try the next one from node

        if (totalOutDistSoFar > max_dist_outdoors):
            # print('Current edge add would exceeed max out distance', edge)
            continue  # skip this edge, try the next one from node

        if totalDistSoFar <= best_dist:
            newPath = [currentPathList, totalDistSoFar, totalOutDistSoFar]
            currShortestPath = get_best_path(digraph, NextNodeName, end,
                                             newPath, max_dist_outdoors,
                                             best_dist, best_path)
            if currShortestPath:
                return currShortestPath
            else:
                continue
                # return None
    return currShortestPath
    # TODO
    # pass


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    # TODO
    # pass
    path = get_best_path(digraph, start, end, [], max_dist_outdoors,
                  max_total_dist, [])
    if path:
        currentBestPath, currentMaxDistance, currentMaxOutDist = \
        path[0].copy(), path[1], path[2]
        while path:
            path = get_best_path(digraph, start, end, [], max_dist_outdoors,
                                 max_total_dist, currentBestPath)
            if path:
                if path[0] != currentBestPath:
                    currentBestPath, max_total_dist, currentMaxOutDist = \
                        path[0].copy(), path[1], path[2]
                else:
                #     print('Best path:', currentBestPath, 'Max distance',
                #           max_total_dist, 'Max out distance', currentMaxOutDist)
                    break
        print('Best path:', currentBestPath, '\nMax distance:',
              max_total_dist, 'and a Max out distance:', currentMaxOutDist)

        return currentBestPath
    else:
        raise ValueError("No path exists between bldgs %s and %s that \
                         satisfies both %s max distance and %s max outdoor \
                             distance constraints"
                         %(start, end, max_total_dist, max_dist_outdoors))


# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    # unittest.main()
    # # buildingGraph = load_map("test_load_map.txt")
    buildingGraph = load_map("mit_map.txt")
    startBldg = '2'
    endBldg = '9'
    maxTotalDistance = 114
    maxTotalOutsideDistance = 1000
    bestPath = directed_dfs(buildingGraph, startBldg, endBldg,
                            maxTotalDistance,maxTotalOutsideDistance)
    print('\nBest path between buildings %s and %s is:' % (startBldg,
          endBldg), bestPath)
    