import pygame
from random import random as rand, randrange
from pygame.locals import *
from math import sqrt
from math import pow

BLUE = (0, 0, 255) # RGB value of the NPCs


# creating a random colour to asign to the balls
def random_colour():
    return randrange(100, 255), randrange(100, 255), randrange(100, 255)


class Characters:
    def __init__(self,x,y,x_speed,y_speed,radius):
        self.x = x
        self.y = y # the position
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.score = self.get_fitscore()
        self.radius = radius
        self.x_initial_speed = x_speed
        self.y_initial_speed = y_speed
        self.colour = (random_colour())

    def draw(self,display,x,y):
        pygame.draw.circle(display, self.colour, (int(x),int(y)),int(self.radius))

    def set_speed(self,new_x_speed,new_y_speed):
        if self.x_speed < 0:
            self.x_speed = -new_x_speed
        else:
            self.x_speed = new_x_speed

        if self.y_speed < 0:
            self.y_speed = -new_y_speed
        else:
            self.y_speed = new_y_speed

    def get_fitscore(self):
        # fitscore == (magnitude of the velocity vector + health)/2
        speed = sqrt(pow(self.x_speed,2) + pow(self.y_speed,2))
        return speed

    # this basically computes the direction in which the player character is located
    # and further computes a unit vector in that direction (dx, dy)
    # the npcs will then move in the direction of the unit vector

    def move_towards_player(self, x_player,y_player):
        (dx, dy) = ((self.x - x_player) / sqrt((self.x - x_player) ** 2 + (self.y - y_player) ** 2),
                    (self.y - y_player) / sqrt((self.x - x_player) ** 2 + (self.y - y_player) ** 2))
        self.x = self.x + dx*self.x_speed
        self.y = self.y + dy*self.y_speed

# this thing still is useless. it was meant to make the player able to shoot the balls
# I was too lazy to continue this, might do it in the future
class Bullet():
    def __init__(self,speed):
        self.speed = speed


# for the NPCs to grow in numbers
# part of the genetic algorithm
def reproduce(mate1,mate2):
    parent1 = mate1
    parent2 = mate2
    new_x_speed,new_y_speed,new_health = 0,0,0

    u = rand()
    if u < 0.45:
         new_x_speed = parent1.x_speed
    else:
         new_x_speed = parent2.x_speed

    u = rand()
    if u < 0.45:
        new_y_speed = parent1.x_speed
    else:
        new_y_speed = parent2.y_speed

    new_Radius = (parent1.radius + parent2.radius)/2

    new_child = Characters((parent1.x + parent2.x)/2,(parent1.y+parent2.y)/2,new_x_speed,new_y_speed,radius=new_Radius)
    return new_child
