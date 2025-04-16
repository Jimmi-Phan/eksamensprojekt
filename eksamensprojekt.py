import pygame as pg
import random

pg.init()

screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

active_circles = None
circles = []
for i in range(1):
    x = 50
    y = 50
    r = 50
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
                    x, y, radius = circle
                    if (event.pos[0] - x) ** 2 + (event.pos[1] - y) ** 2 <= radius ** 2:
                        active_circles = num


        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                active_circles = None

        if event.type == pg.MOUSEMOTION:
            if active_circles != None:
                x, y, radius = circles[active_circles]
                circles[active_circles] = (x + event.rel[0], y + event.rel[1], radius)
                        



    # Drawing
    screen.fill((128, 128, 128))
    for circle in circles:
        x, y, radius = circle
        pg.draw.circle(screen, (255, 0, 0), (x, y), radius)
    pg.display.flip()
