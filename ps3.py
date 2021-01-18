# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name: Clarke Homan
# Collaborators (discussion):
# Starting Date: December 18, 2020
# Ending Date: January 18, 2021

import math
import random

import ps3_visualize
import pylab

# For python 2.7:
# from ps3_verify_movement27 import test_robot_movement


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.

    where the coordinates are given by floats (x, y).
    """

    def __init__(self, x, y):
        """
        Position object constructor that initializes with coordinates (x, y).

        Args:
            x (float): Position's x component (Height).
            y (float): Position's y component (Width).

        Returns
        -------
            None.

        """
        self.x = float(x)
        self.y = float(y)

    def get_x(self):
        """Return position object's x component (as a float)."""
        return self.x

    def get_y(self):
        """Return position object's y component (as a float)."""
        return self.y

    def get_new_position(self, angle, speed):
        """
        Compute and return the new Position after a single clock-tick.

        After clock tick, with this object as the current position, and with
        the specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()

        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))

        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y

        return Position(new_x, new_y)

    def __str__(self):
        """
        Return string that describes a Position object.

        Returns
        -------
            string: String ready for printing.

        """
        return "Position: " + str(math.floor(self.x)) + ", " + \
            str(math.floor(self.y))

# Constants (semi) used to index into tile's dictionary elements. Never
# overwritten. Too bad python doesn't support the 'const' keyword like
# other languages. It should.


CONST_TILE_POS_IND = 0
CONST_TILE_AMT_DIRT_IND = 1
CONST_TILE_CLEANED_IND = 2
CONST_TILE_CLEANED = 0


class Tile(object):
    """Class definition for tile object."""

    _tileNum = 0

    def __init__(self, center, dirtAmount, tileCleaned=False):
        """
        Tile class constructor.

        Args:
            center (list): width-height position center of tile expressed as
              list of floats (width-height)
            dirtAmount (int): initial amount of dirt on tile to clean
            tileCleaned (Boolean, optional): Set when tile is cleaned.
              Defaults to False.

        Returns
        -------
            None.

        """
        if type(center) != list:
            raise TypeError('Center must be a 2 element list of floats')
        if len(center) != 2:
            raise TypeError('Center must be a 2 element float array')
        if center[0] < 0.0 or center[1] < 0.0:
            raise ValueError('Elements of center must be < 0.0')
        self.center = center

        if type(dirtAmount) != int:
            raise TypeError('DirtAmount must be an int')
        if dirtAmount < 0:
            raise ValueError('Dirt amount must be >= 0')
        self.dirtAmount = dirtAmount

        self.tileCleaned = tileCleaned

        self.tileNum = Tile._tileNum
        Tile._tileNum += 1

    def setCenter(self, center):
        """
        Set tile's center position.

        Args:
            center (list): width-height position center of tile expressed as
              list of floats (width-height)

        Returns
        -------
            tileCenter (list): tile's updated center

        """
        if type(center) != list:
            raise TypeError('Center must be a 2 element list of floats')
        if len(center) != 2:
            raise TypeError('Center must be a 2 element float array')
        if center[0] < 0.0 or center[1] < 0.0:
            raise ValueError('Elements of center must be < 0.0')
        self.center = center

        return self.center

    def getCenter(self):
        """
        Fetch tile's center position.

        Returns
        -------
            center (Position): tile's center position (as a Position object)

        """
        return self.center

    def setDirtAmount(self, dirtAmount):
        """
        Set tile's current dirt amount (overwrite).

        Args:
            dirtAmount (int): amount of dirt on tile

        Returns
        -------
            None.

        """
        if type(dirtAmount) != int:
            raise TypeError('DirtAmount must be an int')
        if dirtAmount < 0:
            raise ValueError('Dirt amount must be >= 0')
        self.dirtAmount = dirtAmount
        self.tileCleaned = False

        return self.dirtAmount

    def removeDirtAmount(self, dirtAmount):
        """
        Remove dirtAmount from tile, floor 0.

        If updated dirt amount is <= 0, tile's dirt amount will be set to 0
        and tile's tileCleaned status variable set to True.

        Args:
            dirtAmount (int): Amount of dirt to be cleaned from tile.

        Returns
        -------
            self.dirtAmount

        """
        if dirtAmount >= 0:
            self.dirtAmount -= dirtAmount

        if dirtAmount < 0:
            self.dirtAmount += -dirtAmount

        if self.dirtAmount <= 0:
            self.dirtAmount = 0
            self.tileCleaned = True
        else:
            self.tileCleaned = False

        return self.dirtAmount

    def getDirtAmount(self):
        """
        Fetch tile's current dirt amount.

        Returns
        -------
            dirtAmount (int): current dirt amount on tile

        """
        return self.dirtAmount

    def setTileCleaned(self):
        """
        Set tile's tileCleaned flag to False and sets tile's dirt amount to 0.

        Returns
        -------
            None.

        """
        self.tileCleaned = True
        self.dirtAmount = 0

    def getIsTileCleaned(self):
        """
        Set tile's tileCleaned flag state.

        Returns
        -------
            None.

        """
        return self.tileCleaned

    def getTileNumber(self):
        """
        Get tile's internal number.

        Returns
        -------
            tileNumber

        """
        return self.tileNum

    def __str__(self):
        """
        Return printable description of tile.

        Returns
        -------
            string: String description of tile

        """
        printString = 'Tile: Center: ' + str(self.center) + ' Dirt Amount: ' \
            + str(self.dirtAmount) + 'Tile Cleaned: ' + str(self.tileCleaned)
        return printString


# === Problem 1
class RectangularRoom(object):
    """
    RectangularRoom models rectangular room containing clean or dirty tiles.

    A room has a width and a height and contains (width * height) tiles.
    Each tile has some fixed amount of dirt. The tile is considered clean only
    when the amount of dirt on this tile is 0.
    """

    def __init__(self, width, height, dirt_amount):
        """
        Initialize a rectangular room with width, height, and dirt_amount \
        dirt_amount on each tile.

        RectangularRoom contains dictionary of square room tiles indexed by
        the tuple (x,y), where 'x' identifies the height position of the tile.
        The 'y' component identifies the width position of the tile.

        Args:
            width (int): Room width dimension in tiles (> 0)
            height (int): Room height dimension in tiles (> 0)
            dirt_amount (int): Initial amount of dirt on each tile when room \
                created (>= 0)

        Raises
        ------
            ValueError: If either width, height or dirt_amount given incorrect
            starting values.

        Returns
        -------
            None.

        """
        if ((width < 1) or (height < 1) or (dirt_amount < 0)):
            raise ValueError('Either width or height or dirt amount are not \
                             appropriate value!')
        self.width = width
        self.height = height
        self.dirt_amount = dirt_amount
        self.tiles = {}
        # tileNum = 0
        for heightInd in range(self.height):
            for widthInd in range(self.width):
                tile = Tile([widthInd+0.5, heightInd+0.5], self.dirt_amount,
                            False)
                self.tiles[widthInd, heightInd] = tile
        # raise NotImplementedError

    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it
              as 0.


        Args
        ----
            pos (class): x-y position objectlocating tile to be cleaned.
            capacity (int): the amount of dirt to be cleaned in a single
                            time-step. Can be negative which would mean adding
                            dirt to the tile
        Returns
        -------
            tileUpdated which is True is tile is found and updated.
            False is tile not found and not updated (because cleaned already)
        """
        # Get the X nd Y coordinates of the position of interest
        posX = pos.get_x()
        if posX > self.width:
            errorStr = 'Position exceeds room width! ' + str(posX) + \
                ' Width Limit: ' + str(self.width)
            raise ValueError(errorStr)

        posY = pos.get_y()
        if posY > self.height:
            raise ValueError('Position exceeds room height!')

        # Loop thru each of the room tiles to compare the position of interest
        # with the tile's position. If the tile's center position is within
        # 1/2 tile's width and height from the position of interest's x and y
        # position, the the tile is considered 'under' the position of
        # interest.
        for widthInd in range(self.width):
            for heightInd in range(self.height):
                # Get the tile's height pos
                tileX = self.tiles[widthInd, heightInd].getCenter()[0]
                # Get the tile's width pos
                tileY = self.tiles[widthInd, heightInd].getCenter()[1]
                # Determine if robot's X-Y position is within abs(0.5) squares
                # of the current tile's center to identify the tile it is over.
                if abs(tileY - posY) <= 0.5:
                    if abs(tileX - posX) <= 0.5:
                        self.tiles[widthInd, heightInd].removeDirtAmount(capacity)
                        return True  # did something, return this status
        # raise NotImplementedError

    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m (integer): queried tile's height position component
        n (integer): queried tile's width position component

        Raises
        ------
            ValueError: If either m (height) or n (width) reference a
            tile position not in room.

        Returns
        -------
            True if the tile (n, m) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        if m > self.width or type(m) != int:
            raise ValueError('Position exceeds room width or invalid type!')
        if n > self.height or type(n) != int:
            raise ValueError('Position exceeds room height or invalid type!')

        if (self.tiles[m, n].getDirtAmount() == 0) and \
           (self.tiles[m, n].getIsTileCleaned()):
            return True  # Tile is clean
        else:
            return False  # Tile is not clean, some amount of dirt remains

    def get_num_cleaned_tiles(self):
        """
        Count and return the number of tiles cleaned in room.

        Returns
        -------
            numTilesCleaned (int): the total number of clean tiles in the room

        """
        numTilesCleaned = 0
        #
        #  Loop thru all of the tiles and look at the dirt amount of each tile.
        #  If the tile is clean (no dirt), then add it to the running count.
        for i in range(self.width):
            for j in range(self.height):
                if (self.tiles[i, j].getIsTileCleaned()) and \
                   (self.tiles[i, j].getDirtAmount() == 0):
                    numTilesCleaned += 1

        return numTilesCleaned
        # raise NotImplementedError

    def is_position_in_room(self, pos):
        """
        Determine if pos is inside the room.

        pos (Position object): position being determined to be in the room

        Returns
        -------
            True if pos is in the room, False otherwise.
        """
        #
        #  Look to see if the X and Y components of a position object
        #  lies within the room's overall height and width constraints.
        #  If both components within room, return True. Otherwise, return
        #  default of False
        #
        inRoom = False
        posX = pos.get_x()
        if (posX < self.width) and (posX >= 0.0):
            posY = pos.get_y()
            if (posY < self.height) and (posY >= 0.0):
                inRoom = True

        return inRoom

    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n).

        Assumes that (m, n) represents a valid tile inside the room.

        m (int): height location component of tile
        n (int): width location component of tile

        Returns
        -------
            dirtAmount (int): Amount of dirt on tile
        """
        pos = Position(m, n)
        if self.is_position_in_room(pos):
            dirtAmount = self.tiles[m, n].getDirtAmount()

        return dirtAmount
        # raise NotImplementedError

    def get_tile_center(self, pos):
        """
        Return the position of center of designated tile at position pos.

        Assumes that pos represents a valid tile inside the room.

        pos (Position): position of tile

        Returns
        -------
            center (list): Center of tile ()
        """
        if self.is_position_in_room(pos):
            m = pos.get_x()
            n = pos.get_y()
            center = self.tiles[m, n].getCenter()

        return center

    def get_random_direction(self):
        """
        Return a randomly generated drection value.

        Direction is ranged checked 0.0 <= direction < 360.0.

        Returns
        -------
            direction (float): float within range of 0.0 <= direction < 360.0

        """
        direction = float(random.uniform(0.0, 360.0))
        return direction

        # raise NotImplementedError

    def get_num_tiles(self):
        """Return numTiles (int) the total number of tiles in the room."""
        # do not change -- implement in subclasses.
        raise NotImplementedError

    def is_position_valid(self, pos):
        """
        pos: a Position object.

        returns: True if pos is in the room and (in the case of FurnishedRoom)
                 if position is unfurnished, False otherwise.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

    def get_random_position(self):
        """Return a Position object; a random position inside the room."""
        # do not change -- implement in subclasses
        raise NotImplementedError


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    Always the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    #
    #  Class variable isRoomDefined, which is shared with all instances of 
    #  Robot class. Since there can be multiple instances of Robot sharing a
    #  common room. Room initially gets set with a dummy room, but then gets reset with
    #  the supplied room when the first robot is instaniated. A robot instance
    #  'knows' they are the first by checking the roomAlreadyDefined class
    #  variable. If False, then they overwrite the room variable when created
    #  and set the roomAlreadyDefined variable to True. That way, a subsequent
    #  robot instance doesn't clobber the room already in play.
    #
    _isRoomDefined = False
    _room = None

    @classmethod
    def isRoomDefined(cls):
        """
        Returns the isRoomDefined class variable status.

        Args:
            cls (robot class): DESCRIPTION.

        Returns:
            isRoomDefined (boolean): isRoomDefined for class (True or False)

        """
        return cls._isRoomDefined

    @classmethod
    def setRoomDefined(cls, room):
        """
        Set class Robot's room class variable _isRoomDefined to True

        Set class Robot's room object.

        Args:
            cls (TYPE): DESCRIPTION.

        Returns:
            None.

        """
        cls._isRoomDefined = True
        cls._room = room
    
    def __init__(self, room, speed, capacity, robotNum=0):
        """
        Robot object constructor with a speed and cleaning capacity in a room.

        The robot initially has a random direction and position in the room.

        Args:
            room (RectangularRoom object): DESCRIPTION.
            speed (float): nominal speed which the robot moves at (> 0.0)
            capacity (int): the amount of dirt cleaned by the robot
                  in a single time-step
            robotNum (int): robot instance number (defaults to 0)

        Raises
        ------
            NotImplementedError: DESCRIPTION.

        Returns
        -------
            None.

        """
        #
        #  Initialize instance data attributes of robot
        #
        if type(speed) != float:
            raise ValueError('Speed must be a float')
        if speed <= 0.0:
            raise ValueError('Speed must be greater than 0.0')
        self.speed = speed

        if capacity < 1:
            raise ValueError('Capacity must be greater than 0')
        self.capacity = capacity

        self.robotNum = robotNum


        if not Robot.isRoomDefined():
            Robot.setRoomDefined(room)

    #
    #  Each robot's instance has an initial random position within the room.
    #
        self.position = self._room.get_random_position()

    #
    #  Each robot instance has an initial direction (attitude) expressed as a
    #  float in degrees.
    #
        self.direction = self._room.get_random_direction()
        # raise NotImplementedError

    def get_robot_position(self):
        """
        Return robot instance's current position.

        Returns
        -------
            self.Position (Position): robot's current position

        """
        return self.position
        # raise NotImplementedError

    def get_robot_direction(self):
        """
        Return robot instance's current direction.

        Returns
        -------
            self.direction (float): giving the direction of the robot as an
            angle in degrees, 0.0 <= d < 360.0.

        """
        return self.direction
        # raise NotImplementedError

    def set_robot_position(self, position):
        """
        Set the position of the robot to position.

        Args:
            position (Position): position to set robot to

        Returns
        -------
            None.

        """
        if type(position) != Position:
            raise TypeError("Can't set robot posiiton using non-position data")
        
        if self._room.is_position_valid(position):
            self.position = position
        # raise NotImplementedError

    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.

        Direction is ranged checked 0.0 <= direction < 360.0. If direction >
        360.0, direction is converted to float wihtin 0.0 <= d < 360. If
        direction is given as a negative float, raise ValueError.

        Args:
            direction (float): direction (attitude) of robot's new direction,
            referenced from 0.0 degrees North

        Returns
        -------
            None.

        """
        _North = 0.0
        fdirection = float(direction)
        if fdirection < _North:
            raise ValueError('Direction must be provided as a positive value')

        if fdirection >= 360.0:
            fdirection = fdirection % 360.0

        self.direction = fdirection
        # raise NotImplementedError

    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is
        invalid, rotate once to a random new direction, and stay stationary)
        and mark the tile it is on as having been cleaned by capacity amount.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError


# === Problem 2
class EmptyRoom(RectangularRoom):
    """An EmptyRoom represents a RectangularRoom with no furniture."""

    def get_num_tiles(self):
        """Return an integer; the total number of tiles in the room."""
        numTiles = len(self.tiles)
        if numTiles > 0:
            return numTiles
        else:
            raise ValueError('Room number of tiles not defined')
        # raise NotImplementedError

    def is_position_valid(self, pos):
        """
        pos: a Position object.

        Returns: True if pos is in the room, False otherwise.
        """
        if type(pos) != Position:
            raise TypeError("Position 'pos' not within room dimensions.")

        # extract the width and height components of position
        isPosValid = self.is_position_in_room(pos)
        return isPosValid
        # raise NotImplementedError

    def get_random_position(self):
        """
        Return a randomly generated Position object.

        Position object has a valid position (inside the room).
        """
        #
        # Generate the position (both width and height dimensions) fudge
        # factors that pick a random poition within a selected tile.
        #
        posWidth = float(random.randint(0, self.width - 1)) + random.random()
        posHeight = float(random.randint(0, self.height - 1)) + random.random()

        #
        #  If the generated position coordinates are within the 'room'
        #  dimensions, return the Position object. Else, complain with a
        #  raised ValueError.
        #
        pos = Position(posWidth, posHeight)
        if self.is_position_in_room(pos):
            return pos
        else:
            raise ValueError('Invalid position generated')
            
        # raise NotImplementedError

    def is_room_cleaned(self):
        """
        Return the status (True or False) of the room being cleaned.
        
        All tiles report being cleaned

        Returns:
            isRoomCleaned (bool): all tiles in room report being cleaned

        """
        if self.get_num_cleaned_tiles() == self.get_num_tiles():
            isRoomCleaned = True
        else:
            isRoomCleaned = False
        return isRoomCleaned

        # raise NotImplementedError
class FurnishedTile(Tile):
    """
    A furnished tile inherits all of the properties and methods of its base
    class Tile, but adds the additional property (and related methods) to
    indicate the tile has furniture in it.
    """
    def __init__(self, center, dirtAmount, tileCleaned=False,
                 hasFurniture=False):
        """
        Initializes a FurnishedTile, a subclass of Tile. FurnishedTile also
        includes the property of hasFurniture (Boolean) that indicates whether
        the tile has a stick of furniture within it.

        Args:
            center (list): width-height position center of tile expressed as
              list of floats (width-height)
            dirtAmount (int): amount of dirt initally on tile
            tileCleaned (bool, optional): DESCRIPTION. Defaults to False.
            hasFurniture (bool, optional): indicates if furniture on
              tile. Defaults to False

        Returns:
            None.

        """
        Tile.__init__(self, center, dirtAmount)
        self.hasFurniture = hasFurniture

    def getHasFurniture(self):
        """Return the value off tile's hasFurniture propoerty."""
        return self.hasFurniture

    def setHasFurniture(self, hasFurniture):
        """
        Set tile's hasFurniture property.

        Args:
            hasFurniture (Boolean): DESCRIPTION.

        Returns
        -------
            Current value of tile's hasFurniture property.

        """
        if type(hasFurniture) != bool:
            raise TypeError('setHasFurniture method: hasFurniture must be a \
                            boolean')
        self.hasFurniture = hasFurniture

class FurnishedRoom(RectangularRoom):
    """
    A FurnishedRoom represents a RectangularRoom with a rectangular piece of 
    furniture. The robot should not be able to land on these furniture tiles.
    """
    def __init__(self, width, height, dirt_amount):
        """ 
        Initializes a FurnishedRoom, a subclass of RectangularRoom. FurnishedRoom
        also has a list of tiles which are furnished (furniture_tiles).
        """
        # This __init__ method is implemented for you -- do not change.
        
        # Call the __init__ method for the parent class
        # RectangularRoom.__init__(self, width, height, dirt_amount)
        # Adds the data structure to contain the list of furnished tiles
        # self.furniture_tiles = []
        if ((width < 1) or (height < 1) or (dirt_amount < 0)):
            raise ValueError('Either width or height or dirt amount are not \
                             appropriate value!')
        self.width = width
        self.height = height
        self.dirt_amount = dirt_amount
        self.tiles = {}
        # tileNum = 0
        for heightInd in range(self.height):
            for widthInd in range(self.width):
                tile = FurnishedTile([widthInd+0.5, heightInd+0.5],
                                     self.dirt_amount)
                self.tiles[widthInd, heightInd] = tile

        #
        #  Furniture Placement Paramters
        #
        self.furniture_width = 0
        self.furniture_height = 0
        self.f_bottom_left_x = 0
        self.f_bottom_left_y = 0
        self.num_furnished_tiles = 0

    def is_room_cleaned(self):
        """
        Return the status (True or False) of the furnished room being cleaned.
        
        All unfurninshed tiles report being cleaned

        Returns:
            isRoomCleaned (bool): all tiles in room report being cleaned

        """
        if self.get_num_cleaned_tiles() == self.get_num_tiles():
            isRoomCleaned = True
        else:
            isRoomCleaned = False
        return isRoomCleaned

    def add_furniture_to_room(self):
        """
        Add a rectangular piece of furniture to the room.

        Each tile that contains a piece of the furniture will have its
        hasFurniture property set.

        A single piece of furniture added to the room will have its location
        and size is randomly selected. Width and height of the furniture piece
        is randomly selected so that the piece of furniture fits within the
        room and does not occupy the entire room. THE furniture's position is
        selected by randomly determining the location of the bottom left corner
        of the piece of furniture so that the entire piece of furniture lies
        within the room.
        """
        #
        # This addFurnitureToRoom method is implemented for you.
        # Do not change it.
        #
        # Generate the size (both width and length) of the furniture. The
        # furniture size cannot exceed the room's width and height
        #
        self.furniture_width = random.randint(1, self.width - 1)
        self.furniture_height = random.randint(1, self.height - 1)

        # Randomly choose bottom left corner of the furniture item.
        self.f_bottom_left_x = random.randint(0, self.width -
                                              self.furniture_width)
        self.f_bottom_left_y = random.randint(0, self.height -
                                              self.furniture_height)

        # Fill list with tuples of furniture tiles.
        for i in range(self.f_bottom_left_x, self.f_bottom_left_x +
                       self.furniture_width):
            for j in range(self.f_bottom_left_y, self.f_bottom_left_y +
                           self.furniture_height):
                self.tiles[i, j].setHasFurniture(True)
                self.num_furnished_tiles += 1

    def is_tile_furnished(self, m, n):
        """Return True if tile (m, n) is furnished."""
        # hasFurniture = False
        hasFurniture = self.is_position_valid(Position(m, n))
        # hasFurniture = self.tiles[m, n].getHasFurniture()
        return hasFurniture
        # raise NotImplementedError

    def is_position_furnished(self, pos):
        """
        Determine pos valid and returns True if furnished and False otherwise.

        Args
        ----
            pos: a Position object.

        Returns True if pos is furnished and False otherwise
        """
        #
        # Use math.floor() to guarantee integer tile numbers rounded downwards
        #
        hasFurniture = self.tiles[math.floor(pos.get_x()),
                                  math.floor(pos.get_y())].getHasFurniture()
        return hasFurniture

        # raise NotImplementedError

    def is_position_valid(self, pos):
        """
        Determine if position is valid and unfurnished.

        Args
        ----
            pos (Position): A position to be determined if unfurnished

        Returns
        -------
            isValid (bool): set True if position is valid and unfurnished

        """
        if self.is_position_in_room(pos):
            return not self.is_position_furnished(pos)
        else:
            return False
        # raise NotImplementedError

    def get_num_tiles(self):
        """
        Provide total number of valid tiles in room that are unfurnished.

        Returns
        -------
            numTiles (int): total number of tiles in the room that are
            unfurnished

        """
        numTiles = 0
        #
        #  searching thru each tile within the room, using the
        #  is_position_valid() method to determine if the tile is valid
        #  and unfurnished. If valid, add the tile to the count.
        #  return the overall count.
        #
        for width in range(self.width):
            for height in range(self.height):
                pos = Position(width, height)
                if self.is_position_valid(pos):
                    numTiles += 1
        return numTiles
        # raise NotImplementedError

    def get_random_position(self):
        """
        Find a valid position that is within a unfurnished tile.

        Returns
        -------
            None.

        """
        #
        # Generate the position (both width and height dimensions) fudge
        # factors that pick a random poition within a selected tile.
        #
        while True:
            posWidth = float(random.randint(0, self.width - 1)) + \
                random.random()
            posHeight = float(random.randint(0, self.height - 1)) + \
                random.random()

            pos = Position(posWidth, posHeight)
            if self.is_position_valid(pos):
                return pos

        #
        #  If the generated position coordinates are within the 'room'
        #  dimensions, return the Position object. Else, complain with a
        #  raised ValueError.
        # raise NotImplementedError

# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall or furtniture, it *instead*
    chooses a new direction randomly.
    """
    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is
        invalid, rotate once to a random new direction, and stay stationary)
        and clean the dirt on the tile by its given capacity.
        """
        pos = self.position  # get current position

        # use Position class's get_new_position to determine new position
        # given robot's current position and direction.
        pos = pos.get_new_position(self.direction, self.speed)

        if self._room.is_position_valid(pos):
            self.set_robot_position(pos)
            priorCleanedState = self._room.is_tile_cleaned(int(pos.x),
                                                           int(pos.y))
            self._room.clean_tile_at_position(self.get_robot_position(),
                                              self.capacity)
            if self._room.is_tile_cleaned(int(pos.x), int(pos.y)) != \
               priorCleanedState:
                print('Robot # {} cleaned tile at {}'.format(self.robotNum,
                                                             pos))
        else:
            # cycle thru random directions until a new direction is proposed
            direction = self._room.get_random_direction()
            while direction == self.get_robot_direction():
                direction = self.get_random_direction()
            self.set_robot_direction(direction)

        # raise NotImplementedError

    def is_robot_finished(self):
        """Return whether the robot has cleaned the room."""
        if self._room.is_room_cleaned():
            return True
        else:
            return False

# Uncomment this line to see your implementation of StandardRobot in action!
# test_robot_movement(StandardRobot, EmptyRoom)
# test_robot_movement(StandardRobot, FurnishedRoom)

# === Problem 4
class FaultyRobot(Robot):
    """
    A FaultyRobot is a robot that will not clean the tile it moves to and
    pick a new, random direction for itself with probability p rather
    than simply cleaning the tile it moves to.
    """
    p = 0.15

    @staticmethod
    def set_faulty_probability(prob):
        """
        Set the probability of getting faulty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        FaultyRobot.p = prob

    def gets_faulty(self):
        """
        Determine if this FaultyRobot get faulty at this timestep.

        A FaultyRobot gets faulty with probability p.

        returns: True if the FaultyRobot gets faulty, False otherwise.
        """
        return random.random() < FaultyRobot.p

    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.

        Check if the robot gets faulty. If the robot gets faulty,
        do not clean the current tile and change its direction randomly.

        If the robot does not get faulty, the robot should behave like
        StandardRobot at this time-step (checking if it can move to a new
        position, move there if it can, pick a new direction and stay
        stationary if it can't)
        """
        pos = self.position  # get current position

        # use Position class's get_new_position to determine new position
        # given robot's current position and direction.
        pos = pos.get_new_position(self.direction, self.speed)
        isFaulty = self.gets_faulty()
        if isFaulty:
            print('Faulty Robot at position {}'.format(pos))

        if self._room.is_position_valid(pos) and not isFaulty:
            self.set_robot_position(pos)
            priorCleanedState = self._room.is_tile_cleaned(int(pos.x),
                                                           int(pos.y))
            self._room.clean_tile_at_position(self.get_robot_position(),
                                              self.capacity)
            if self._room.is_tile_cleaned(int(pos.x), int(pos.y)) != \
               priorCleanedState:
                print('Robot # {} cleaned tile at {}'.format(self.robotNum,
                                                             pos))
        else:
            # cycle thru random directions until a new direction is proposed
            direction = self._room.get_random_direction()
            while direction == self.get_robot_direction():
                direction = self.get_random_direction()
            self.set_robot_direction(direction)

        # raise NotImplementedError
    def is_robot_finished(self):
        """Return whether the robot has cleaned the room."""
        if self._room.is_room_cleaned():
            return True
        else:
            return False


#test_robot_movement(FaultyRobot, EmptyRoom)

# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each       
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile.
    
    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    capacity: an int (capacity >0)
    width: an int (width > 0)
    height: an int (height > 0)
    dirt_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                FaultyRobot)
    """
    raise NotImplementedError


# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))

# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the two robot types compare when cleaning 80%
#       of a 20x20 room?
#
#
# 2) How does the performance of the two robot types compare when two of each
#       robot cleans 80% of rooms with dimensions 
#       10x30, 20x15, 25x12, and 50x6?
#
#

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the two robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, FaultyRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, FaultyRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


#show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time / steps')
#show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time / steps')
