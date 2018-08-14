'''
    Still an early version of this "game". I've only made it because I was really bored... to the point of actually
    being painful. So here I am, explaining myself why I made a game where Hitler is being followed by some randomly coloured,
    AI powered balls.
    The AI part is actually a genetic algorithm and a way for the balls to follow you around if you approach them too much.
    You control your character with the arrow keys.
    The goal is to survive as much as possible.
    Sometimes, ball might spawn on top of you and you'll lose instantly. Just restart the game.

'''


import pygame
import random
import character
import time
from character import reproduce
from math import sqrt
from math import pow

pygame.init()

display_width = 800  # dimensions
display_height = 600

# colour definitions

black = (0, 0, 0)
white = (255, 255, 255)


# main character, controlled by player
vilImg = pygame.image.load('villain.png') # the title is as it is, because I wanted to make it the 'villain' at first


def chr(x, y, display):
    display.blit(vilImg, (x, y))


# setting up the display (the window of the game)
gameDisplay = pygame.display.set_mode((display_width, display_height))  # canvas; display size
pygame.display.set_caption('A bit too random')  # title
clock = pygame.time.Clock()  # game clock


# name of function -- self explanatory
def create_npc(how_many):
    npc = []
    for _ in range(how_many):
        x = random.randrange(0, display_width)
        y = random.randrange(0, display_height)
        radius = random.randrange(5, 20)
        dude = character.Characters(x, y, x_speed=random.randrange(2, 5), y_speed=random.randrange(2, 5),radius=radius)
        npc.append(dude)
    return npc


def get_chr_center(x_character,y_character,width,height):
    x = x_character + width/2
    y = y_character + height/2
    return x, y


# euclidian distance
def get_distance(x1, y1, x2, y2):
    '''
    :param x1: x coord of first object
    :param y1: y coord of fist object
    :param x2: x coord of second object
    :param y2: y coord of second object
    :return: the distance between obj1 and obj2
    '''
    return sqrt(pow((x2-x1), 2) + pow((y2-y1), 2))


# functions to display text on screen
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()


# simple message for game over
def crash():
    message_display('You ded')


def display_score(score):
    largeText = pygame.font.Font('freesansbold.ttf', 80)
    TextSurf, TextRect = text_objects('Score: ' + str(score), largeText)
    TextRect.center = ((display_width/2),(display_height/2 + 75))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)


npcs = create_npc(5)  # start off with n enemies; can be a future feature of the game, where the starting number differs by difficulty

# determines the spawn point of the player
x = random.randrange(0,700)
y = random.randrange(0,500)


x_change = 0
y_change = 0
x_prev = 0
y_prev = 0
speed = 0

dead = False
now = time.time()
t = 0
score = 0

while not dead:
    t += 1
    new_bullet = character.Bullet(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = True

        # movement of character
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -5
            if event.key == pygame.K_RIGHT:
                x_change = 5
            if event.key == pygame.K_UP:
                y_change = -5
            if event.key == pygame.K_DOWN:
                y_change = 5
            if event.key == pygame.K_SPACE:
                new_bullet.draw_bullet(gameDisplay, x, y)
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            x_change = 0
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            y_change = 0

    x += x_change
    y += y_change

    if x > display_width - 20 or x <= 10:
        x_change = 0
    if y > display_height - 45 or y <= 10:
        y_change = 0
    gameDisplay.fill(white)
    for i in range(len(npcs)):
        # making the npcs move in relatively random directions
        # and other controls of the npcs

        if npcs[i].y > display_height - npcs[i].radius or npcs[i].y < 10:
            npcs[i].y_speed = -npcs[i].y_speed
        if npcs[i].x > display_width - npcs[i].radius or npcs[i].x < 10:
            npcs[i].x_speed = -npcs[i].x_speed

        # this is basically where it takes the decision whether or not to follow the player

        x_Center, y_Center = get_chr_center(x, y, 25, 50) # center point of character model
        if get_distance(x_Center, y_Center, npcs[i].x, npcs[i].y) <= 100:
            npcs[i].move_towards_player(x, y)
            npcs[i].set_speed(5,5)
        else:
            npcs[i].x += npcs[i].x_speed
            npcs[i].y += npcs[i].y_speed

        # checks for collisions

        d = get_distance(x_Center, y_Center, npcs[i].x, npcs[i].y)
        a = sqrt((2500/4 + 625/4)) + npcs[i].radius
        if d >= npcs[i].radius + (25/2) and d <= a:
            print('Crash')
            crash()
            display_score(score)
            time.sleep(1)
            pygame.quit()
            quit()


        npcs[i].draw(gameDisplay, npcs[i].x, npcs[i].y)

    npcs = sorted(npcs, key=lambda x: x.score)

    new_now = time.time()
    if t == 400:
        child = reproduce(npcs[0],npcs[1])
        npcs.append(child)
        t = 0
        score += 1

    chr(x, y, gameDisplay)
    x_prev = x
    y_prev = y
    font = pygame.font.Font(None, 14)
    text = font.render('Score: ' + str(score), 3, black)
    gameDisplay.blit(text,(0,0))
    pygame.display.update()
    clock.tick(60)
pygame.quit()
quit()
