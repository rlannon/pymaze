# pymaze

A simple maze solver written in Python.

## About

This project was originally written for an Algorithms course and was inspired by [a similar project](https://github.com/mikepound/mazesolving) by University of Nottingham professor Mike Pound.

This project is a fun way to implement graphs and searching algorithms. The program loads an image and generates a graph data structure from it. From there, it is able to use breadth-first searching or A* to find a solution. It will generate a copy of the image with the solution highlighted (the coloring was taken from Dr. Pound's implementation -- I thought the blue to red gradient in the solution was a nice touch). The console will also display various information about the solution -- how many nodes were discovered, how many were in the path, the elapsed time, etc..

The program supports perfect mazes, where there is only one solution; as well as normal mazes, where multiple solutions are possible. In the event of a normal maze, the program will find the best solution.

## Getting Started

This program was designed to be used in the command line, and so there is no user interface. It has minimal dependencies, though it does require the [Python Imaging Library](https://www.pythonware.com/products/pil/).

### Input

The image file must be either PNG, BMP, or other bitmap iamge formats used by the Python Imaging Library. _JPEG compression is not supported._ The requirements for mazes are as follows:

* Must be black and white. Any other color besides 0x000000 and 0xFFFFFF will cause the program to abort
* White pixels are path, black pixels are walls
* Mazes must be surrounded by a black border, save a pixel along the top and a pixel along the bottom to represent the start and end nodes, respectively; mazes must not start or end in the center, though this feature may be implemented in future

### Command-line usage

This program is meant to be run from the command line. It uses the Python module ```argparse``` to parse command-line arguments. It takes the following flags:

```mazesolve.py [-h] -i INFILE [-o OUTFILE] [-a {bfs, dfs, a*} ] [-c {bfs, dfs, a*} ]```

The 'h' flag will display a help/usage message. An input file, specified with the 'i' flag, is always required. If left unspecified, the outfile will be 'solution.png' in the main directory and the algorithm will be BFS.

The compare flag (```-c```) allows the user to compare two or more algorithms to see how they perform on the same maze. This is more efficient than running the program with the same image twice using different algorithms, as it does not reconstruct the Maze object each time an algorithm solves it. This saves computational energy by using the same object in each algorithm. Since the ```Maze.parent``` member is not used by each algorithm until the very end, it does not affect the outcomes or performance of the algorithms because these values are overwritten as necessary before they are used.

## Notes

In this implementation, BFS performs better than A\* does. Although A\* considers _far_ fewer nodes, it takes more time to come up with a solution. This is in part due to how the mazes are constructed, but partially because A\* has a lot more overhead than BFS and the current implementation is not optimized.

Most images included in this repository come from the aforementioned project by Dr. Pound.
