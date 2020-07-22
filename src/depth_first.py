# pymaze
# Implementation of DFS

from collections import deque
import maze


def depth_first_search(to_solve: maze.Maze) -> list:
    """Run a depth-first search on the maze object"""

    # set up the function like the others; however, this algorithm will be more similar to BFS than to A*
    # we will get the start and end nodes and use dictionaries to fetch previous nodes and visited nodes
    start = to_solve.get_start()
    end = to_solve.get_end()

    # like the other algorithms, use a dictionary to track which nodes have been visited
    visited = {}

    # while we used a queue for the breadth-first search, we will use a stack here (using deque). While we could use a
    # list for this purpose, a deque will give us better performance because a list might call realloc, while a deque
    # uses linked list logic, meaning we do not need to worry about heap fragmentation and memory reallocation with it
    fringe = deque([start])

    completed = False
    node_count = 0

    # like the other algorithms, continue searching if we have nodes to consider and we also have not found a solution
    while not completed and fringe:
        node_count += 1
        current = fringe.pop()

        if current == end:
            completed = True
        else:
            # get the node's children
            neighbors = [current.neighbors[maze.Direction.NORTH], current.neighbors[maze.Direction.SOUTH],
                        current.neighbors[maze.Direction.EAST], current.neighbors[maze.Direction.WEST]]

            # iterate through each child node, making sure we only operate on valid nodes that haven't been visited
            for child in neighbors:
                if child is not None and child.get_position() not in visited:
                    child.parent = current
                    fringe.append(child)

        visited[current.get_position()] = True

    # construct the path in the same manner as the other algorithms
    if completed:
        path = deque()
        current = end
        while current is not None:
            path.appendleft(current.get_position())
            current = current.parent
    else:
        path = []

    return completed, node_count, path
