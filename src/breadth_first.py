"""Implementation of the breadth-first search algorithm for use with a Maze object."""

from collections import deque


def breadth_first_search(maze):
    """Solves a maze (from Maze object 'maze') using a breadth-first search"""
    start = maze.get_start()
    end = maze.get_end()

    queue = deque([start])

    # make sure we track which nodes have been visited so we don't get caught in a loop; use a dictionary for speed
    visited = {}
    visited[start.get_position()] = True

    node_count = 0
    completed = False

    # as long as we have values in the queue and we also have not found the end node, continue searching
    while queue and not completed:
        node_count += 1

        # get the current node from the queue, and use our dictionary to get the node that came before this one
        current = queue.pop()

        # if the node we are on is the end node, we are done
        if current == end:
            completed = True
        # otherwise, we need to add the children to the queue
        else:
            # create the list of our neighbor nodes
            neighbors = [current.neighbors["North"], current.neighbors["South"], current.neighbors["East"],
                         current.neighbors["West"]]

            # for every node that exists, update the node that came before it (the current node) and add it to the queue
            for node in neighbors:
                if node is not None and node.get_position() not in visited:
                    # update the "parent" node of the child to point to "current"
                    node.parent = current

                    # update the queue and the visited list
                    queue.appendleft(node)
                    visited[node.get_position()] = True

    # if we solved the maze, construct the path
    if completed:
        # create an object for our path
        path = deque()
        current = end   # start at 'end' and work our way through the path backwards until we reach the start

        # as long as we can retrieve a parent node, we haven't reached the start node
        # the "parent" of the start node will never be updated by the algorithm, so it will always point to 'None'
        while current is not None:
            path.appendleft(current.get_position())     # add the node to the path
            current = current.parent
    else:
        path = []   # if we didn't solve the maze, there is no path

    # return a list of data about the search -- formatted as follows:
    # (bool)completed, (int)node_count, (list< tuple<int, int> >)path
    return completed, node_count, path
