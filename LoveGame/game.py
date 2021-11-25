import pygame
import random
import math
from pygame import mixer

pygame.init()

FPS = 60
fpsclock = pygame.time.Clock()

screen = pygame.display.set_mode((800,600))

# background
background = pygame.image.load('background.png')

# you
vuongImg = []
vuongX = []
vuongY = []
vuongX_change = []
vuongY_change = []
num_of_vuong = 5

for i in range(num_of_vuong):
    vuongImg.append(pygame.image.load('vuong.png'))
    vuongX.append(random.randint(0,735))
    vuongY.append(random.randint(20,150))
    vuongX_change.append(0.2)
    vuongY_change.append(20)

    def vuong(x,y,i):
        screen.blit(vuongImg[i],(x,y))

# your girl friend
thuyImg = pygame.image.load('thuy.png')
thuyX = 380
thuyY = 500
thuyX_change = 0
thuyY_change = 0

def thuy(x,y):
    screen.blit(thuyImg,(x,y))

# heart
heartImg = pygame.image.load('heart.png')
heartX = 0
heartY = thuyY
heartX_change = 0
heartY_change = 0.4

heart_state = "ready"

def heart(x,y):
    global heart_state
    heart_state = "fire"
    screen.blit(heartImg,(x+16,y+10))

# icon and title
title = pygame.display.set_caption("17-04-2020")
icon = pygame.image.load('heart.png')
pygame.display.set_icon(icon)

# check colision
def iscollision(vuongX,vuongY,heartX,heartY):
    distance = math.sqrt(math.pow(vuongX - heartX,2)+math.pow(vuongY - heartY,2))

    if distance < 27:
        return True
    else:
        return False

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Thuy love Vuong x " + str(score_value),True, (150,150,255))
    screen.blit(score,(x,y))

# Game over
over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over_text = over_font.render("You lost but I still love u" ,True, (150,150,255))
    screen.blit(over_text,(30,250))

# sound and music
mixer.music.load("until_you.wav")
mixer.music.play(-1)

running = True
while running:

    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                thuyX_change = 1
            if event.key == pygame.K_LEFT:
                thuyX_change = -1
            if event.key == pygame.K_UP:
                thuyY_change = -1
            if event.key == pygame.K_DOWN:
                thuyY_change = 1
            if event.key == pygame.K_SPACE:
                if heart_state == "ready":
                    heartX = thuyX
                    heartY = thuyY
                    heart(heartX,heartY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                thuyX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                thuyY_change = 0

    thuy(thuyX,thuyY)
    thuyX += thuyX_change
    thuyY += thuyY_change

    if thuyX <=0:
        thuyX = 0 
    elif thuyX >=736:
        thuyX = 736

    if thuyY <= 400: 
        thuyY = 400
    elif thuyY >=530:
        thuyY = 529

    for i in range(num_of_vuong):
        # game over
        if vuongY[i] > 200:
            for j in range(num_of_vuong):
                vuongY[j] =2000
            game_over_text()
            break

        vuong(vuongX[i],vuongY[i],i)

        if vuongX[i] <= 0:
            vuongX_change[i] = 0.2
            vuongY[i] += vuongY_change[i]
        if vuongX[i] >= 736:
            vuongX_change[i] = -0.2
            vuongY[i] += vuongY_change[i]

        vuongX[i] += vuongX_change[i]
           
        collision = iscollision(vuongX[i],vuongY[i],heartX,heartY)
        if collision:
            heart_state = "ready"
            vuongY[i] = random.randint(50,150)
            vuongX[i] = random.randint(0,735)
            score_value += 1
            explosion_sound = mixer.Sound('tick.wav')
            explosion_sound.play()

    if heartY <= 0:
        heartY = thuyY
        heart_state ="ready" 
    if heart_state == "fire":
        heartY -= heartY_change
        heart(heartX,heartY)

    show_score(textX,textY)
    fpsclock.tick()
    pygame.display.flip()
