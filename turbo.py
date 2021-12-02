# Importerer brukte biblioteker
import pygame
import numpy as np
from spillfunksjoner import *
from sense_hat import SenseHat
import time

pygame.init() # Initialiserer koden

# Lager variabler for lettere tilkalling
clock = pygame.time.Clock()
sense = SenseHat()


# Konstanter
LEVELTOT = 3
FPS = 60

# Variabler
score = 0
nl = 0

level=np.array(nextlevel(nl))

holepos = []

            
# Farger
B=(255, 255, 255) #Ball
W=(128, 0, 0) # Wall
H=(0, 255, 0) # Hole
F=(255, 255, 0) # Finish
G=(0, 0, 0) # Ground

# Fart i x og y retning
vx = 0
vy = 0

# Variabler for telling av frames
xstep = 0
ystep = 0
cx = 0
cy = 0

# Henter posisjoner for alle ruter
for i in range(8):
    for j in range(8):
        if level[i, j] == 1:
            bx = i
            by = j
        elif level[i, j] == 3:
            holepos.append([i, j])
        elif level[i, j] == -1:
            goalpos = [i, j]


# Spillokka
running = True

while running:
    clock.tick(FPS) # Kjorer lokka FPS mange ganger per sekund, hoyere FPS gir mer noyaktige maalinger.

    # Henter orientasjonen fra SenseHat
    xy = ori() 
    x = xy[1]
    y = xy[0]

    # Her bestemmes det om ballen skal bevege seg i det hele tatt
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

    xstep = 10 - abs(int(x * 3))
    ystep = 10 - abs(int(y * 3))

    level[bx, by] = 0 # Fjern gammel posisjon

    if cy >= ystep:

        if vy != 0: # Sjekk kollisjon i y retning og beveg
            try: 
                if level[bx, by + vy] == 2 or by + vy == -1 or by + vy == 8:
                    vy = 0
            except IndexError:
                vy = 0

            by += vy
        cy = 0

    else:
        cy += 1

    if cx >= xstep:

        if vx != 0: # Sjekk kollisjon i x retning og beveg
            try:
                if level[bx + vx, by] == 2 or bx + vx == -1 or bx + vx == 8:
                    vx = 0
            except IndexError:
                vx = 0
            bx += vx
        cx = 0

    else:
        cx += 1


    if [bx, by] in holepos:
        GAMEOVER(score)
        nl = 1
        print_score(score)
        score = 0

        level=np.array(nextlevel(nl))

        holepos = []

        for i in range(8):
            for j in range(8):
                if level[i, j] == 1:
                    bx = i
                    by = j
                elif level[i, j] == 3:
                    holepos.append([i, j])
                elif level[i, j] == -1:
                    goalpos = [i, j]


    
    if [bx, by] == goalpos: # Neste level
        nl += 1
        score += 100
        if nl > LEVELTOT:
            nl = 1
            print_score(score)
            score = 0
        level=np.array(nextlevel(nl))
   

        holepos = []
        
        for i in range(8):
            for j in range(8):
                if level[i, j] == 1:
                    bx = i
                    by = j
                elif level[i, j] == 3:
                    holepos.append([i, j])
                elif level[i, j] == -1:
                    goalpos = [i, j]



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
