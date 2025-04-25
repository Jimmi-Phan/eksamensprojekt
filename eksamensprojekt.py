import pygame as pg
import random
import math

pg.init()

screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

screen_width, screen_height = pg.display.get_window_size()

## Timer ##
clock = pg.time.Clock()
font = pg.font.Font(None, 100)
counter = 10
text = font.render(str(counter), True, (0, 0, 0))

## Circles ##
line_distance = 150
active_circle = None
circles = []
starting_coords = [
    ((screen_width/2), (screen_height/2)+line_distance), #0
    ((screen_width/2-106.07), (screen_height/2)+line_distance+106.07), #1
    ((screen_width/2+106.07), (screen_height/2)+line_distance+106.07), #2
    ((screen_width/2), (screen_height/2)), #3
    ((screen_width/2)-line_distance, (screen_height/2)), #4
    ((screen_width/2)+line_distance, (screen_height/2)), #5
    ((screen_width/2), (screen_height/2)-line_distance), #6
]

for i in range(7):
    x, y = starting_coords[i]
    r = 20
    circles.append((x, y, r))

## Functions ##
def no_elongate(circle_number, i):
    x1, y1, r1 = circles[circle_number]
    x2, y2, r2 = circles[i]

    # angle between the two circles
    angle = math.atan2(y2 - y1, x2 - x1)

    # move second circle
    x2 = x1 + math.cos(angle) * line_distance
    y2 = y1 + math.sin(angle) * line_distance
    circles[i] = (x2, y2, r2)

## Game Loop ##
running = True
while running:

    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
        
        ## NO ELONGATED LINES ##
        # mouse leftclick check
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, circle in enumerate(circles):
                    x, y, r = circle
                    if (event.pos[0] - x) ** 2 + (event.pos[1] - y) ** 2 <= r ** 2:
                        active_circle = num

        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                active_circle = None
        # mouse movement check
        if event.type == pg.MOUSEMOTION:
            if active_circle != None:
                # chain reation movement
                x, y, r = circles[active_circle]
                circles[active_circle] = (x + event.rel[0], y + event.rel[1], r)
                # If #0 circle is moved
                if active_circle == 0:
                    for i in range(1,4):
                        no_elongate(0, i)
                        if i == 3:
                            for i in range(4,7):
                                no_elongate(3, i)
                # If #3 circle is moved
                if active_circle == 3:
                    for i in range(4,8):
                        if i != 7:
                            no_elongate(3, i)
                        else:
                            for i in range(0,1): # i = 0
                                no_elongate(3, i)
                                if i == 0:
                                    for i in range(1,4):
                                        no_elongate(0, i)
                # If #1 circle is moved
                if active_circle == 1:
                    for i in range(0,1): # i = 0
                        no_elongate(1, i)
                        for i in range(1,4):
                            no_elongate(0, i)
                            for i in range(4,7):
                                no_elongate(3, i)
                # If #2 circle is moved
                if active_circle == 2:
                    for i in range(0,1): # i = 0
                        no_elongate(2, i) 
                        for i in range(1,4):
                            no_elongate(0, i)
                            for i in range(4,7):
                                no_elongate(3, i)
                # If #4 circle is moved
                if active_circle == 4:
                    for i in range(3,4): # i = 3
                        no_elongate(4, i)
                        for i in range(4,8):
                            if i != 7:
                                no_elongate(3, i)
                            else:
                                for i in range(0,1): # i = 0
                                    no_elongate(3, i)
                                    if i == 0:
                                        for i in range(1,4):
                                            no_elongate(0, i)
                if active_circle == 5:
                    for i in range(3,4): # i = 3
                        no_elongate(5, i)
                        for i in range(4,8):
                            if i != 7:
                                no_elongate(3, i)
                            else:
                                for i in range(0,1): # i = 0
                                    no_elongate(3, i)
                                    if i == 0:
                                        for i in range(1,4):
                                            no_elongate(0, i)
                if active_circle == 6:
                    for i in range(3,4): # i = 3
                        no_elongate(6, i)
                        for i in range(4,8):
                            if i != 7:
                                no_elongate(3, i)
                            else:
                                for i in range(0,1): # i = 0
                                    no_elongate(3, i)
                                    for i in range(1,4):
                                        no_elongate(0, i)


    ## Drawing
    screen.fill((200, 200, 200))

    # Draw circles
    for i, circle in enumerate(circles):
        x, y, r = circle
        if i == 6:
            r = 40
        pg.draw.circle(screen, (250, 250, 250), (x, y), r, 3)
        pg.draw.circle(screen, (100, 100, 100), (x, y), r-10)

    # Draw lines between circles
    for i in range(6):
        if i < 3:
            if len(circles) >= 2:
                x1, y1, _ = circles[0]
                x2, y2, _ = circles[1+i]  
                pg.draw.line(screen, (100, 100, 100), (x1, y1), (x2, y2), 17)
        else:
            if len(circles) >= 2:
                x1, y1, _ = circles[3]
                x2, y2, _ = circles[1+i]
                pg.draw.line(screen, (100, 100, 100), (x1, y1), (x2, y2), 17)

    pg.display.flip()

