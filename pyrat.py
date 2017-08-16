#!/usr/bin/python
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

from imports.parameters import *
from imports.maze import *
import importlib
import sys
import time
from queue import Queue
import queue
from threading import Thread
from imports.display import *
import os
import pygame
import traceback

if args.width < 1 or args.height < 1:
    sys.exit("maze is too small")

try:
    if not(args.nodrawing):
        pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)

        effect_left = pygame.mixer.Sound("resources/cheese_left.wav")
        effect_right = pygame.mixer.Sound("resources/cheese_right.wav")
        effect_both = pygame.mixer.Sound("resources/cheese_both.wav")
        nosound = False
    else:
        1/0
except:
    effect_left = ""
    effect_right = ""
    effect_both = ""
    nosound = True

def play_sound(effect):
    if nosound or args.nodrawing:
        ()
    else:
        try:
            effect.play()
        except:
            ()


def player(pet, filename, q_in, q_out, q_quit, width, height, preparation_time, turn_time):
    try:
        player = importlib.import_module(filename.split(".")[0].replace("/",".").replace("\\","."))
        name = str(getattr(player, "TEAM_NAME"))
        preprocessing = getattr(player, "preprocessing")
        turn = getattr(player, "turn")
        existence = True
    except:
        if filename != "":
            print("Error: " + str((sys.exc_info()[0])), file=sys.stderr)
            print("Error while loading player controlling " + pet + ", dummy player loaded instead", file=sys.stderr)
        player = importlib.import_module("imports.dummyplayer")
        name = str(getattr(player, "TEAM_NAME"))
        preprocessing = getattr(player, "preprocessing")
        turn = getattr(player, "turn")
        existence = False
    q_out.put(name)
    maze = q_in.get()
    player1_location = q_in.get()
    player2_location = q_in.get()
    pieces_of_cheese = q_in.get()    
    try:
        preprocessing(maze, width, height, player1_location, player2_location, pieces_of_cheese, preparation_time)
    except Exception as e:
        traceback.print_exc()
        print(e, file=sys.stderr,)
        while q_quit.empty():
            q_in.get()
            q_out.put("")
    while q_quit.empty():
        player1_location = q_in.get()
        player2_location = q_in.get()
        score1 = q_in.get()
        score2 = q_in.get()
        pieces_of_cheese = q_in.get()
        if not(q_quit.empty()):
            break
        try:
            decision = turn(maze, width, height, player1_location, player2_location, score1, score2, pieces_of_cheese, turn_time)
        except Exception as e:
            traceback.print_exc()
            print(e, file=sys.stderr)
            while q_quit.empty():
                q_in.get()
                q_out.put("")
        q_out.put(decision)

def convert_time_to_int(datetime):
    return datetime.hour * 3600000 + datetime.minute * 60000 + datetime.second * 1000 + datetime.microsecond / 1000.0

def cell_of_decision(location, decision):
    a, b = location
    if decision == "U":
        return (a,b+1)
    elif decision == "D":
        return (a,b-1)
    elif decision == "L":
        return (a-1,b)
    elif decision == "R":
        return (a+1,b)
    else:
        return (-1,-1)
    
def move(decision1, decision2, maze, player1_location, player2_location, stuck1, stuck2, moves1, moves2, miss1, miss2):
    cell1 = cell_of_decision(player1_location, decision1)
    cell2 = cell_of_decision(player2_location, decision2)
    if cell1 in maze[player1_location]:
        stuck1 = maze[player1_location][cell1]
        player1_location = cell1
        moves1 = moves1 + 1
    elif stuck1 <= 0:
        miss1 = miss1 + 1
    if cell2 in maze[player2_location]:
        stuck2 = maze[player2_location][cell2]
        player2_location = cell2
        moves2 = moves2 + 1
    elif stuck2 <= 0:
        miss2 = miss2 + 1
    return player1_location, player2_location, stuck1, stuck2, moves1, moves2, miss1, miss2

def initial_info(q, player1_location, player2_location, maze, pieces_of_cheese):
    q.put(maze)
    q.put(player1_location)
    q.put(player2_location)
    q.put(pieces_of_cheese)

def send_turn(q, player1_location, player2_location, score1, score2, pieces_of_cheese):
    q.put(player1_location)
    q.put(player2_location)
    q.put(score1)
    q.put(score2)
    q.put(pieces_of_cheese)

def send_info(text, q_info):
    if not(args.nodrawing):
        q_info.put(text)
    else:
        print(text, file=sys.stderr)

def run_game():
    global is_human_rat, is_human_python
    # Generate connected maze
    width, height, pieces_of_cheese, maze = generate_maze(args.width, args.height, args.density, not(args.nonconnected), not(args.nonsymmetric), args.mud_density, args.mud_range, args.maze_file)
    player1_location = (0,0)
    player2_location = (width - 1, height - 1)
    # Generate cheese
    if pieces_of_cheese == []:
        pieces_of_cheese = generate_pieces_of_cheese(args.pieces, width, height, not(args.nonsymmetric), player1_location, player2_location)


    # Create players
    q1_in = Queue()
    q2_in = Queue()
    q1_out = Queue()
    q2_out = Queue()
    q1_quit = Queue()
    q2_quit = Queue()


    if not(is_human_rat):
        p1 = Thread(target=player, args=("rat", args.rat, q1_in, q1_out, q1_quit, width, height, args.preparation_time, args.turn_time,))
        p1.start()
    else:
        q1_out.put("human")
    if not(is_human_python):
        p2 = Thread(target=player, args=("python", args.python, q2_in, q2_out, q2_quit, width, height, args.preparation_time, args.turn_time,))
        p2.start()
    else:
        q2_out.put("human")
        
    # Run game
    score1 = 0
    score2 = 0
    stuck1 = 0
    stuck2 = 0

    moves1 = 0
    moves2 = 0
    miss1 = 0
    miss2 = 0
    stucks1 = 0
    stucks2 = 0         

    p1name = str(q1_out.get())
    p2name = str(q2_out.get())

    # Start rendering
    q_render = Queue()
    q_render_in = Queue()
    q_info = Queue()
    if not(args.nodrawing):
        q_render_quit = Queue ()
        draw = Thread(target=run, args=(maze, width, height, q_render, q_render_in, q_render_quit, p1name, p2name, q1_out, q2_out, is_human_rat, is_human_python, q_info))
        draw.start()
    q_render.put(pieces_of_cheese)
    q_render.put(player1_location)
    q_render.put(player2_location)
    q_render.put(args.rat != "")
    q_render.put(args.python != "")

    initial_info(q1_in, player1_location, player2_location, maze, pieces_of_cheese)
    initial_info(q2_in, player2_location, player1_location, maze, pieces_of_cheese)

    if not(args.synchronous):
        time.sleep(args.preparation_time / 1000.0)        

    turns = 0
    win1 = 0
    win2 = 0
    while 1:
        if turns == args.max_turns + 1:
            send_info("max number of turns reached!", q_info)
            break
        turns = turns + 1    

        stuck1 = stuck1 - 1
        stuck2 = stuck2 - 1

        # if args.synchronous:
        #     if stuck1 > 0:
        #         stucks1 = stucks1 + stuck1
        #     if stuck2 > 0:
        #         stucks2 = stucks2 + stuck2
        #     stuck1 = 0
        #     stuck2 = 0
    
        if player1_location in pieces_of_cheese and stuck1 <= 0 and args.rat != "":
            pieces_of_cheese.remove(player1_location)
            if player2_location == player1_location and stuck2 <= 0 and args.python != "":
                score1 = score1 + 0.5
                score2 = score2 + 0.5
                play_sound(effect_both)
            else:
                score1 = score1 + 1
                if player2_location in pieces_of_cheese and stuck2 <= 0 and args.python != "":
                    play_sound(effect_both)
                else:
                    play_sound(effect_left)
        if player2_location in pieces_of_cheese and stuck2 <= 0 and args.python != "":
            pieces_of_cheese.remove(player2_location)
            score2 = score2 + 1
            play_sound(effect_right)

        q_render.put(pieces_of_cheese)
        q_render.put(player1_location)
        q_render.put(player2_location)
        q_render.put(score1)
        q_render.put(score2)
        q_render.put(moves1)
        q_render.put(moves2)
        q_render.put(miss1)
        q_render.put(miss2)
        q_render.put(stucks1)
        q_render.put(stucks2)
    
        if args.rat != "" and args.python != "":
            if score1 > args.pieces // 2:
                if score1 == score2:
                    send_info("The Rat(" + p1name + ") and the Python (" + p2name + ") got the same number of pieces of cheese!", q_info)
                    win1 = win1 + 0.5
                    win2 = win2 + 0.5
                    break
                else:
                    send_info("The Rat (" + p1name + ") won the match!", q_info)
                    win1 = win1 + 1
                    break
            if score2 > args.pieces // 2:
                send_info("The Python (" + p2name + ") won the match!", q_info)
                win2 = win2 + 1
                break
        else:
            if score1 >= args.pieces:
                send_info("The Rat (" + p1name + ") got all pieces of cheese!", q_info)
                win1 = win1 + 1
                break
            elif score2 >= args.pieces:
                send_info("The Python (" + p2name + ") got all pieces of cheese!", q_info)
                win2 = win2 + 1
                break
        if len(pieces_of_cheese) == 0:
            send_info("No more pieces of cheese!", q_info)
            break

    
        if stuck1 <= 0:
            send_turn(q1_in, player1_location, player2_location, score1, score2, pieces_of_cheese)
        if stuck2 <= 0:
            send_turn(q2_in, player2_location, player1_location, score2, score1, pieces_of_cheese)

        if not(args.synchronous):
            time.sleep(args.turn_time / 1000.0)
    
        try:
            if stuck1 <= 0:
                decision1 = str(q1_out.get(args.synchronous))
            else:
                decision1 = "None"
                stucks1 = stucks1 + 1
        except:
            decision1 = "None"
        try:
            if stuck2 <= 0:
                decision2 = str(q2_out.get(args.synchronous))
            else:
                decision2 = "None"
                stucks2 = stucks2 + 1
        except:
            decision2 = "None"
        try:
            q_render_in.get(False)
            os._exit(0)
        except queue.Empty:
            ()

        player1_location, player2_location, stuck1, stuck2, moves1, moves2, miss1, miss2 = move(decision1, decision2, maze, player1_location, player2_location, stuck1, stuck2, moves1, moves2, miss1, miss2)
    q1_quit.put("")
    q2_quit.put("")
    if not(args.nodrawing) and (args.tests > 1 or args.auto_exit):        
        q_render_quit.put("")
    elif not(args.nodrawing):
        q_render_in.get()
        q_render_quit.put("")
    if not(is_human_rat):
        while p1.is_alive():
            q1_in.put("")
    if not(is_human_python):
        while p2.is_alive():
            q2_in.put("")
    if not(args.nodrawing):
      while draw.is_alive ():
          ()
    return {"win_rat": win1, "win_python": win2, "score_rat": score1, "score_python": score2, "moves_rat": moves1, "moves_python": moves2, "miss_rat": miss1, "miss_python": miss2, "stucks_rat":stucks1, "stucks_python":stucks2}

result = run_game()
for i in range(args.tests - 1):
    print("match " + str(i+2) + "/" + str(args.tests))
    new = run_game()
    result = {x: result.get(x, 0) + new.get(x, 0) for x in set(result).union(new)}
result = {k: v / args.tests for k, v in result.items()}
print(repr(result))
