#
# 6.0002 Problem Set 1a: Space Cows
# Name: Clarke A Homan
# Collaborators:
# Time:
#

from ps1_partition import get_partitions
import time

# ================================
# Part A: Transporting Space Cows
# ================================

#
# Problem 1
#


def load_cows(filename):
    """
    Read the contents of the given file.  Loads cow info.

    Assumes the file contents contain data in the form of comma-separated
    cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as
    values.

    Parameters
    ----------
    filename - the name of the data file as a string

    Returns
    -------
    a unsorted dictionary of cow name (string), weight (int) pairs

    """
    # TODO: Your code here
    print("Loading cows from file...\n")
    inFile = open(filename, 'r')
    nextLineStr = inFile.readline()
    if nextLineStr == '':   # test for empty file
        cowDict = {}
        return cowDict
    cowNameStr, cowWeightStr = nextLineStr.split(',')
    cowDict = {cowNameStr: int(cowWeightStr)}  # add 1st cow to dictionary
    endofFile = False
    while not endofFile:
        nextLineStr = inFile.readline()  # fetch next cow info
        if nextLineStr == '':            # if no more cow info, quit looping
            break
        cowNameStr, cowWeightStr = nextLineStr.split(',')
        cowDict[cowNameStr] = int(cowWeightStr)  # add next cow info to dict
    inFile.close()  # close file
    return cowDict  # return cow dictionary
    # pass


def sort_Cows(cows):
    """
    Generate a sorted cow dictionary from a unsorted dictionary.

    Args
    ----
        cows (Dictionay): DESCRIPTION.

    Returns
    -------
        localCows  (List) sorted by weight (decending)
        sortedCows (Dictionary) sorted by weight (decending)
    """
#
# Create a sorted dictionary of candidate cows, ready for travel
#
    localCows = sorted(cows, key=cows.__getitem__, reverse=True)
    localCowsDict = {}
    for i in localCows:
        localCowsDict[i] = cows.get(i)

    return localCows, localCowsDict

#
# Problem 2: procedure greedy_cow_transport()
#


def greedy_cow_transport(cows, limit=10):
    """
    Determine allocation of cows to transport using 'greedy algorithm'.

    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows.
    The returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow
       that will fit to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters
    ----------
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns
    -------
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips

    Procedure Steps
    ---------------
    1. Generate sorted version (copy) of passed in cow dictionary
    2. Loop thru sorted cow dict (cowDict) selecting the next available cow
       that doesn't cause the total cow payload to exceed the wieght limit
       constraint.
        a. Add the cow to the current trip sublist and update trip tare value
           with selected cow's weight
        b. Once all remaining cows are evaluated, remove the cows from the
           remaining cows list that were selected for the current trip to
           prevent them from being reselected in subsequent trips.
    3. Once a trip is "full" (collective weight ), if there are remaining cows
       to be transported, start a new list and loop thru remaining cows
    4. Once all cows have be selected for some trip, return lists of list
    """
    # TODO: Your code here

#
# Create a sorted dictionary of candidate cows, ready for travel
#
    localCowsNames, localCowsDict = sort_Cows(cows)

    tripPayLoad = 0
    globalCowList = []

#
#  Loop thru remaining candidate cows in the sorted dictionary. Select
#  the heaviest cow (which will be the first cow in the dictionary) and then
#  add cows to the payload that whose collective weight does not exceed the
#  total payload weight limit. Cows that have been selected for a trip, are
#  removed from the candidate pool. Trip lists are bundled together within a
#  returned "global" list of lists.
#

    while len(localCowsDict) > 0:  # while there are remaining cows to be taken
        localList = []
        for i in localCowsDict:    # loop thru remaining cows
            if localCowsDict[i] <= (limit - tripPayLoad):
                localList.append(i)     # add selected cow to local list
                tripPayLoad += localCowsDict[i]  # update current trip payload
        if len(localList) > 0:
            for j in localList:
                localCowsDict.pop(j)  # remove selected cow(s) from potentials
        globalCowList.append(localList)  # add trip cows to list of trip lists
        tripPayLoad = 0         # zero out local trip payload for next trip
    return globalCowList
    # pass

#
# Problem 3: procedure brute_force_cow_transport()
#


def brute_force_cow_transport(cows, limit=10):
    """
    Determine list (trips) of cows for transport using brute force method.

    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following
    method:

    1. Enumerate all possible ways that the cows can be divided into separate
       trips. Use the given get_partitions function in ps1_partition.py to help
       you!
    2. Select the allocation that minimizes the number of trips without making
       any trip that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters
    ----------
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns
    -------
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here

# Sort the cow dictionary generating a copy (not sure if needed)
    # localCowsNames, localCowsDict = sort_Cows(cows)

    localCowsNames = []
    for i in cows.keys():
        localCowsNames.append(i)

    localCowsDict = cows.copy()

#
# Will contain lists of candidate cow trips (meet trip payload restrictions)
#
    candidatePartitionSet = []

#
# Generate all possible set partitions of cows using get_partitions.
# For each trip within a given partitioning, see if any trip exceeds trip
# weight restrictions. If any trip within a partition set violates weight limit
# then throw out partition. If all trips wihtin a partition abides the trip
# weight restriction, then add the partition to the candidiatePartitionSet
# list. Process all partitions to generate all candidiate partition.
#
    for partition in get_partitions(localCowsNames):
        includePartition = True
        for subList in partition:
            localPayLoad = 0
            for k in subList:
                localPayLoad += localCowsDict[k]
            if localPayLoad > limit:
                includePartition = False
                break
        if includePartition:
            candidatePartitionSet.append(partition)

#
# Find the first partition with the lowest number of trips. Number of trips
# is determined by the len of the partition array which contain trip lists.
#
    minTrips = len(cows)
    maxTrips = 0
    j = 0
    for i in candidatePartitionSet:
        numTrips = len(candidatePartitionSet[j])
        if numTrips < minTrips:
            minTrips = numTrips
            minTripSet = candidatePartitionSet[j]
        # if numTrips > maxTrips:
            # maxTrips = numTrips
            # maxTripSet = candidatePartitionSet[j]
        j += 1
        # print('Candidate partition number:', j,'->', i, ':', 'number of trips', len(i))

    # print('\nMinimum trips is', minTrips, 'with partition set:', minTripSet)
    # print('\nMaximum trips is', maxTrips, 'with partition set:', maxTripSet)

    return minTripSet
    # pass

#
# Problem 4: procedure compare_cow_transport_algorithm()
#


def compare_cow_transport_algorithms():
    """
    Compare the output performance of the two cow selection algorithms.

    Using the data from ps1_cow_data.txt and the specified weight limit, run
    your greedy_cow_transport and brute_force_cow_transport functions here.
    Use the default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns
    -------
    Does not return anything.
    """
    # TODO: Your code here
    # pass


greedyCowTrips = {}
bruteforceCowTrips = {}

#
# Load cows information from file
#

fileName = 'ps1_cow_data.txt'
cowDict = load_cows(fileName)

#
# Determine cow trip sets for a all cows using greedy method (heaviest cow
# loaded with filler cows if weight restriction is not exceeded). All cows
# have to be transported in some trip.
#

#
# Timer setup
#
greedyStartTime = time.time()
greedyCowTrips = greedy_cow_transport(cowDict)
greedyEndTime = time.time()
greedyTime = greedyEndTime - greedyStartTime
print('Greedy method partitioning with', len(greedyCowTrips),
      'List:', greedyCowTrips, 'Total time:', greedyTime, '\n')

#
# Determine cow trip sets for a all cows using brute force method. Generate all
# possible cow trip combinations as partition sets.  Throw out a generated
# partition if any trip within the partition exceeds weight restrictions.
# Select the first partition with the minimum number of trips that carry all
# cows. All cows have to be transported in some trip.
#

bruteforceStartTime = time.time()
bruteforceCowTrips = brute_force_cow_transport(cowDict)
bruteforceEndTime = time.time()
bruteforceTime = bruteforceEndTime - bruteforceStartTime
print('Brute force method partitioning with:', len(bruteforceCowTrips),
      'List:', bruteforceCowTrips, 'Total time:',
      bruteforceTime, '\n')

print('Difference in time between brutefoce and greedy', bruteforceTime -
      greedyTime, 'Percentage improvement difference of greedy to bruteforce', 
      ((bruteforceTime - greedyTime)/greedyTime)*100.0)
