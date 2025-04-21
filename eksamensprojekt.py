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
active_circles = None
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
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, circle in enumerate(circles):
                    x, y, r = circle
                    if (event.pos[0] - x) ** 2 + (event.pos[1] - y) ** 2 <= r ** 2:
                        active_circles = num


        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                active_circles = None

        if event.type == pg.MOUSEMOTION:
            if active_circles != None:
                x, y, r = circles[active_circles]
                circles[active_circles] = (x + event.rel[0], y + event.rel[1], r)

                # If the first circle is moved, adjust the second circle
                #if active_circles == 0 and len(circles) > 1:
                #    x1, y1, r1 = circles[0]
                #    x2, y2, r2 = circles[1]

                    # Calculate the angle between the two circles
                #    angle = math.atan2(y2 - y1, x2 - x1)

                    # Update the second circle's position to maintain the desired distance
                #    x2 = x1 + math.cos(angle) * line_distance
                #    y2 = y1 + math.sin(angle) * line_distance
                #    circles[1] = (x2, y2, r2)

                    



    # Drawing
    screen.fill((200, 200, 200))

    # Draw circles
    for circle in circles:
        x, y, r = circle
        pg.draw.circle(screen, (250, 250, 250), (x, y), r, 3)
        pg.draw.circle(screen, (100, 100, 100), (x, y), r/2)

    
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

