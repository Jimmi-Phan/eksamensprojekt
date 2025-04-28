import pygame as pg
import random
import math

pg.init()

screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

screen_width, screen_height = pg.display.get_window_size()
line_distance = 150


## Timer ##
clock = pg.time.Clock()
font = pg.font.Font(None, 100)
counter = 10
text = font.render(str(counter), True, (0, 0, 0))

## Circles ##
active_circle = None
circles = []
starting_coords = [
    ((screen_width/2), (screen_height/2)+line_distance), #0
    ((screen_width/2-106.07), (screen_height/2)+line_distance+106.07), #1
    ((screen_width/2+106.07), (screen_height/2)+line_distance+106.07), #2
    ((screen_width/2), (screen_height/2)), #3
    ((screen_width/2)-line_distance, (screen_height/2)), #4
    ((screen_width/2)+line_distance, (screen_height/2)), #5
    ((screen_width/2), (screen_height/2)-(line_distance/3)), #6
    #((screen_width/2), (screen_height/2)-line_distance), #7
    #((screen_width/2), (screen_height/2)-line_distance), #8
    #((screen_width/2), (screen_height/2)-line_distance), #9
    #((screen_width/2), (screen_height/2)-line_distance) #10
]

for i in range(7):
    x, y = starting_coords[i]
    r = 20
    circles.append((x, y, r))

## Functions ##
def no_elongate(circle_number, i):
    if (circle_number == 3 and i == 6) or (circle_number == 6 and i == 3):
        distance1 = line_distance/3
    else:
        distance1 = line_distance
    x1, y1, r1 = circles[circle_number]
    x2, y2, r2 = circles[i]
    # angle between the two circles
    angle = math.atan2(y2 - y1, x2 - x1)
    # move second circle
    x2 = x1 + math.cos(angle) * distance1
    y2 = y1 + math.sin(angle) * distance1
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
                ## chain reation movement
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
    
    ## Collision prevention
    temp_range1, temp_range2, temp_range3 = (0, 7,1)
    if active_circle in (2,5):
        temp_range1, temp_range2, temp_range3 = (6, -1, -1)
    for i in range(temp_range1, temp_range2, temp_range3):
        for j in range(temp_range1, temp_range2, temp_range3):
            if i != j:
                x1, y1, r1 = circles[i]
                x2, y2, r2 = circles[j]
                distance2 = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                if distance2 < r1 + r2:
                    overlap = r1 + r2 - distance2
                    angle = math.atan2(y2 - y1, x2 - x1)
                    
                    x2 += math.cos(angle) * overlap
                    y2 += math.sin(angle) * overlap

                    circles[i] = (x1, y1, r1)
                    circles[j] = (x2, y2, r2)

    # Collision for #6 circle
    x1, y1, r1 = circles[0]
    x2, y2, r2 = circles[3]
    x3, y3, r3 = circles[6]
    angle = math.atan2(y2 - y1, x2 - x1) + 1.5707963267948966
    angle2 = math.atan2(y3 - y2, x3 - x2) + 1.5707963267948966
    print(angle, angle2)
    if (abs(angle-angle2)) > 0.75:
        if angle > angle2:
            overlap = 0.6
            x3 += math.cos(angle2) * overlap
            y3 += math.sin(angle2) * overlap
            
            circles[6] = (x3, y3, r3)
        else:
            overlap = 0.6
            x3 -= math.cos(angle) * overlap
            y3 -= math.sin(angle) * overlap
            
            circles[6] = (x3, y3, r3)



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

