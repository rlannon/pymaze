# pymaze
# Solve the maze by the right-hand rule

from collections import deque
from enum import Enum
import maze


def get_next_direction(current_direction: maze.Direction, node: maze.Node) -> maze.Direction:
    """ Gets the next direction we can move
    """

    dirs = [maze.Direction.NORTH, maze.Direction.EAST, maze.Direction.SOUTH, maze.Direction.WEST]
    to_return = current_direction
    
    try:
        # Start with the node to the right of where we are,
        # walk backwards through the list to find the correct one
        idx: int = dirs.index(current_direction)
        if idx == 3:
            idx = 0
        else:
            idx += 1
        
        to_return = None
        while to_return is None:
            to_test = dirs[idx]
            if node.has_neighbor(to_test):
                to_return = to_test
            else:
                idx -= 1
                if idx == -1:
                    idx = 3
    except ValueError:
        print("Invalid direction")
    
    return to_return
    


def wall_follower(to_solve: maze.Maze) -> list:
    """ Solves the maze with the right-hand rule

    The algorithm is pretty simple:
        * If we can continue straight, do so
        * If we can turn right, do so
        * If we _have to_ turn left, we will
        * If we reach a dead end, we will turn around
    Which direction we are facing will also be tracked (N, S, W, E)
    This means we will always try to go clockwise around the compass if we can, and only go in other directions when it's the only option.

        :param maze:
            The maze object containing the maze to solve
        
        :returns:
            A tuple containing:
                * Whether the maze was completed (bool)
                * The number of nodes in the path (int)
                * The solution path (deque containing nodes)
    """

    # get the start, end nodes
    start_node = to_solve.get_start()
    end_node = to_solve.get_end()
    current_node = start_node

    # get the positions of the start and end
    start_pos = start_node.get_position()
    end_pos = end_node.get_position()

    # the start direction is south
    current_direction = maze.Direction.SOUTH

    # data we want to return
    completed = False
    node_count = 0
    path = deque([start_pos])

    # continue until we are done
    while not completed:
        # increment the node count
        node_count += 1

        # get the next node based on how we are facing
        next_direction = get_next_direction(current_direction, current_node)
        next_node = current_node.neighbors[next_direction]
        next_pos = next_node.get_position()

        # create the new node, setting the current node as its parent
        next_node.parent = current_node
        current_node = next_node
        current_direction = next_direction

        path.append(next_pos)

        if next_pos == end_pos:
            completed = True

    return completed, node_count, path
