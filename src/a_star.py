# pymaze
# A* Implementation

from FibonacciHeap import FibHeap   # for our Fibonacci heap, we will use Mike Pound's implementation
from priority_queue import HeapPQ  # also from Dr. Pound
from collections import deque
import maze


def get_distance(a, b):
    """Finds the Manhattan between two points, a and b, and returns it.
    The Manhattan distance is |x2 - x1| + |y2 - y1|  -- it is a measure of how many steps in the cardinal directions
    are needed to get between any two points in a grid. This is also called taxicab geometry."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(to_solve):
    """Uses the A* search algorithm (variant of Dijkstra's algorithm) to solve a maze, 'maze'.
    Note that due to the way some mazes are structured -- very dense mazes with short paths -- A* may not outperform
    a breadth-first search, and in fact may be almost identical in its operation with extra computational overhead.
    However, this depends on the variety of maze supplied"""

    # get our start and end nodes
    start = to_solve.get_start()
    end = to_solve.get_end()

    # we will use the start and end positions so frequently that it is worth having variables for them; calling a
    # function is not free, so this trades off a little memory in exchange for a little better performance
    start_pos = start.get_position()
    end_pos = end.get_position()

    # set up our "visited" dictionary, like we have for BFS and DFS
    visited = {}

    # set up our priority queues
    # the unvisited list will be a Heap Priority Queue; the nodes we want to visit will be ordered according to the
    # heuristics we set for them -- get_distance from current node + Euclidian get_distance to end coordinate
    unvisited = HeapPQ()    # we can use any priority queue, but I have found HeapPQ to be the fastest for this purpose

    start_node = FibHeap.Node(0, start)
    unvisited.insert(start_node)    # we start with the start node unvisited

    # we also need an object to equate nodes from the Maze object with nodes from the FibHeap object
    node_index = {}
    node_index[start_pos] = start_node

    # the distances of all nodes start at infinity, because we haven't visited them yet and we don't know what the
    # get_distance is given the best known path
    infinity = float("inf")

    # track the get_distance to a given node using the best path known so far; better paths will replace worse ones as
    # we go. Note, however that this will NOT include the additional heuristic of the get_distance from the point to the
    # end position -- that information is included in the FibHeap node (we don't care about this additional heuristic
    # when we aren't adding new ones to the queue)
    distances = {}    # the get_distance associated with S is 0
    distances[start_pos] = 0

    # track the number of considered nodes and whether we have completed the maze
    node_count = 0
    completed = False

    # as long as we have nodes to visit, continue working
    while not completed and len(unvisited) > 0:
        node_count += 1

        # get the node with the minimum combined heuristic and explore that first
        node = unvisited.remove_minimum()
        current = node.value    # get the Maze.Node object
        current_pos = current.get_position()

        # if we are at the end, we have completed the maze; however, we can't exit just yet -- we need to wait until the
        # queue is empty to be sure we have found the best solution
        if current_pos == end_pos:
            completed = True
        # otherwise, check each unvisited child node, as in the breadth-first search
        else:
            # get our node's neighbors, and check each of them
            neighbors = [current.neighbors[maze.Direction.NORTH], current.neighbors[maze.Direction.SOUTH],
                        current.neighbors[maze.Direction.EAST], current.neighbors[maze.Direction.WEST]]

            for child in neighbors:
                # if there is a neighbor at that position that we have not visited check it; otherwise, continue on
                if child is not None and child.get_position() not in visited:
                    # get the positions so we can calculate our distances
                    parent_pos = current_pos
                    child_pos = child.get_position()

                    # get the get_distance of parent to child
                    parent_to_child = get_distance(parent_pos, child_pos)

                    # we also want to know the get_distance to this child without our additional heuristic of the get
                    # distance to the end node -- just the get_distance to the parent plus parent_to_child
                    path_length = distances[parent_pos] + parent_to_child

                    # get the get_distance of child to end -- this is our additional heuristic
                    remaining_distance = get_distance(child_pos, end_pos)

                    # if we have a get_distance associated with the node, fetch it; otherwise, it's infinity
                    if child_pos in distances:
                        current_distance = distances[child_pos]
                    else:
                        current_distance = infinity

                    # We will only update the get_distance if path length is less than the get_distance currently
                    # associated with this node's position -- if it's not, then the other path we have found to this
                    # node is shorter, and so we shouldn't make any changes in the path to that node
                    if path_length < current_distance:
                        # if we have a node for the child already, update it; otherwise, create a new node for the child
                        if child_pos in node_index:
                            # we want to decrease the get_distance heuristic of the child node; but first, we need to
                            # fetch the node from node_index, as decrease_key operates on a FibHeap.Node object
                            to_decrease = node_index[child_pos]
                            # the key is the coordinate, the new value is the path length plus the extra heuristic
                            unvisited.decrease_key(to_decrease, path_length + remaining_distance)

                            # update the get_distance to this node as well -- we have found a shorter path; again, this
                            # does not include the additional heuristic
                            distances[child_pos] = path_length

                            # we also need to update the new parent node of that child
                            child.parent = current
                        # if we don't have a node for the child yet, create one
                        else:
                            # create a FibHeap node and add it to our priority queue
                            new_node = FibHeap.Node(path_length + remaining_distance, child)
                            node_index[child_pos] = new_node
                            unvisited.insert(new_node)

                            # update the entry at the get_distance vector for the child and make sure we mark the
                            # current node as its previous node
                            distances[child_pos] = path_length
                            child.parent = current

        # add this node to "visited" so we don't try to evaluate it again
        visited[current_pos] = True

    # in the same manner as in in the BFS algorithm, construct the path by going back through the parent of each node,
    # starting at the end node and working backwards
    if completed:
        path = deque()
        current = end
        while current is not None:
            path.appendleft(current.get_position())     # has a complexity of O(1) at each end, so do this instead of
            current = current.parent  # appending to a list and reversing it at the end
    else:
        path = []

    # we must return (bool)solved, (int)node_count, (list< tuple< int, int > >)path
    return completed, node_count, path
