# pymaze
# Contains the object to contain our mazes

from enum import Enum

class Direction(Enum):
    """ An enumerated type for the direction we are traveling
    Ensure the directions work clockwise
    """
    NORTH = 1,
    EAST = 2,
    SOUTH = 3,
    WEST = 4

    def __str__(self):
        if (self == self.NORTH):
            return "North"
        elif (self == self.SOUTH):
            return "South"
        elif (self == self.EAST):
            return "East"
        else:
            return "West"


class Node:
    """Node objects for our Maze"""
    def __init__(self, position):
        # All nodes have a position in the graph
        self.position = position

        # Each node can have, at most, 4 neighbors -- a north, south, east, and west neighbor
        self.neighbors = {Direction.NORTH: None, Direction.SOUTH: None, Direction.EAST: None, Direction.WEST: None}

        # we must also track the parent node of the nodes we visit when we are solving the maze so we can construct
        # the path to the end
        self.parent = None

    def __str__(self):
        return "Node { " + str(self.position) + "}"

    # see documentation on the A* implementation for why this operator overload is necessary
    def __lt__(self, other):
        return False

    def get_position(self):
        """Returns a tuple containing the position of the node"""
        return self.position
    
    def has_neighbor(self, direction: Direction) -> bool:
        return self.neighbors[direction] is not None


class MazeException(Exception):
    """Exceptions generated in the maze will use this exception"""
    def __init__(self, message, position):
        super(MazeException, self).__init__(message)
        self.message = message
        self.position = position

    def __str__(self):
        self.message += " (error occurred at pixel " + str(self.position) + ")"
        return self.message


class Maze:
    """An object to store maze data"""

    # Some static methods to test whether a pixel is white or black
    @staticmethod
    def is_white(pixel):
        return pixel == (255, 255, 255)

    @staticmethod
    def is_black(pixel):
        return pixel == (0, 0, 0)

    def __init__(self, image):
        # open the maze file and operate through it, finding black and white squares
        self.maze_file = image
        # make sure we keep track of the maze width and height
        self.width, self.height = self.maze_file.size

        # the start and end positions should start out as None, and get updated when we create the nodes for the graph
        self.start = None
        self.end = None

        # track the number of nodes
        self.num_nodes = 0

        """Get the nodes in the maze and create Node objects for them. They are accessed by using the start and end
        nodes, depending on how you are traversing the maze."""

        # we need a list to hold the next highest nodes in the row above; this will allow us to determine neighbors on
        # the north and south sides of a node
        top_nodes = [None] * self.width

        # first, get the start node by iterating over the first row
        # if there are multiple white pixels in the top row, the leftmost one is considered to be the start
        x = 1   # x must start at 1; corners cannot be the start, as we must have a border
        y = 0   # we are iterating over the row at y=0

        # iterate as long as we haven't exhausted the pixels in the top line and we still don't have a start node
        while (x < self.width - 1) and (self.start is None):
            px = self.maze_file.getpixel((x, y))

            if self.is_white(px):   # if the pixel is white
                self.start = Node((x, y))
                top_nodes[x] = self.start   # make sure we add the start node to top_nodes so that the next node down
                # has a northern neighbor
                self.num_nodes += 1
            elif self.is_black(px):
                # skip black pixels; increment x position
                x += 1
            else:
                # if it's not white or black, raise an exception -- it must be black/white
                message = "BMP image must be black and white (RGB values were " + str(px) + ")"
                raise MazeException(message, (x, y))

        # ensure there is a start node on the top line -- if self.start is None, we didn't find one
        if self.start is None:
            raise Exception("There must be a start point in the top row of the image.")

        # iterate over every pixel in the image _except_ the first and last rows
        for y in range(1, self.height - 1):
            # left_node must be set to None at the start of every row
            left_node = None

            for x in range(self.width):
                px = self.maze_file.getpixel((x, y))

                # if the pixel is all white, we can make a node based on its neighbors
                if self.is_white(px):
                    # test the pixels at (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)
                    # get the pixels at these positions and use variables to make it more readable
                    north_neighbor = self.maze_file.getpixel((x, y - 1))
                    south_neighbor = self.maze_file.getpixel((x, y + 1))

                    # it is possible we don't have a black border; if so, pretend as if the neighbors on the edges have
                    # a black square next to them

                    # check to see if the east/west sides are at the end; if so, set it equal to a black pixel
                    if x != self.width - 1:
                        east_neighbor = self.maze_file.getpixel((x + 1, y))
                    else:
                        east_neighbor = (0, 0, 0)

                    if x != 0:
                        west_neighbor = self.maze_file.getpixel((x - 1, y))
                    else:
                        west_neighbor = (0, 0, 0)

                    # if only the north and south neighbors, or only the east and west neighbors, are white, it's
                    # not a node, as we have a straight tunnel
                    # otherwise, we can create a node at the position
                    if (self.is_white(north_neighbor) and self.is_white(south_neighbor)) \
                            and not (self.is_white(east_neighbor) or self.is_white(west_neighbor)):
                        continue
                    elif (self.is_white(east_neighbor) and self.is_white(west_neighbor)) \
                            and not (self.is_white(north_neighbor) or self.is_white(south_neighbor)):
                        continue
                    else:
                        # first, create the new node
                        new_node = Node((x, y))

                        # next, check for neighbors
                        # if the west neighbor is white, we must have a node in that direction; it's in left_node
                        if self.is_white(west_neighbor):
                            if left_node is not None:
                                left_node.neighbors[Direction.EAST] = new_node
                                new_node.neighbors[Direction.WEST] = left_node
                            else:
                                raise MazeException("Expected node to the west; could not find one!", (x, y))

                        # update left_node to be the current node so any nodes to the right have a west neighbor,
                        # assuming there are no walls between
                        left_node = new_node

                        # if the northern neighbor is white, update the north neighbor, and the southern neighbor of
                        # that node
                        if self.is_white(north_neighbor):
                            if top_nodes[x] is not None:    # todo: unnecessary check?
                                t = top_nodes[x]
                                t.neighbors[Direction.SOUTH] = new_node
                                new_node.neighbors[Direction.NORTH] = t
                            else:
                                raise MazeException("Expected node to the north; could not find one!", (x, y))

                        # if there is path below, set top_nodes[x] to be the current node
                        if self.is_white(south_neighbor):
                            top_nodes[x] = new_node

                        self.num_nodes += 1

                # on a black pixel, set top_nodes[x] and left_node to None
                elif self.is_black(px):
                    top_nodes[x] = None
                    left_node = None

                # if we find a color other than black or white, it's an error
                else:
                    message = "BMP image must be black and white (RGB values were " + str(px)
                    raise MazeException(message, (x, y))

        # iterate over the last row of pixels
        y = self.height - 1
        x = 1
        while (x < self.width - 1) and (self.end is None):
            px = self.maze_file.getpixel((x, y))

            if self.is_white(px):
                # create the end node if we find a white pixel
                end_node = Node((x, y))

                # the node to the end must be above it
                if top_nodes[x] is not None:
                    t = top_nodes[x]
                    t.neighbors[Direction.SOUTH] = end_node
                    end_node.neighbors[Direction.NORTH] = t
                else:
                    raise MazeException("No node found north of end position", (x, y))

                self.end = end_node
                self.num_nodes += 1
            elif self.is_black(px):
                x += 1
            else:
                # if it's not white or black, raise an exception -- it must be black/white
                message = "BMP image must be black and white (RGB values were " + str(px) + ")"
                raise MazeException(message, (x, y))

        # make sure we have an end node
        if self.end is None:
            raise Exception("There must be an endpoint on the bottom line of the image.")

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_num_nodes(self):
        return self.num_nodes

    def get_dimensions(self):
        return self.width, self.height
