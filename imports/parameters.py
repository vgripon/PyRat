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

import argparse
import sys

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--rat', type=str, metavar = "rat_file", help='Program to control the rat', default="")
parser.add_argument('--python', type=str, metavar = "python_file", help='Program to control the python', default="")
parser.add_argument('-x', '--width', type=int, metavar = "x", help='Width of the maze', default=21)
parser.add_argument('-y', '--height', type=int, metavar = "y", help='Height of the maze', default=15)
parser.add_argument('-d', '--density', type=float, metavar = "d", help='Targetted density of walls', default=0.7)
parser.add_argument('-p', '--pieces', type=int, metavar = "p", help='Number of pieces of cheese', default=13)
parser.add_argument('--nonsymmetric', action="store_true", help='Do not enforce symmetry of the maze')
parser.add_argument('-md', '--mud_density', type=float, metavar = "md", help='Mud density', default=0.1)
parser.add_argument('-mr', '--mud_range', type=int, metavar = "mr", help='Mud range (mud is between 2 and mr)', default=10)
parser.add_argument('--nonconnected', action="store_true", help='Does not enforce connectivity of the maze')
parser.add_argument('--preparation_time', type=int, metavar = "pt", help='Preparation time in milliseconds', default=2000)
parser.add_argument('--turn_time', type=int, metavar = "tt", help='Turn time in milliseconds', default=100)
parser.add_argument('--window_width', type=int, metavar = "ww", help='Window width (in pixels)', default=1366)
parser.add_argument('--auto_exit', action="store_true", help='Automatically exit when game is finished (useful for scripts)')
parser.add_argument('--desactivate_animations', action='store_true', help='Desactivate animations (for slower systems)')
parser.add_argument('--synchronous', action='store_true', help='Wait for players')
parser.add_argument('-mt', '--max_turns', type=int, metavar = "mt", help='Max number of turns', default=2000)
parser.add_argument('--nodrawing', action="store_true", help='Desactivate drawing')
parser.add_argument('--tests', type=int, metavar = "tests", help='Number of tests (for statistics)', default=1)
parser.add_argument('--maze_file', metavar = "maze_file", help='Specific maze file to load', default="")
parser.add_argument('--fullscreen', action="store_true", help='Start game in fullscreen (you can press the "f" key instead)')
args = parser.parse_args()
args.window_height = int(10 * args.window_width / 16)

# Check for conflicts
if args.synchronous and not(args.desactivate_animations):
    print("Note: in synchronous mode, animations are automatically desactivated", file=sys.stderr)
    args.desactivate_animations = True
if args.nodrawing:
    args.auto_exit = True
if args.tests > 1:
    args.auto_exit = True
if args.python=="human":
    is_human_python = True
else:
    is_human_python = False
if args.rat=="human":
    is_human_rat = True
else:
    is_human_rat = False
if args.width < 1 or args.height < 1:
    sys.exit("maze is too small")
