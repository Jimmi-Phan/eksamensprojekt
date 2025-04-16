import pygame as pg
import random

pg.init()

screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

active_circles = None
circles = []
for i in range(3):
    x = 50+i * 100
    y = 50+i * 100
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
                        



    # Drawing
    screen.fill((128, 128, 128))

    # Draw circles
    for circle in circles:
        x, y, r = circle
        pg.draw.circle(screen, (50, 50, 50), (x, y), r)
        pg.draw.circle(screen, (100, 100, 100), (x, y), r/2)

    # Draw a line between the two circles
    if len(circles) >= 2:
        x1, y1, _ = circles[0]  # Center of the first circle
        x2, y2, _ = circles[1]  # Center of the second circle
        pg.draw.line(screen, (100, 100, 100), (x1, y1), (x2, y2), 18)

    pg.display.flip()

