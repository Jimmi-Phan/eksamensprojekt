import pygame as pg
import random
import math
import walls

pg.init()

screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

screen_width, screen_height = pg.display.get_window_size()
line_distance = 150

round = -1

lives = 3

hole_size = 50

in_game = False

joints = 7 # number o balls

difficulty = 5+1 # seconds on timer

color_of_balls = (150, 150, 150)

## Varibales ##
# startbutton
startbutton_x = screen_width*0.0175
startbutton_y = screen_height*0.1
startbutton_width = screen_width*(0.2-0.0175)-startbutton_x
startbutton_height = screen_height*0.3-startbutton_y

# nextbutton
nextbutton_x = screen_width*0.0175
nextbutton_y = screen_height*0.4
nextbutton_width = screen_width*(0.2-0.0175)-nextbutton_x
nextbutton_height = screen_height*0.6-nextbutton_y

# optionsbutton
optionsbutton_x = screen_width*0.0175
optionsbutton_y = screen_height*0.7
optionsbutton_width = screen_width*(0.2-0.0175)-optionsbutton_x
optionsbutton_height = screen_height*0.9-optionsbutton_y

## Timer ##
clock = pg.time.Clock()
counter = 0
timer = str(counter)
pg.time.set_timer(pg.USEREVENT, 1000)
a = 75
font = pg.font.Font(None, a)

## Circles ##
active_circle = None
circles = []
starting_coords = [
    ((screen_width/2), (screen_height/2)+line_distance), #0
    ((screen_width/2-(math.sqrt(2)*(line_distance/2))), (screen_height/2)+line_distance+(math.sqrt(2)*(line_distance/2))), #1
    ((screen_width/2+(math.sqrt(2)*(line_distance/2))), (screen_height/2)+line_distance+(math.sqrt(2)*(line_distance/2))), #2
    ((screen_width/2), (screen_height/2)), #3
    ((screen_width/2)-line_distance, (screen_height/2)), #4
    ((screen_width/2)+line_distance, (screen_height/2)), #5
    ((screen_width/2), (screen_height/2)-(line_distance/3)), #6
]


hole = []
walls = [walls.wall0, walls.wall1, walls.wall2, walls.wall3, walls.wall4]
random.shuffle(walls)

for i in range(joints):
    x1, y2,  = starting_coords[i]
    r = 20
    circles.append((x1, y2, r))

    x2, y2 = walls[round+1][i]
    r = 20
    hole.append((x2, y2, r))

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

def fit_check(round):
    win_check = 0
    for i in range(joints):
        x1, y1, r = circles[i]
        x2, y2 = walls[round][i]
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        if distance + r > hole_size: # if failed
            return False
    return True

def make_hole():
    hole.clear()
    for i in range(joints):
        x2, y2 = walls[round][i]
        r = 20
        hole.append((x2, y2, r))

def get_coords():
    coords = []
    for i in range(joints):
        x, y, r = circles[i]
        coords.append((x, y))

        print(f"(({x}),({y})),")
    return coords

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
        ## Timer ##
        if event.type == pg.USEREVENT:
            if in_game == True:
                counter -= 1
                if counter > 0:
                    timer = str(counter)
                else:
                    if fit_check(round) == True:
                        timer = "You win!"
                        in_game = False
                    else:
                        timer = "You lose!"
                        in_game = False
                        lives -= 1
        
        # Buttons
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                for i in range(joints):
                    x, y = starting_coords[i]
                    r = 20
                    circles[i] = (x, y, r)
            if event.key == pg.K_3:
                get_coords()
            # dev tool
            keys = pg.key.get_pressed()
            if keys[pg.K_j] and keys[pg.K_i] and keys[pg.K_m]:
                for i in range(joints):
                    x, y = walls[round][i]
                    r = 20
                    circles[i] = (x, y, r)

        ## NO ELONGATED LINES ##
        # mouse leftclick check
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, circle in enumerate(circles):
                    x, y, r = circle
                    if (event.pos[0] - x) ** 2 + (event.pos[1] - y) ** 2 <= r ** 2:
                        active_circle = num
                if pg.mouse.get_pos()[0] < startbutton_x + startbutton_width and pg.mouse.get_pos()[0] > startbutton_x and pg.mouse.get_pos()[1] < startbutton_y + startbutton_height and pg.mouse.get_pos()[1] > startbutton_y and in_game == False:
                    round += 1
                    make_hole()
                    in_game = True
                    counter = difficulty
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
    temp_range1, temp_range2, temp_range3 = (0, 6,1)
    if active_circle in (2,5):
        temp_range1, temp_range2, temp_range3 = (5, -1, -1)
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
    # if (abs(angle-angle2)) > 0.75: ctrl + '
    #     if angle > angle2:
    #         overlap = 0.6
    #         x3 += math.cos(angle2) * overlap
    #         y3 += math.sin(angle2) * overlap
            
    #         circles[6] = (x3, y3, r3)
    #     else:
    #         overlap = 0.6
    #         x3 -= math.cos(angle) * overlap
    #         y3 -= math.sin(angle) * overlap
            
    #         circles[6] = (x3, y3, r3)



    ## Drawing
    screen.fill((200, 200, 200))

    if in_game == True:
        # Draw hole
        for i, circle in enumerate(hole):
            x, y, r = circle
            if i == 6:  
                r += 20
            pg.draw.circle(screen, (50, 50, 50), (x, y), r)

        # Draw lines between circles
        for i in range(6):
            if i < 3:
                if len(hole) >= 2:
                    x1, y1, _ = hole[0]
                    x2, y2, _ = hole[1+i]
                    pg.draw.line(screen, (50, 50, 50), (x1, y1), (x2, y2), 27)
            else:
                if len(hole) >= 2:
                    x1, y1, _ = hole[3]
                    x2, y2, _ = hole[1+i]
                    pg.draw.line(screen, (50, 50, 50), (x1, y1), (x2, y2), 27)


    # Draw circles
    for i, circle in enumerate(circles):
        x, y, r = circle
        if i == 6:
            r = 40
        pg.draw.circle(screen, (250, 250, 250), (x, y), r, 3)
        pg.draw.circle(screen, color_of_balls, (x, y), r-10)

    # Draw lines between circles
    for i in range(6):
        if i < 3:
            if len(circles) >= 2:
                x1, y1, _ = circles[0]
                x2, y2, _ = circles[1+i]
                pg.draw.line(screen, color_of_balls, (x1, y1), (x2, y2), 17)
        else:
            if len(circles) >= 2:
                x1, y1, _ = circles[3]
                x2, y2, _ = circles[1+i]
                pg.draw.line(screen, color_of_balls, (x1, y1), (x2, y2), 17)
    

    pg.draw.rect(screen,(100, 100, 100),pg.Rect(0,0,(screen_width*0.2),(screen_height)))
    pg.draw.rect(screen,(100, 100, 100),pg.Rect((screen_width*0.8),0,(screen_width),(screen_height)))

    ## Draw text

    # timer
    text_surface = font.render("Countdown", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=((screen_width*0.9), (screen_height*0.175)))
    screen.blit(text_surface, text_rect)
    text_surface = font.render(timer if round > -1 else "Not In Game", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=((screen_width*0.9), (screen_height*0.25)))
    screen.blit(text_surface, text_rect)

    # round
    text_surface = font.render("Round", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=((screen_width*0.9), (screen_height*0.475)))
    screen.blit(text_surface, text_rect)
    text_surface = font.render(str(round) if round > -1 else "Not In Game", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=((screen_width*0.9), (screen_height*0.55)))
    screen.blit(text_surface, text_rect)

    # lives
    text_surface = font.render("Lives", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=((screen_width*0.9), (screen_height*0.75)))
    screen.blit(text_surface, text_rect)
    text_surface = font.render(str(lives) if round > -1 else "Not In Game", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=((screen_width*0.9), (screen_height*0.825)))
    screen.blit(text_surface, text_rect)

    ## Draw buttons

    # startbutton
    pg.draw.rect(screen,(50,50,50),pg.Rect(startbutton_x, startbutton_y,startbutton_width,startbutton_height))
    text_surface = font.render("Start", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(startbutton_x+startbutton_width/2, startbutton_y+startbutton_height/2))
    screen.blit(text_surface, text_rect)

    # nextbutton
    pg.draw.rect(screen,(50,50,50),pg.Rect(nextbutton_x, nextbutton_y,nextbutton_width,nextbutton_height))
    text_surface = font.render("Next", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(nextbutton_x+nextbutton_width/2, nextbutton_y+nextbutton_height/2))
    screen.blit(text_surface, text_rect)

    # optionsbutton
    pg.draw.rect(screen,(50,50,50),pg.Rect(optionsbutton_x, optionsbutton_y,optionsbutton_width,optionsbutton_height))
    text_surface = font.render("Options", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(optionsbutton_x+optionsbutton_width/2, optionsbutton_y+optionsbutton_height/2))
    screen.blit(text_surface, text_rect)
    pg.display.flip()