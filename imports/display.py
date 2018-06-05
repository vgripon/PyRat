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
import pygame
import random
import datetime
from pygame import locals

def image_of_maze(maze, tiles, image_tile, image_wall, image_corner, image_mud, offset_x, offset_y, scale, width, height, screen, window_height):
    global mud_range
    for i in range(width):
        for j in range(height):
            screen.blit(image_tile[tiles[i][j]], (offset_x + scale * i, window_height - offset_y - scale * (j+1)))
    for i in range(width):
        for j in range(height):
            if not((i-1,j) in maze[(i,j)]):
                pass
            elif maze[(i,j)][(i-1,j)] > 1:
                screen.blit(image_mud, (offset_x + scale * i - scale/2, window_height - offset_y - scale * (j+1)))
            if not((i,j+1) in maze[(i,j)]):
                pass
            elif maze[(i,j)][(i,j+1)] > 1:
                screen.blit(pygame.transform.rotate(image_mud, 270), (offset_x + scale * i, window_height - offset_y - scale * (j+1) - scale/2))
    for i in range(width):
        for j in range(height):
            if not((i-1,j) in maze[(i,j)]):
                screen.blit(image_wall, (offset_x + scale * i - scale / 2, window_height - offset_y - scale * (j+1)))
            if not((i,j+1) in maze[(i,j)]):
                screen.blit(pygame.transform.rotate(image_wall, 270), (offset_x + scale * i, window_height - offset_y - scale * (j+1) - scale/2))
    for i in range(width):
        screen.blit(pygame.transform.rotate(image_wall, 270), (offset_x + scale * i, window_height - offset_y - scale/2))
    for j in range(height):
        screen.blit(image_wall, (offset_x + scale * width -scale/2, window_height - offset_y - scale * (j+1)))
    for i in range(width+1):
        for j in range(height+1):
            horiz = False
            vert = False
            count = 0
            if i == 0 or i == width:
                vert = True
            if j == 0 or j == height:
                horiz = True
            # is there a wall left?
            if i > 0 and j < height and j > 0:
                if (i-1,j) not in maze[(i-1,j-1)]:
                    horiz = True
                    count = count + 1
            # is there a wall right?
            if i < width and j < height and j > 0:
                if (i,j-1) not in maze[(i,j)]:
                    horiz = True
                    count = count + 1
            # is there a wall up?
            if i > 0 and i < width and j < height:
                if (i,j) not in maze[(i-1,j)]:
                    vert = True
                    count = count + 1
            # is there a wall down?
            if i > 0 and i < width and j > 0:
                if (i,j-1) not in maze[(i-1,j-1)]:
                    vert = True
                    count = count + 1
            if vert and horiz or count == 1:                
                screen.blit(image_corner, (offset_x + scale * i - scale/2, window_height - offset_y - scale * j - scale/2))

def draw_pieces_of_cheese(pieces_of_cheese, image_cheese, offset_x, offset_y, scale, width, height, screen, window_height):
    for (i,j) in pieces_of_cheese:
        screen.blit(image_cheese, (offset_x + scale * i, window_height - offset_y - scale * (j+1)))

def draw_players(player1_location, player2_location, image_python, image_rat, offset_x, offset_y, scale, width, height, screen, window_height):
    i, j = player1_location
    screen.blit(image_python, (offset_x + scale * i, window_height - offset_y - scale * (j+1)))
    i, j = player2_location
    screen.blit(image_rat, (offset_x + scale * i, window_height - offset_y - scale * (j+1)))


def draw_players_animate(player1_location, player2_location, image_python, image_rat, offset_x, offset_y, scale, width, height, screen, window_height):
    i, j = player1_location
    screen.blit(image_python, (offset_x + scale * i, window_height - offset_y - scale * (j+1)))
    i, j = player2_location
    screen.blit(image_rat, (offset_x + scale * i, window_height - offset_y - scale * (j+1)))

font_sizes = [50, 25, 50, 25, 50, 50, 50]
def draw_text(text, font, color, max_size, index_size, x, y, screen):
    global font_sizes
    font = pygame.font.Font("resources/fonts/" + font + ".ttf", font_sizes[index_size])    
    label = font.render(text, 1, color)
    while(label.get_rect().width > max_size):
        font_sizes[index_size] = font_sizes[index_size] - 1
        font = pygame.font.SysFont("monospace", font_sizes[index_size])
        label = font.render(text, 1, color)
    # pygame.draw.rect(screen, (57,57,64), (x - label.get_rect().width // 2, y, label.get_rect().width,label.get_rect().height))
    screen.blit(label, (x - label.get_rect().width // 2,y))
    
def draw_scores(p1name, score1, image1, p2name, score2, image2, window_width, window_height, screen, player1_is_alive, player2_is_alive, moves1, miss1, moves2, miss2, stuck1, stuck2):
    if player1_is_alive:
        draw_text("Score: "+str(score1), "Kalam-Bold", (50,50,50), window_width / 6, 0, int(window_width / 12), window_width / 3 + 50, screen)
        draw_text(p1name, "Kalam-Bold", (50,50,50), window_width / 6, 5, int(window_width / 12), window_width / 3, screen)
        draw_text("Moves: " + str(moves1), "Kalam-Regular", (2,118,137), window_width / 6, 1, int(window_width / 12), window_width / 3 + 150, screen)
        draw_text("Miss: " + str(miss1), "Kalam-Regular", (229,35,64), window_width / 6, 1, int(window_width / 12), window_width / 3 + 180, screen)
        draw_text("Mud: " + str(stuck1), "Kalam-Regular", (229,35,64), window_width / 6, 1, int(window_width / 12), window_width / 3 + 210, screen)
    if player2_is_alive:
        draw_text("Score: "+str(score2), "Kalam-Bold", (50,50,50), window_width / 6, 2, int(11 * window_width / 12), window_width / 3 + 50, screen)
        draw_text(p2name, "Kalam-Bold", (50,50,50), window_width / 6, 6, int(11 * window_width / 12), window_width / 3, screen)
        draw_text("Moves: " + str(moves2), "Kalam-Regular", (2,118,137), window_width / 6, 3, int(11 * window_width / 12), window_width / 3 + 150, screen)
        draw_text("Miss: " + str(miss2), "Kalam-Regular", (229,35,64), window_width / 6, 3, int(11 * window_width / 12), window_width / 3 + 180, screen)
        draw_text("Mud: " + str(stuck2), "Kalam-Regular", (229,35,64), window_width / 6, 3, int(11 * window_width / 12), window_width / 3 + 210, screen)    

def display_exit():
    pygame.quit()

def play(q_out, move):
    while not q_out.empty():
        q_out.get()
    q_out.put(move)

def init_coords_and_images(width, height, player1_is_alive, player2_is_alive, window_width, window_height):

    scale = int(min((window_height - 50) / height, window_width * 2/3 / width))
    offset_x = window_width // 2 - int(width / 2 * scale)
    offset_y = max(25, window_height // 2 - int(scale * height / 2))
    scale_portrait_w = int(window_width / 6)
    scale_portrait_h = int(window_width / 6)

    image_background = pygame.transform.smoothscale(pygame.image.load("resources/illustrations/background.jpg"),(window_width, window_height))
    image_cheese = pygame.transform.smoothscale(pygame.image.load("resources/gameElements/cheese.png"),(scale, scale))
    image_corner = pygame.transform.smoothscale(pygame.image.load("resources/gameElements/corner.png"),(scale, scale))
    image_moving_python = pygame.transform.smoothscale(pygame.image.load("resources/gameElements/movingPython.png"),(scale, scale))
    image_moving_rat = pygame.transform.smoothscale(pygame.image.load("resources/gameElements/movingRat.png"),(scale, scale))
    image_python = pygame.transform.smoothscale(pygame.image.load("resources/gameElements/python.png"),(scale, scale))
    image_rat = pygame.transform.smoothscale(pygame.image.load("resources/gameElements/rat.png"),(scale, scale))
    image_wall = pygame.transform.smoothscale(pygame.image.load("resources/gameElements/wall.png"),(scale, scale))
    image_mud = pygame.transform.smoothscale(pygame.image.load("resources/gameElements/mud.png"),(scale, scale))
    image_portrait_python = pygame.transform.smoothscale(pygame.image.load("resources/illustrations/python_left.png"),(scale_portrait_w, scale_portrait_h))
    image_portrait_rat = pygame.transform.smoothscale(pygame.image.load("resources/illustrations/rat.png"),(scale_portrait_w, scale_portrait_h))
    image_tile = []
    for i in range(10):
        image_tile.append(pygame.transform.smoothscale(pygame.image.load("resources/gameElements/tile"+str(i+1)+".png"),(scale, scale)))
    tiles = []
    for i in range(width):
        tiles.append([])
        for j in range(height):
            tiles[i].append(random.randrange(10))

    if not(args.save_images):
        if not(player1_is_alive):
            image_rat = image_rat.convert()
            image_rat.set_alpha(0)
            image_moving_rat = image_moving_rat.convert()
            image_moving_rat.set_alpha(0)
        if not(player2_is_alive):
            image_python = image_python.convert()
            image_python.set_alpha(0)
            image_moving_python = image_moving_python.convert()
            image_moving_python.set_alpha(0)
    return scale, offset_x, offset_y, image_background, image_cheese, image_corner, image_moving_python, image_moving_rat, image_python, image_rat, image_wall, image_mud, image_portrait_python, image_portrait_rat, tiles, image_tile

def build_background(screen, maze, tiles, image_background, image_tile, image_wall, image_corner, image_mud, offset_x, offset_y, width, height, window_width, window_height, image_portrait_rat, image_portrait_python, scale, player1_is_alive, player2_is_alive):
    global font_sizes
    # screen.fill((57,57,64))
    font_sizes = [50, 25, 50, 25, 50, 50, 50]
    maze_image = screen.copy()
    maze_image.blit(image_background, (0,0))
    image_of_maze(maze, tiles, image_tile, image_wall, image_corner, image_mud, offset_x, offset_y, scale, width, height, maze_image, window_height)
    

    if player1_is_alive:
        maze_image.blit(image_portrait_rat, (int(window_width /12 - image_portrait_python.get_rect().width / 2), 100))
    if player2_is_alive:
        maze_image.blit(image_portrait_python, (int(window_width * 11 / 12 - image_portrait_python.get_rect().width / 2), 100))
    return maze_image

    
def run(maze, width, height, q, q_render_in, q_quit, p1name, p2name, q1_out, q2_out, is_human_rat, is_human_python, q_info, pieces_of_cheese, player1_location, player2_location, player1_is_alive, player2_is_alive, screen, infoObject):
    global args

    debug("Starting rendering",2)
    if args.save_images:
        window_width, window_height = args.window_width, args.window_height
    else:
        window_width, window_height = pygame.display.get_surface().get_size()
    turn_time = args.turn_time
    scale, offset_x, offset_y, image_background, image_cheese, image_corner, image_moving_python, image_moving_rat, image_python, image_rat, image_wall, image_mud, image_portrait_python, image_portrait_rat, tiles, image_tile = init_coords_and_images(width, height, player1_is_alive, player2_is_alive, window_width, window_height)

    debug("Defining constants",2)
    d = 10000000
    clock = pygame.time.Clock()
    new_player1_location = player1_location
    new_player2_location = player2_location
    time_to_go1 = pygame.time.get_ticks()
    time_to_go2 = pygame.time.get_ticks()
    score1 = 0
    score2 = 0
    image1 = image_rat
    image2 = image_python
    moves1 = 0
    moves2 = 0
    miss1 = 0
    miss2 = 0
    stuck1 = 0
    stuck2 = 0

    debug("Trying to initialize Joystick",2)
    pygame.joystick.init()
    try:
        j0 = pygame.joystick.Joystick(0)
        j0.init()
        print('Enabled joystick: ' + j0.get_name() + ' with ' + str(j0.get_numaxes()) + ' axes', file=sys.stderr)
        j1 = pygame.joystick.Joystick(1)
        j1.init()
        print('Enabled joystick: ' + j1.get_name() + ' with ' + str(j1.get_numaxes()) + ' axes', file=sys.stderr)
    except pygame.error:        
        ()

    debug("Building background image",2)
    maze_image = build_background(screen, maze, tiles, image_background, image_tile, image_wall, image_corner, image_mud, offset_x, offset_y, width, height, window_width, window_height, image_portrait_rat, image_portrait_python, scale, player1_is_alive, player2_is_alive)

    starting_time = pygame.time.get_ticks()

    text_info = ""

    debug("Starting main loop",2)
    while q_quit.empty() or (args.desactivate_animations and not(q.empty())):
        debug("Checking events",2)
        if not(args.save_images):
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
                    q_quit.put("")
                    break
                if event.type == pygame.VIDEORESIZE or (event.type == pygame.KEYDOWN and event.key == pygame.K_f):
                    if event.type == pygame.KEYDOWN and not(screen.get_flags() & 0x80000000):
                        screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
                        window_width, window_height = infoObject.current_w, infoObject.current_h
                    else:
                        if event.type == pygame.VIDEORESIZE:
                            window_width, window_height = event.w, event.h
                            screen = pygame.display.set_mode((window_width, window_height),pygame.RESIZABLE)
                            scale, offset_x, offset_y, image_background, image_cheese, image_corner, image_moving_python, image_moving_rat, image_python, image_rat, image_wall, image_mud, image_portrait_python, image_portrait_rat, tiles, image_tile = init_coords_and_images(width, height, player1_is_alive, player2_is_alive, window_width, window_height)
                            maze_image = build_background(screen, maze, tiles, image_background, image_tile, image_wall, image_corner, image_mud, offset_x, offset_y, width, height, window_width, window_height, image_portrait_rat, image_portrait_python, scale, player1_is_alive, player2_is_alive)

                if event.type == pygame.KEYDOWN and (is_human_rat or is_human_python):                
                    if event.key == pygame.K_LEFT:
                        play(q1_out, "L")
                    if event.key == pygame.K_RIGHT:
                        play(q1_out, "R")
                    if event.key == pygame.K_UP:
                        play(q1_out, "U")
                    if event.key == pygame.K_DOWN:
                        play(q1_out, "D")
                    if event.key == pygame.K_KP4:
                        play(q2_out, "L")
                    if event.key == pygame.K_KP6:
                        play(q2_out, "R")
                    if event.key == pygame.K_KP8:
                        play(q2_out, "U")
                    if event.key == pygame.K_KP5:
                        play(q2_out, "D")

        debug("Processing joysticks",2)
        try:
            x , y = j0.get_axis(3), j0.get_axis(4)
            if x < -0.7:
                play(q1_out, "L")
            if x > 0.7:
                play(q1_out, "R")
            if y < -0.7:
                play(q1_out, "U")
            if y > 0.7:
                play(q1_out, "D")
        except:
            ()
        try:
            x , y = j1.get_axis(3), j1.get_axis(4)
            if x < -0.7:
                play(q2_out, "L")
            if x > 0.7:
                play(q2_out, "R")
            if y < -0.7:
                play(q2_out, "U")
            if y > 0.7:
                play(q2_out, "D")
        except:
            ()
        debug("Looking for updates from core program",2)
        if (args.desactivate_animations and not(q.empty())) or not(args.desactivate_animations):
            if args.desactivate_animations:
                pieces_of_cheese, nnew_player1_location, nnew_player2_location, score1, score2, moves1, moves2, miss1, miss2, stuck1, stuck2 = q.get()
                player1_location = nnew_player1_location
                player2_location = nnew_player2_location
            else:
                while not(q.empty()):
                    pieces_of_cheese, nnew_player1_location, nnew_player2_location, score1, score2, moves1, moves2, miss1, miss2, stuck1, stuck2 = q.get()
                    if not(args.desactivate_animations):
                        if nnew_player1_location != new_player1_location:
                            time_to_go1 = pygame.time.get_ticks() + turn_time * maze[new_player1_location][nnew_player1_location]
                            player1_location = new_player1_location
                        if nnew_player2_location != new_player2_location:
                            player2_location = new_player2_location
                            time_to_go2 = pygame.time.get_ticks() + turn_time * maze[new_player2_location][nnew_player2_location]
                    new_player1_location = nnew_player1_location
                    new_player2_location = nnew_player2_location
                
            debug("Starting draw",2)
            screen.fill((57, 57, 64))
            screen.blit(maze_image, (0, 0))
            draw_pieces_of_cheese(pieces_of_cheese, image_cheese, offset_x, offset_y, scale, width, height, screen, window_height)

            if not(args.desactivate_animations):
                if time_to_go1 <= pygame.time.get_ticks() or player1_location == new_player1_location:
                    player1_location = new_player1_location
                    player1_draw_location = player1_location
                else:
                    prop = (time_to_go1 - pygame.time.get_ticks()) / (maze[player1_location][new_player1_location] * turn_time)
                    i, j = player1_location
                    ii, jj = new_player1_location
                    player1_draw_location = i * prop + ii * (1 - prop), j * prop + jj * (1 - prop)
                    if ii > i:
                        image1 = pygame.transform.rotate(image_moving_rat, 270)
                    elif ii < i:
                        image1 = pygame.transform.rotate(image_moving_rat, 90)
                    elif j < jj:
                        image1 = pygame.transform.rotate(image_moving_rat, 0)
                    else:
                        image1 = pygame.transform.rotate(image_moving_rat, 180)
                if time_to_go2 <= pygame.time.get_ticks() or player2_location == new_player2_location:
                    player2_location = new_player2_location
                    player2_draw_location = player2_location
                else:
                    prop = (time_to_go2 - pygame.time.get_ticks()) / (maze[player2_location][new_player2_location] * turn_time)
                    i, j = player2_location
                    ii, jj = new_player2_location
                    player2_draw_location = i * prop + ii * (1 - prop), j * prop + jj * (1 - prop)
                    if ii > i:
                        image2 = pygame.transform.rotate(image_moving_python, 270)
                    elif ii < i:
                        image2 = pygame.transform.rotate(image_moving_python, 90)
                    elif j < jj:
                        image2 = pygame.transform.rotate(image_moving_python, 0)
                    else:
                        image2 = pygame.transform.rotate(image_moving_python, 180)
                draw_players_animate(player1_draw_location, player2_draw_location, image1, image2, offset_x, offset_y, scale, width, height, screen, window_height)
            else:#if desactivate_animations
                draw_players(player1_location, player2_location, image_rat, image_python, offset_x, offset_y, scale, width, height, screen, window_height)
            draw_scores(p1name, score1, image_portrait_rat, p2name, score2, image_portrait_python, window_width, window_height, screen, player1_is_alive, player2_is_alive, moves1, miss1, moves2, miss2, stuck1, stuck2)
            if not(q_info.empty()):
                text_info = q_info.get()
            if text_info != "":
                draw_text(text_info, "Kalam-Bold", (50,50,50), window_width, 4, window_width // 2, 25, screen)
            if (pygame.time.get_ticks() - starting_time < args.preparation_time) and not(args.desactivate_animations):
                remaining = args.preparation_time - pygame.time.get_ticks() + starting_time
                if remaining > 0:
                    draw_text("Starting in " + str(remaining // 1000) + "." + (str(remaining % 1000)).zfill(3), "Kalam-Bold", (50,50,50), window_width, 4, window_width // 2, 25, screen)

            debug("Drawing on screen",2)
            if not(args.save_images):
                pygame.display.flip()
            if not(args.desactivate_animations):
                clock.tick(60)
            else:
                if not(args.synchronous):                
                    clock.tick(1000/turn_time)
            if args.save_images:
                pygame.image.save(screen, "output_images/image" + str(d)[1:] + ".png")
                d = d + 1
        else:
            clock.tick(60)
    debug("Exiting rendering", 2)
    q_render_in.put("quit")
    if is_human_python:
        q2_out.put("")
    if is_human_rat:
        q1_out.put("")


