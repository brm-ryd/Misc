#!/usr/bin/python

#AI race program
"""
implementation similar horse race simulation using random method
"""

import turtle
import random
import time

def newHorse():
    horses = turtle.Turtle()
    return horses

def generatesHorses(num_horses):
    horses = []
    for k in range(0, num_horses):
        horse = newHorse()
        horses.append(horse)
    return horses

def placeHorses(horses, loc, separation):
    color = ['black', 'red', 'yellow', 'blue', 'green', 'orange']
    for k in range(0, len(horses)):
        colors = random.choice(color)
        horses[k].fillcolor(colors)
        horses[k].hideturtle()
        horses[k].penup()
        horses[k].setposition(loc[0], loc[1] + k * separation)
        horses[k].setheading(180)
        horses[k].showturtle()
        horses[k].pendown()
        
def startHorses(horses, finish_line, forward_incr):
    have_winner = False
    k = 0
    while not have_winner:
        horse = horses[k]
        horse.forward(random.randint(1,3) * forward_incr)

        if horse.position()[0] < finish_line:
            have_winner = True
        else:
            k = (k+1) % len(horses)
    return k

def displayWinner(winning_horse):
    print('Horse', winning_horse, 'the Winner !')

    

num_horses = 10
turtle.setup(750, 800)
window = turtle.Screen()
window.title('Race Simulation')
start_loc=(240, -200)
finish_line = -240
track_separation = 60
forward_incr = 6


horses = generatesHorses(num_horses)
placeHorses(horses, start_loc, track_separation)
winner = startHorses(horses, finish_line, forward_incr)
displayWinner(winner+1)
turtle.exitonclick()
