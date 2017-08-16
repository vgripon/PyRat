#    Copyright © 2017 Vincent Gripon (vincent.gripon@imt-atlatique.fr) and IMT Atlantique
#
#    This file is part of PyRat.
#
#    PyRat is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PyRat is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PyRat.  If not, see <http://www.gnu.org/licenses/>.

import random
import sys
import imports.parameters

# compute the connected component of a given initial cell with depth-first search
def connected_region(maze, cell, connected):
  for neighbor in maze[cell]:
    if not(neighbor in connected):
        connected.append(neighbor)
        connected_region(maze, neighbor, connected)

def gen_mud(mud_density, mud_range):
    if random.uniform(0, 1) < mud_density:
        return random.randrange(2, mud_range + 1)
    else:
        return 1

def generate_maze(width, height, target_density, connected, symmetry, mud_density, mud_range, maze_file):
    if maze_file != "":
        with open(maze_file, 'r') as content_file:
            content = content_file.read()
        lines = content.split("\n")
        width = int(lines[0])
        height = int(lines[1])
        maze = {}
        for i in range(width):
            for j in range(height):
                maze[(i,j)] = {}
                line = lines[i + j * width +2].split(" ")
                if line[0] != "0":
                    maze[(i,j)][(i,j+1)] = int(line[0])
                if line[1] != "0":
                    maze[(i,j)][(i,j-1)] = int(line[1])
                if line[2] != "0":
                    maze[(i,j)][(i-1,j)] = int(line[2])
                if line[3] != "0":
                    maze[(i,j)][(i+1,j)] = int(line[3])
        line = lines[height*width+2].split(" ")
        pieces_of_cheese = []
        for i in range(len(line)):
            l = int(line[i])
            pieces_of_cheese.append((l % width, l // width))
    else:
        # Start with purely random maze
        maze = {};
        not_considered = {};
        for i in range(width):
            for j in range(height):
                maze[(i,j)] = {}
                not_considered[(i,j)] = True
        for i in range(width):
            for j in range(height):
                if not(symmetry) or not_considered[(i,j)]:
                    if random.uniform(0,1) > target_density and i + 1 < width:
                        m = gen_mud(mud_density, mud_range)
                        maze[(i,j)][(i+1,j)] = m
                        maze[(i+1,j)][(i,j)] = m
                        if symmetry:
                            maze[(width - 1 - i, height - 1 - j)][(width - 2 - i, height - 1 - j)] = m
                            maze[(width - 2 - i, height - 1 - j)][(width - 1 - i, height - 1 - j)] = m
                    if random.uniform(0,1) > target_density and j + 1 < height:
                        m = gen_mud(mud_density, mud_range)
                        maze[(i,j)][(i,j+1)] = m
                        maze[(i,j+1)][(i,j)] = m
                        if symmetry:
                            maze[(width - 1 - i, height - 2 - j)][(width - 1 - i, height - 1 - j)] = m
                            maze[(width - 1 - i, height - 1 - j)][(width - 1 - i, height - 2 - j)] = m
                    if symmetry:
                        not_considered[(i,j)] = False
                        not_considered[(width - 1 - i, height - 1 - j)] = False
        for i in range(width):
            for j in range(height):
                if len(maze[(i,j)]) == 0 and (i == 0 or j == 0 or i == width - 1 or j == height - 1):
                    m = gen_mud(mud_density, mud_range)
                    possibilities = []
                    if i + 1 < width:
                        possibilities.append((i+1,j))
                    if j + 1 < height:
                        possibilities.append((i,j+1))
                    if i - 1 >= 0:
                        possibilities.append((i-1,j))
                    if j - 1 >= 0:
                        possibilities.append((i,j-1))
                    chosen = possibilities[random.randrange(len(possibilities))]
                    maze[(i,j)][chosen] = m                
                    maze[chosen][(i,j)] = m
                    if symmetry:
                        ii, jj = chosen
                        maze[(width - 1 - i, height - 1 - j)][(width - 1 - ii, height - 1 - jj)] = m
                        maze[(width - 1 - ii, height - 1 - jj)][(width - 1 - i, height - 1 - j)] = m

        # Then connect it
        if connected:
            connected = [(0,height-1)]
            connected_region(maze, (0,height-1), connected)
            while 1:
                if len(connected) >= width * height:
                    break
                border = []
                for i in range(width):
                    for j in range(height):
                        if not((i+1,j) in maze[(i,j)]) and i + 1 < width:
                            if ((i+1,j) in connected and not((i,j) in connected)):
                                border.append(((i+1,j),(i,j)))
                            elif ((i,j) in connected and not((i+1,j) in connected)):
                                border.append(((i,j),(i+1,j)))
                        if not((i,j+1) in maze[(i,j)]) and j + 1 < height:
                            if ((i,j+1) in connected and not((i,j) in connected)):
                                border.append(((i,j+1),(i,j)))
                            elif ((i,j) in connected and not((i,j+1) in connected)):
                                border.append(((i,j),(i,j+1)))
                a,b = border[random.randrange(len(border))]
                m = gen_mud(mud_density, mud_range)
                maze[a][b] = m
                maze[b][a] = m
                if symmetry:
                    ai, aj = a
                    bi, bj = b
                    bsym = (width - 1 - bi, height - 1 - bj)
                    asym = (width - 1 - ai, height - 1 - aj)
                    maze[asym][bsym] = m
                    maze[bsym][asym] = m
                connected.append(b)
                connected_region(maze, b, connected)
                if symmetry:
                    if not(bsym in connected) and (asym in connected):
                        connected.append(bsym)
                    connected_region(maze, bsym, connected)
        pieces_of_cheese = []
    return width, height, pieces_of_cheese, maze

# Generate pieces of cheese
def generate_pieces_of_cheese(nb_pieces, width, height, symmetry, player1_location, player2_location):
    remaining = nb_pieces
    pieces = []
    candidates = []
    considered = []
    if symmetry:
        if nb_pieces % 2 == 1 and (width % 2 == 0 or height % 2 == 0):
            sys.exit("The maze has even width or even height and thus cannot contain an odd number of pieces of cheese if symmetric.")
        if nb_pieces % 2 == 1:
            pieces.append((width // 2, height // 2))
            considered.append((width // 2, height // 2))
            remaining = remaining - 1
    for i in range(width):
        for j in range(height):
            if (not(symmetry) or not((i,j) in considered)) and (i,j) != player1_location and (i,j) != player2_location:
                candidates.append((i,j))
                if symmetry:
                    considered.append((i,j))
                    considered.append((width - 1 - i, height - 1 - j))
    while remaining > 0:
        if len(candidates) == 0:
            sys.exit("Too many pieces of cheese for that dimension of maze")
        chosen = candidates[random.randrange(len(candidates))]
        pieces.append(chosen)
        if symmetry:
            a, b = chosen
            pieces.append((width - a - 1, height - 1 - b))
            symmetric = (width - a - 1, height - 1 - b)
            candidates = [i for i in candidates if i != symmetric]
            remaining = remaining - 1
        candidates = [i for i in candidates if i != chosen]
        remaining = remaining - 1
    return pieces
        
