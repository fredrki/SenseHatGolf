import pygame
import numpy as np
from spillfunksjoner import *
from sense_hat import SenseHat
import time

sense = SenseHat()
pygame.init()

clock = pygame.time.Clock()


nl = 0
tot_levels = 2
score = 0

level=np.array(nextlevel(nl))

holepos = []
pointpos = []

            

B=(255, 255, 255) #Ball
W=(128, 0, 0) # Wall
H=(0, 255, 0) # Hole
F=(255, 255, 0) # Finish
G=(0, 0, 0) # Ground

vx = 0
vy = 0

FPS = 60
step = 0

score=0

for i in range(8):
    for j in range(8):
        if level[i, j] == 1:
            bx = i
            by = j
        elif level[i, j] == 3:
            holepos.append([i, j])
        elif level[i, j] == -1:
            goalpos = [i, j]
        elif level[i,j] == 4:
            pointpos.append([i,j])



running = True


while running:
    clock.tick(FPS)

    xy = ori()
    x = xy[1]
    y = xy[0]

    print(f"x = {x}, y = {y}")

    if x > 1:
        vx = -1
    elif x < -1:
        vx = 1
    else:
        vx = 0

    if y > 1:
        vy = 1
    elif y < -1:
        vy = -1
    else:
        vy = 0

        
    
    
    level[bx, by] = 0 # Fjern gammel posisjon

    if vy != 0: # Sjekk kollisjon i y retning og beveg
        try: 
            if level[bx, by + vy] == 2 or by + vy == -1 or by + vy == 8:
                vy = 0
        except IndexError:
            vy = 0

        by += vy

    if vx != 0: # Sjekk kollisjon i x retning og beveg
        try:
            if level[bx + vx, by] == 2 or bx + vx == -1 or bx + vx == 8:
                vx = 0
        except IndexError:
            vx = 0
        bx += vx

    if [bx, by] in holepos:
        GAMEOVER(score)
        nl = 1
    if [bx,by] in pointpos:
        score+=100

        level=np.array(nextlevel(nl))

        holepos = []
        pointpos=[]

        for i in range(8):
            for j in range(8):
                if level[i, j] == 1:
                    bx = i
                    by = j
                elif level[i, j] == 3:
                    holepos.append([i, j])
                elif level[i, j] == -1:
                    goalpos = [i, j]
                elif level[i,j] == 4:
                    pointpos.append([i,j])


    
    if [bx, by] == goalpos: # Neste level
        nl += 1
        score += 100
        if nl > tot_levels:
            nl = 1
        level=np.array(nextlevel(nl))
   

        holepos = []
        pointpos=[]
        
        for i in range(8):
            for j in range(8):
                if level[i, j] == 1:
                    bx = i
                    by = j
                elif level[i, j] == 3:
                    holepos.append([i, j])
                elif level[i, j] == -1:
                    goalpos = [i, j]
                elif level[i,j] == 4:
                    pointpos.append([i,j])



    level[bx, by] = 1 # Oppdater posisjon


    for i in range(8):
        for j in range(8):
            if level[i, j]==1:
                sense.set_pixel(i, j, B)
            elif level[i,j]==2:
                sense.set_pixel(i,j,W)
            elif level[i,j]==3:
                sense.set_pixel(i,j,H)
            elif level[i,j]==-1:
                sense.set_pixel(i,j,F)
            else:
                sense.set_pixel(i,j,G)
        
print_score(score)
sense.clear()
