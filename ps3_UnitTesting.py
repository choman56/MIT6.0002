#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 13:18:20 2020

@author: clarke homan
"""

import random
import ps3
import matplotlib.pyplot as plt
import math

def xyrange(x_upper_bound, y_upper_bound):
    """
    Return the cartesian product of range(x_upper_bound) and \
        range(y_upper_bound).

    Useful for iterating over the tuple coordinates of a room
    """
    for x in range(x_upper_bound):
        for y in range(y_upper_bound):
            yield (x, y)  # these are the room tile xy tuples



HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

if __name__ == "__main__":
    # height = 5
    # width = 4
    # room = ps3.RectangularRoom(width, height, 5)
    # pos = ps3.Position(0.75, 2.75)
    # updated = room.clean_tile_at_position(pos, 3)
    # updated = room.clean_tile_at_position(pos, 3)
    # updated = room.clean_tile_at_position(pos, 3)
    # pos1 = ps3.Position(.75, 2.0)
    # updated = room.clean_tile_at_position(pos1, 4)
    # updated = room.clean_tile_at_position(pos, 3)
    # print('Number of tiles cleaned is:', room.get_num_cleaned_tiles())
    # updated = room.clean_tile_at_position(pos, -3)
    # print('Number of tiles cleaned is:', room.get_num_cleaned_tiles())

    """
    Test 1a: test_room_dirt_dirty():

    Can fail either because get_dirt_amount is working incorrectly
    OR the student is initializing the dirt amount incorrectly
    """
    # width, height, dirt_amount = (3, 4, 1)
    # room = ps3.RectangularRoom(width, height, dirt_amount)
    # print('Testing room_dirt_clean module')
    # for x, y in xyrange(width, height):
    #     if room.get_dirt_amount(x, y) != dirt_amount:
    #         print("Tile {} was not initialized with correct dirt amount",
    #               format((x, y)))
    #     else:
    #         print('All tiles properly initialized with correct dirt amount')
#
#
#
    """
    test_room_dirt_clean():

    Can fail either because get_dirt_amount is working incorrectly
    OR the student is initializing the dirt amount incorrectly
    """
    # width, height, dirt_amount = (3, 4, 0)
    # room = ps3.RectangularRoom(width, height, dirt_amount)
    # print('\nTesting room_dirt_clean module')
    # for x, y in xyrange(width, height):
    #     if room.get_dirt_amount(x, y) != dirt_amount:
    #         print('Tile {} was not initialized with correct dirt amount tile \
    #               location: x:', x, 'y:', y)
    #     else:
    #         pos = ps3.Position(x, y)
    #         center = room.get_tile_center(pos)
    #         print('Tiles properly initialized with correct dirt amount tile \
    #               location: x:', center[0], 'y:', center[1])
#
#
#
    """
    test_is_tile_cleaned_dirty

    """
    # print('\nTesting is tile_cleaned module')
    # for i in range(2):
    #     width, height, dirt_amount = (3, 4, i)
    #     print('Dirt amount is', i)
    #     room = ps3.RectangularRoom(width, height, i)
    # #   Check all squares are unclean at start, given initial dirt > 1
    #     for x, y in xyrange(width, height):
    #         isCleaned = room.is_tile_cleaned(x, y)
    #         pos = ps3.Position(x, y)
    #         center = room.get_tile_center(pos)
    #         if not isCleaned:
    #             print('Unclean tile was returned at location: x:',
    #                   center[0], 'y:', center[1])
    #         else:
    #             print('Clean tile was returned at location: x:',
    #                   center[0], 'y:', center[1])
#
#
#
    """
    test_clean_tile_at_position_PosToZero

    Test if clean_tile_at_position removes all dirt
    """
    # width, height, dirt_amount = (3, 4, 1)
    # room = ps3.RectangularRoom(width, height, dirt_amount)
    # # Clean the tiles and confirm they are marked as clean
    # for x, y in xyrange(width, height):
    #     HeightPos = x + random.random()
    #     WidthPos = y + random.random()
    #     room.clean_tile_at_position(ps3.Position(HeightPos, WidthPos),
    #                                 dirt_amount)
    #     # using random.random in case there is any issue with specific
    #     # parts of a tile
    # for x, y in xyrange(width, height):
    #     isCleaned = room.is_tile_cleaned(x, y)
    #     pos = ps3.Position(x, y)
    #     center = room.get_tile_center(pos)
    #     if not isCleaned:
    #         print('Unclean tile was returned at location: x:',
    #               center[0], 'y:', center[1])
    #     else:
    #         print('Clean tile was returned at location: x:',
    #               center[0], 'y:', center[1])
#
#
#
    """
    test_get_num_cleaned_tiles_FullIn1

    Test get_num_cleaned_tiles for cleaning subset of room completely with
    1 call

    """
    # width, height, dirt_amount = (3, 4, 1)
    # room = ps3.RectangularRoom(width, height, dirt_amount)
    # cleaned_tiles = 0
    # # Clean some tiles
    # for x, y in xyrange(width-1, height-1):
    #     room.clean_tile_at_position(ps3.Position(x + random.random(),
    #                                               y + random.random()), 1)
    #     cleaned_tiles += 1
    #     num_cleaned = room.get_num_cleaned_tiles()
    #     if num_cleaned != cleaned_tiles:
    #         print("Number of clean tiles is incorrect: expected {}, got {}".
    #               format(cleaned_tiles, str(num_cleaned)))
    #     else:
    #         print("Number of clean tiles is correct: expected {}, got {}".
    #               format(cleaned_tiles, str(num_cleaned)))
#
#
#
    """
    test_get_num_cleaned_tiles_Partial

    Test get_num_cleaned_tiles for cleaning subset of room incompletely
    """
    # width, height, dirt_amount = (3, 4, 2)
    # room = ps3.RectangularRoom(width, height, dirt_amount)
    # cleaned_tiles = 0
    # # Clean some tiles
    # for x, y in xyrange(width-1, height-1):
    #     room.clean_tile_at_position(ps3.Position(x + random.random(), y +
    #                                               random.random()), 1)
    #     num_cleaned = room.get_num_cleaned_tiles()
    #     if num_cleaned != cleaned_tiles:
    #         print("Number of clean tiles is incorrect: expected {}, got {}".
    #               format(cleaned_tiles, str(num_cleaned)))
    #     else:
    #         print("Number of clean tiles is correct: expected {}, got {}".
    #               format(cleaned_tiles, str(num_cleaned)))

#
#
    """
    test_get_num_cleaned_tiles_FullIn2(self):

    Test get_num_cleaned_tiles for cleaning subset of room in two calls
    """
    # width, height, dirt_amount = (3, 4, 2)
    # room = ps3.RectangularRoom(width, height, dirt_amount)
    # cleaned_tiles = 0
    # # Clean some tiles
    # for x, y in xyrange(width-1, height-1):
    #     room.clean_tile_at_position(ps3.Position(x + random.random(), y +
    #                                               random.random()), 1)
    #     room.clean_tile_at_position(ps3.Position(x + random.random(), y +
    #                                               random.random()), 1)
    #     cleaned_tiles += 1
    #     num_cleaned = room.get_num_cleaned_tiles()
    #     if num_cleaned != cleaned_tiles:
    #         print("Number of clean tiles is incorrect: expected {}, got {}".
    #               format(cleaned_tiles, str(num_cleaned)))
    #     else:
    #         print("Number of clean tiles is correct: expected {}, got {}".
    #               format(cleaned_tiles, str(num_cleaned)))
#
#
#
    """
    test_get_num_cleaned_tiles_OverClean:

    Test cleaning already clean tiles does not increment counter
    """
    # width, height, dirt_amount = (3, 4, 2)
    # room = ps3.RectangularRoom(width, height, dirt_amount)
    # # clean all of the tiles in the room
    # for x, y in xyrange(width, height):
    #     room.clean_tile_at_position(ps3.Position(x + random.random(), y +
    #                                               random.random()), dirt_amount)
    # for x, y in xyrange(width, height):
    #     room.clean_tile_at_position(ps3.Position(x + random.random(), y +
    #                                               random.random()), 1)

    # num_cleaned = room.get_num_cleaned_tiles()
    # if num_cleaned != width * height:
    #     print("Number of clean tiles", num_cleaned, "is incorrect: re-cleaning cleaned \
    #           tiles must not increase number of cleaned tiles")
    # else:
    #     print("Number of clean tiles", num_cleaned, "is correct: no incorrectly extra \
    #           clean tiles")
#
#
#
    """
    test_is_position_in_room:
        
    Test is_position_in_room.
    """
    # width, height, dirt_amount = (3, 4, 2)
    # room = ps3.RectangularRoom(width, height, dirt_amount)
    # solution_room = ps3.RectangularRoom(width, height, dirt_amount)

    # for x in [0.0, -0.1, width - 0.1, width, width + 0.1]:
    #     for y in [0.0, -0.1, height - 0.1, height, height + 0.1]:
    #         pos = ps3.Position(x, y)
    #         solutionRoomValidPosition = solution_room.is_position_in_room(pos)
    #         roomValidPosition = room.is_position_in_room(pos)
    #         if (solutionRoomValidPosition == roomValidPosition) and roomValidPosition:
    #             print("Pass: position ({}, {}) is a valid room position".
    #                   format(x, y))
    #         else:
    #             print("FAIL: POSITION ({}, {}) IS NOT IN THE ROOM!".
    #             format(x, y))
#
#
#
    """
    test_getset_robot_direction:

    Test get_robot_direction and set_robot_direction
    """
    # instantiate EmptyRoom from solutions for testing
    # width, height, dirt_amount = (3, 4, 2)
    # solution_room = ps3.EmptyRoom(width, height, dirt_amount)

    # robots = [ps3.Robot(solution_room, 1.0, 1) for i in range(4)]
    # directions = [1, 333, 105, 75, 74.3]
    # for dir_index, robot in enumerate(robots):
    #     robot.set_robot_direction(directions[dir_index])
    # for dir_index, robot in enumerate(robots):
    #     robot_dir = robot.get_robot_direction()
    #     if robot_dir == directions[dir_index]:
    #         print('Robot direction pointing correctly')
    #     else:
    #         print("Robot direction set or retrieved incorrectly:\
    #               expected {}, got {}".format(directions[dir_index],
    #               robot_dir))

    """
    test_get_random_position:

    Test get_random_position, checks for distribution of positions and validity
    of positions
    """
    # width, height, dirt_amount = (5, 10, 1)
    # room = ps3.EmptyRoom(width, height, dirt_amount)
    # sol_room = ps3.EmptyRoom(width, height, dirt_amount)
    # freq_buckets = {}
    # for i in range(50000):
    #     pos = room.get_random_position()
    #     # confirm from test that this is a valid position
    #     assert sol_room.is_position_valid(pos)
    #     try:
    #         x, y = pos.get_x(), pos.get_y()
    #     except AttributeError:
    #         print("get_random_position returned {} which is not a Position".
    #               format(pos))

    #     if not(0 <= x < width and 0 <= y < height):
    #         print("get_random_position returned {} which is not in [0, {}),\
    #               [0, {})".format(pos, width, height))
    #     # else:
    #     #     print('Position Width:', x, 'Position Height:', y)

    #     x0, y0 = int(x), int(y)
    #     freq_buckets[(x0, y0)] = freq_buckets.get((x0, y0), 0) + 1

    # bucketList = []
    # bucketind = []
    # i = 0
    # for t in xyrange(width, height):
    #     num_in_bucket = freq_buckets.get(t, 0)
    # #     #  This is a 99.7% confidence interval for a uniform
    # #     #  distribution. Fail if the total of any bucket falls outside
    # #     # this range.
    #     # print('Number in bucket {},{}: {}'.format(t[0], t[1], num_in_bucket))
    #     if not 865 < num_in_bucket < 1135:
    #         print("The distribution of positions from get_random_position \
    #               looks incorrect (it should be uniform (close to 1000) but \
    #                                 found {}".format(num_in_bucket))

# 
#
#
    """
    test_get_num_tiles:

    test get_num_tiles method
    """
    # for i in range(10):
    #     width, height, dirt_amount = (random.randint(1, 10),
    #                                   random.randint(1, 10), 1)
    #     room_num_tiles = ps3.EmptyRoom(width, height,
    #                                    dirt_amount).get_num_tiles()
    #     sol_room_tiles = ps3.EmptyRoom(width, height,
    #                                    dirt_amount).get_num_tiles()
    #     if room_num_tiles != sol_room_tiles:
    #         print("student code number of room tiles = {}, not equal to \
    #               solution code num tiles {}".format(room_num_tiles,
    #               sol_room_tiles))
    #     else:
    #         print("student code num of room tiles equals solution code num \
    #               tile {}".format(sol_room_tiles))
#
#
#
    """
    test_is_position_valid:

    Test is_position_valid this should be refactored as it's mostly a copy of
    is_position_in_room code
    """
    # width, height, dirt_amount = (3, 4, 2)
    # room = ps3.EmptyRoom(width, height, dirt_amount)
    # solution_room = ps3.EmptyRoom(width, height, dirt_amount)

    # for x in [0.0, -0.1, width - 0.1, width, width + 0.1]:
    #     for y in [0.0, -0.1, height - 0.1, height, height + 0.1]:
    #         pos = ps3.Position(x, y)
    #         if solution_room.is_position_valid(pos) != \
    #            room.is_position_in_room(pos):
    #             print("\nstudent code {} and solution code {} disagree on \
    #                       whether position is valid, with position {}".
    #                   format(solution_room.is_position_valid(pos),
    #                          room.is_position_in_room(pos), pos))
    #         else:
    #             print("\nstudent code and solution code agrees on whether \
    #                       position is valid {} with position {} {}".
    #                   format(solution_room.is_position_valid(pos), x, y))
#
#
#
    """
    test_is_tile_furnished:

    test is_tile_furnished
    """
    # print('New set of trials!')
    # for trial in range(5):
    #     print('\nTrial number: {}'.format(trial))
    #     width, height, dirt_amount = (random.randint(2, 8),
    #                                   random.randint(2, 8), 1)
    #     # create room using student's class, set furniture
    #     # tiles for solution class
    #     room = ps3.FurnishedRoom(width, height, dirt_amount)
    #     print('Room dimmensions are width {} and height {}'.
    #           format(width, height))
    #     room.add_furniture_to_room()
    #     print('Furniture dimensions and placement are:')
    #     print('  Furniture Width: {} and Furniture Height {}'.
    #           format(room.furniture_width, room.furniture_height))
    #     print('  Furniture Bottom Left Placement is: Width {} and Height {}\n'.
    #           format(room.f_bottom_left_x, room.f_bottom_left_y))
    #     # sol_room = ps3.FurnishedRoom(width, height, dirt_amount)
    #     # this relies on knowing the underlying details of the class
    #     # sol_room.furniture_tiles = room.furniture_tiles
    #     for x, y in xyrange(width, height):
    #         if room.is_tile_furnished(x, y) is True:
    #             print("Tile {} {} furnished".format(str(x), str(y)))
#
#
#
    """
    test_is_position_valid:

    Test is_position_valid
    """
    # print('New set of trials!')
    # for trial in range(5):
    #     print('\nTrial number: {}'.format(trial))
    #     width, height, dirt_amount = (3, 4, 2)
    #     room = ps3.FurnishedRoom(width, height, dirt_amount)
    #     print('Room dimmensions are width {} and height {}'.
    #           format(width, height))
    #     room.add_furniture_to_room()
    #     print('Furniture dimensions and placement are:')
    #     print('  Furniture Width: {} and Furniture Height {}'.
    #           format(room.furniture_width, room.furniture_height))
    #     print('  Furniture Bottom Left Placement is: Width {} and Height {}\n'.
    #           format(room.f_bottom_left_x, room.f_bottom_left_y))
    #     # sol_room = test.FurnishedRoom(width, height, dirt_amount)
    #     # sol_room.furniture_tiles = room.furniture_tiles 

    #     for x in [0.0, -0.1, width - 0.1, width, width + 0.1, room.f_bottom_left_x + 0.3]:
    #         for y in [0.0, -0.1, height - 0.1, height, height + 0.1, room.f_bottom_left_y + 0.3]:
    #             pos = ps3.Position(x, y)
    #             print('\nUsing {} with x: {} and y: {}'.format(pos, x, y))
    #             if(room.is_position_valid(pos)):
    #                 print('Position valid x: {} and y: {}'.format(x, y))
    #             else:
    #                 print('Position invalid x: {} and y: {}'.format(x, y))
#
#
#
    """
    test_get_num_tiles:

    test get_num_tiles method - should refactor - is mostly copy of EmptyRoom
    test
    # """
    # for i in range(10):
    #     width, height, dirt_amount = (random.randint(2,10), 
    #                                   random.randint(2,10), 1)
        # instanciate student's room
        # room = ps3.FurnishedRoom(width, height, dirt_amount)
        # room.add_furniture_to_room()
        # instanciate solution's room based on student's furniture
        # sol_room = ps3.FurnishedRoom(width, height, dirt_amount)
        # sol_room.furniture_tiles = room.furniture_tiles 
        # generate answers
        # room_num_tiles = room.get_num_tiles()
        # sol_room_num_tiles = sol_room.get_num_tiles()
        # self.assertEquals(room_num_tiles, sol_room_num_tiles,
        #                  "student code number of room tiles = {}, not equal to solution code num tiles {}".format(room_num_tiles, sol_room_num_tiles)
        #                  )
        # print('Number of valid tiles is: {} with width {} and height {}'.
        #       format(room_num_tiles, width, height))
        # print('Furniture was x: {} and y: {}\n'.format(room.furniture_width,
        #                                              room.furniture_height))
#
#
#
    """
    test_get_random_position(self):

    Test get_random_position for FurnishedRoom tests for validity of positions - could add distribution checking 
    similar to empty room
    """
    # width, height, dirt_amount = (5, 10, 1)
    #  Create a Width x Height Results Matix (using lists)
    # positions = [[0] * height for i in range(width)]
    # instanciate student's room
    # room = ps3.FurnishedRoom(width, height, dirt_amount)
    # room.add_furniture_to_room()
    # instanciate solution's room based on student's furniture
    # sol_room = ps3.FurnishedRoom(width, height, dirt_amount)
    # sol_room.furniture_tiles = room.furniture_tiles
    # for i in range(1000000):
    #     pos = room.get_random_position()
        # print('Random position: x: {} y: {}'.format(pos.x, pos.y))
    #     positions[math.floor(pos.get_x())][math.floor(pos.get_y())] += 1
    # print('Positions Results:')
    # print('Furniture Size: height = {} width = {}'.format(room.furniture_height,
    #                                                       room.furniture_width))
    # print('Furniture Position: height = {} width = {}'.format(room.f_bottom_left_x,
    #                                                       room.f_bottom_left_y))
    # for i in range(width):
    #     print('Column {}: {}'.format(i, positions[i]))
#
#
#
    """
    createRoomAndRobots(num_robots)
    """
def createRoomAndRobots(num_robots):
#   Create common room
    room = ps3.EmptyRoom(5, 7, 1)

#  Create robots
    speed = 1.0
    capacity = 1
    robots = [ps3.StandardRobot(room, speed, capacity) for i in range(num_robots)]
    return room, robots
    
    "Test strict inequalities in random positions for the EmptyRoom and StandardRobot"
# for m in range(70000):
#     # robots = [ps3.StandardRobot(room, speed, capacity) for i in range(num_robots)]
#     r, robots = createRoomAndRobots(4)
#     for robot in robots:
#         r_position = robot.get_robot_position()
#         r_direction = robot.get_robot_direction()
#         try:
#             x, y = r_position.get_x(), r_position.get_y()
#         except AttributeError: 
#             print("get_robot_position returned %r which is not a Position"
#                       % (r_position,))
#             exit(-1)
#         if not (x < 5 and y < 7):
#             print("Robot position was set to %r which is not in [0, 5), [0, 7)" %
#                         ((r_position.get_x(), r_position.get_y()),))
#             exit(-1)
#         else:
#             print("Robot position: x: {} y: {}".format(x, y))

#         if not (0 <= r_direction < 360):
#             print("Robot direction was set to %r, which is not in [0, 360)"
#                   % (r_direction,))
#             exit(-1)

"""
testRobot:
Test StandardRobot
"""
# pos_buckets = {}
# dir_buckets = {}
# skip_pos_distribution_test = False
# for m in range(7000):
#     r, robots = createRoomAndRobots(4)
#     for robot in robots:
#         r_position = robot.get_robot_position()
#         r_direction = robot.get_robot_direction()
#         try:
#             x, y = r_position.get_x(), r_position.get_y()
#         except AttributeError: 
#             print("get_robot_position returned %r which is not a Position"
#                       % (r_position,))
#             exit(-1)
#         if not (x < float(5) and y < float(7)):
#             print("Robot position was set to %r which is not in [0, 5), [0, 7)" %
#                         ((r_position.get_x(), r_position.get_y()),))
#             exit(-1)
        # else:
        #     print("Robot position: x: {} y: {}".format(x, y))

    #     if not (float(0) <= r_direction < float(360)):
    #         print("Robot direction was set to %r, which is not in [0, 360)"
    #               % (r_direction,))
    #         exit(-1)

    # x0, y0 = int(r_position.get_x()), int(r_position.get_y())
    # pos_buckets[(x0, y0)] = pos_buckets.get((x0, y0), 0) + 1
    # dir_buckets[int(r_direction)] = \
    #   dir_buckets.get(int(r_direction), 0) + 1
# Test that positions are correctly distributed
# if not skip_pos_distribution_test:
#     for t in xyrange(5, 7):
#         num_in_bucket = pos_buckets.get(t, 0)
#         # self.assertTrue(
#         if not 685 < num_in_bucket < 915:
#             # 685 < num_in_bucket < 915,
#             print("The distribution of positions on new Robot objects \
# looks incorrect for bucket: {} having {} positions".format(t, num_in_bucket))
#         else:
#             print("The distribution of positions on new Robot objects \
#                   looks correct with number in bucket # {} is {}".
#                   format(t, num_in_bucket))
            
# # Test that directions are correctly distributed
#     for t in range(360):
#         num_in_bucket = dir_buckets.get(t, 0)
#         # self.assertTrue(
#         if not 658 < num_in_bucket < 898:
#             print("The distribution of directions on new Robot objects \
# looks incorrect for bucket: {} having {} directions".format(t, num_in_bucket))
#             # print("The distribution of positions from get_random_position \
#               # looks incorrect (it should be uniform)")
#         else:
#             print("The distribution of directions on new Robot objects \
#                   looks correct with number in bucket # {} is {}".
#                   format(t, num_in_bucket))
#
#
#
"""
test_update_position_and_cleanStandardRobot

Test StandardRobot.update_position_and_clean
"""
width = 5
height = 5
dirtAmount = 1
room = ps3.EmptyRoom(width, height, dirtAmount)
# room = ps3.FurnishedRoom(width, height, dirtAmount)
# room.add_furniture_to_room()

speed = 1.0
capacity = 1
robots = []
# Ask how many robots to deploy
numRobots = int(input("Enter number of robots to deploy: "))

#  Create the robots
for i in range(numRobots):
    # robots.append(ps3.StandardRobot(room, speed, capacity, i))
    robots.append(ps3.FaultyRobot(room, speed, capacity, i))
    
# robot.set_robot_position(ps3.Position(1.5, 2.5))
# robot.set_robot_direction(90)
# robot.update_position_and_clean()
# if robot.get_robot_direction() != 90.0:
#     print("Robot direction is updated incorrectly by update_position_and_clean: expected %r, got %r" %
#                   (90, robot.get_robot_direction()))
# else:
#     print("Robot correctly made its first step. {} Direction: {}".format(robot.get_robot_position(), robot.get_robot_direction()))

#  check if robot position is valid
# robotPos = robot.get_robot_position()
# correctPos = ps3.Position(2.5, 2.5)
# if robotPos.get_x() != correctPos.get_x() and robotPos.get_y() != correctPos.get_y():
#     print("Robot position is updated incorrectly by update_position_and_clean: expected %r, got %r" %
#                   (ps3.Position(2.5, 2.5), robot.get_robot_position()))
# else:
#     print("Robot position is updated correctly. New Position is {}".format(robot.get_robot_position()))

# if not 2 >= room.get_num_cleaned_tiles() >= 1:
#     print("update_position_and_clean should have marked one or two tiles as clean")
# else:
#     print("update_position_and_clean did mark {} tile(s) clean".format(room.get_num_cleaned_tiles()))

# tile1, tile2 = room.is_tile_cleaned(1, 2), room.is_tile_cleaned(2, 2)
# if not (tile1 or tile2 ):
#     print("update_position_and_clean should have marked either (1, 2) or (2, 2) as clean")
# elif tile1:
#     print("update_position_and_clean has marked tile(1, 2) as clean") 
# else:
#     print("update_position_and_clean has marked tile(2, 2) as clean")
 
# # Simulate a lot of time passing...
for i in range(20000):
    if not (robots[0].is_robot_finished()):
        print("\nStep number: {}".format(i))
        for j in range(numRobots):
            robots[j].update_position_and_clean()
            if not robots[j]._room.is_position_in_room(robots[j].get_robot_position()):
                print("Robot #{} position {} is not in room!".format(j,robots[j].get_robot_position()))
            # else:
            #     print("Robot #{} {} is within room".format(j, robots[j].get_robot_position()))
    else:
        print('Robots finished cleaning room! In {} steps.'.format(i))
        # print('Furniture dimensions and placement are:')
        # print('  Furniture Width: {} and Furniture Height {}'.
        #       format(room.furniture_width, room.furniture_height))
        # print('  Furniture Bottom Left Placement is: Width {} and Height {}\n'.
        #       format(room.f_bottom_left_x, room.f_bottom_left_y))
        break
#     self.assertTrue(r.is_position_in_room(robot.get_robot_position()),
#                     "Robot position %r is not in room!" % (robot.get_robot_position(),))

# self.assertNotEquals(robot.get_robot_direction(), 90,
#                   "Robot direction should have been changed in update_position_and_clean")
# self.assertTrue(r.get_num_cleaned_tiles() >= 1,
#                 "update_position_and_clean should have marked another tile as clean")
