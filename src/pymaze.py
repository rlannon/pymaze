# user-modules
from maze import *
from breadth_first import *
from depth_first import *
from a_star import *
from draw_solution import *
from wall_follow import *

# built-in modules
import time     # so we can keep track of how long operations take
import argparse  # so we can use command-line arguments
from PIL import Image


def min_length(nmin):
    """Specifies the minimum length of an argparse argument. If the number of values supplied is less than the 'nmin',
    raises an exception"""
    class MinimumLength(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if len(values) < nmin:
                msg = 'argument "{f}" requires at least {nmin} arguments'.format(f=self.dest, nmin=nmin)
                raise argparse.ArgumentTypeError(msg)
            setattr(args, self.dest, values)
    return MinimumLength


def main(argv):
    # if we get an error when trying to solve the maze, we will catch it and display the error message
    try:
        maze_path = argv.infile
        output_path = argv.outfile
        algorithm = argv.algorithm
        compare = argv.compare

        # load the image and convert to RGB format
        print("Loading image...")
        maze_image = Image.open(maze_path)
        maze_image = maze_image.convert("RGB")

        print("Creating maze...")
        t0 = time.time()
        to_solve = Maze(maze_image)
        t1 = time.time()
        scan_total = t1 - t0

        print("Found", to_solve.get_num_nodes(), "nodes")
        print("Time elapsed:", scan_total)

        print()
        print("Solving maze...")

        # if we are just using one algorithm
        if not compare:
            # breadth-first search
            if algorithm == "bfs":
                print("Algorithm = BFS")
                t0 = time.time()
                solved, explored_count, path = breadth_first_search(to_solve)
                t1 = time.time()
            # depth-first search
            elif algorithm == "dfs":
                print("Algorithm = DFS")
                t0 = time.time()
                solved, explored_count, path = depth_first_search(to_solve)
                t1 = time.time()
            # A*
            elif algorithm == "a*":
                print("Algorithm = A*")
                t0 = time.time()
                solved, explored_count, path = a_star(to_solve)
                t1 = time.time()
            # Wall follow method
            elif algorithm == "wall":
                print("Algorithm = right-hand wall follow method")
                t0 = time.time()
                solved, explored_count, path = wall_follower(to_solve)
                t1 = time.time()
            else:
                raise Exception("You must specify an algorithm.")

            solve_total = t1 - t0

            # print out our data and draw our image, if there is a solution to the maze
            if solved:
                print("Nodes explored:", explored_count)
                print("Path length:", len(path), "nodes")
                print("Time elapsed:", solve_total)
                print()
                print("Drawing image...")
                # our draw_solution function will also calculate the distance traversed in the path
                solution_img, total_distance = draw_solution(maze_image, path)
                solution_img.save(output_path)
                print("Path length as calculated by draw_solution:", total_distance, "pixels")
            else:
                print("No solution.")

        # otherwise, we have algorithms to compare
        else:
            # todo: generalize this since we are accruing more algorithms
            a_star_time = None
            a_star_solved = False

            bfs_time = None
            bfs_solved = False

            dfs_time = None
            dfs_solved = False

            wall_time = None
            wall_solved = False

            # track the shortest explored path and the path that was found quickest
            fewest_nodes = [float("inf"), ""]
            fewest_considered = [float("inf"), ""]
            fastest_compute_time = [float("inf"), ""]

            # iterate through each algorithm in the comparison list
            for algorithm in compare:
                # check which algorithm we want and verify that we haven't supplied the same algorithm more than once
                # by checking whether our time variable has been modified
                if algorithm == "a*" and a_star_time is None:
                    print("Running A* ...")
                    t0 = time.time()
                    a_star_solved, a_star_explored_count, a_star_path = a_star(to_solve)
                    t1 = time.time()
                    a_star_time = t1 - t0

                    print("Time:", a_star_time)
                    print("Nodes considered:", a_star_explored_count)
                    print("Nodes in path:", len(a_star_path))
                    print()

                    if len(a_star_path) < fewest_nodes[0]:
                        fewest_nodes = [len(a_star_path), "A*"]

                    if a_star_explored_count < fewest_considered[0]:
                        fewest_considered = [a_star_explored_count, "A*"]

                    if a_star_time < fastest_compute_time[0]:
                        fastest_compute_time = [a_star_time, "A*"]
                elif algorithm == "bfs" and bfs_time is None:
                    print("Running BFS ...")
                    t0 = time.time()
                    bfs_solved, bfs_explored_count, bfs_path = breadth_first_search(to_solve)
                    t1 = time.time()
                    bfs_time = t1 - t0

                    print("Time:", bfs_time)
                    print("Nodes considered:", bfs_explored_count)
                    print("Nodes in path:", len(bfs_path))
                    print()

                    if len(bfs_path) < fewest_nodes[0]:
                        fewest_nodes = [len(bfs_path), "BFS"]

                    if bfs_explored_count < fewest_considered[0]:
                        fewest_considered = [bfs_explored_count, "BFS"]

                    if bfs_time < fastest_compute_time[0]:
                        fastest_compute_time = [bfs_time, "BFS"]
                elif algorithm == "dfs" and dfs_time is None:
                    print("Running DFS ...")
                    t0 = time.time()
                    dfs_solved, dfs_explored_count, dfs_path = depth_first_search(to_solve)
                    t1 = time.time()
                    dfs_time = t1 - t0

                    print("Time:", dfs_time)
                    print("Nodes considered:", dfs_explored_count)
                    print("Nodes in path:", len(dfs_path))
                    print()

                    if len(dfs_path) < fewest_nodes[0]:
                        fewest_nodes = [len(dfs_path), "DFS"]

                    if dfs_explored_count < fewest_considered[0]:
                        fewest_considered = [dfs_explored_count, "DFS"]

                    if dfs_time < fastest_compute_time[0]:
                        fastest_compute_time = [dfs_time, "DFS"]
                elif algorithm == "wall" and wall_time is None:
                    print("Running wall algorithm...")
                    t0 = time.time()
                    wall_solved, wall_explored_count, wall_path = wall_follower(to_solve)
                    t1 = time.time()
                    wall_time = t1 - t0

                    print("Time:", wall_time)
                    print("Nodes in path:", len(wall_path))
                    print()

                    if len(wall_path) < fewest_nodes[0]:
                        fewest_nodes = [len(wall_path), "wall"]
                    
                    if wall_explored_count < fewest_considered[0]:
                        fewest_considered = [wall_explored_count, "wall"]
                    
                    if wall_time < fastest_compute_time[0]:
                        fastest_compute_time = [wall_time, "wall"]
                else:
                    raise Exception("Invalid algorithm for comparison")

            solved = a_star_solved or bfs_solved or dfs_solved or wall_solved

            if solved:
                # set up our list to track which algorithm has the shortest length; if the lengths of two algorithms are
                # identical, we must have a perfect maze, or at least there is no algorithm that performs best
                shortest_length = [float("inf"), ""]
                paths_equal = False

                if dfs_time is not None and dfs_solved:
                    print("Drawing path generated by DFS (red)...")
                    maze_image, dfs_path_length = draw_solution(maze_image, dfs_path, (255, 0, 0))

                    if dfs_path_length < shortest_length[0]:
                        shortest_length = [dfs_path_length, "DFS"]
                if bfs_time is not None and bfs_solved:
                    print("Drawing path generated by BFS (green)...")
                    maze_image, bfs_path_length = draw_solution(maze_image, bfs_path, (0, 255, 0))

                    if bfs_path_length < shortest_length[0]:
                        shortest_length = [bfs_path_length, "BFS"]
                    elif bfs_path_length == shortest_length[0]:
                        paths_equal = True
                if a_star_time is not None and a_star_solved:
                    print("Drawing path generated by A* (blue)...")
                    maze_image, a_star_path_length = draw_solution(maze_image, a_star_path, (0, 0, 255))

                    if a_star_path_length < shortest_length[0]:
                        shortest_length = [a_star_path_length, "A*"]
                    elif a_star_path_length == shortest_length[0]:
                        paths_equal = True
                if wall_time is not None and wall_solved:
                    print("Drawing path generated by the wall algorithm (purple)...")
                    maze_image, wall_path_length = draw_solution(maze_image, wall_path, (127, 0, 127))

                    if wall_path_length < shortest_length[0]:
                        shortest_length = [wall_path_length, "wall"]
                    elif wall_path_length == shortest_length[0]:
                        paths_equal = True

                print()
                print("Summary:")
                print("Algorithm that considered the fewest nodes was", fewest_considered[1], "(considered",
                      fewest_considered[0], "nodes)")
                print("Path with fewest nodes was found by", fewest_nodes[1], "(length of", fewest_nodes[0], "nodes)")

                if not paths_equal:
                    print("Path with shortest length was found by", shortest_length[1], "(length of", fewest_nodes[0],
                          "pixels)")

                print("Fastest path calculation was performed by", fastest_compute_time[1], "(took",
                      fastest_compute_time[0], "seconds)")
                print()

                # save the resultant image
                maze_image.save(output_path)

            # otherwise, if there was no solution, alert the user
            else:
                print("No solution")

        # close our image
        maze_image.close()
        print("Done.")

    except Exception as e:
        print(f"**** Error: {e}")

    finally:
        return 0


if __name__ == "__main__":
    # use argparse library for command-line use
    parser = argparse.ArgumentParser(description="mazesolve: solve mazes from input images")
    parser.add_argument('-i', '--infile', help="The path to the image containing the maze you wish to solve",
                        required=True)
    parser.add_argument('-o', '--outfile', help="The path of the solution image", default="solution.png")
    parser.add_argument('-a', '--algorithm', help="The algorithm you wish to use; may either be 'bfs' (for breadth-"
                                                  "first searching), 'dfs' (depth-first search), 'a*' (to use the A*"
                                                  " algorithm), or 'wall' (to use the right-hand method). If unspecified, uses BFS",
                        default="bfs", choices=["bfs", "dfs", "a*", "wall"])
    parser.add_argument('-c', '--compare', choices=["bfs", "dfs", "a*", 'wall'], help="Compare two or more algorithms and see "
                        "which performs best by a variety of criteria", nargs="*", action=min_length(2))

    # if we get an error in parsing, catch and display it
    try:
        args = parser.parse_args()
        main(args)
    except argparse.ArgumentTypeError as err:
        print(parser.error(err))
