from __future__ import division
import curses
import math
from random import randint, gauss, uniform
import time
###Flight simulator.
#Write a code in python that simulates the tilt correction of the plane (angle between plane wings and earth).
##The program should:
# - print out current orientation
# - applied tilt correction
# - run in infinite loop
# - until user breaks the loop
#Assume that plane orientation in every new simulation step is random angle with gaussian distribution (the planes is experiencing "turbulations").
#With every simulation step the orentation should be corrected, applied and printed out.
#If you can thing of any other features, you can add them.
#This code shoud be runnable with 'python kol1.py'.
#If you have spare time you can implement: Command Line Interface, generators, or even multiprocessing.
#Do your best, show off with good, clean, well structured code - this is more important than number of features.
#After you finish, be sure to UPLOAD this (add, commit, push) to the remote repository.
#Good Luck

TITLE = "Flight Simulator"
WIDTH = 80
HEIGHT = 16
MAX_X = WIDTH - 2
MAX_Y = HEIGHT - 2
TIMEOUT = 100

def print_start_text(window):
    print("\tWelcome to Flight Simulator, to stop program press: 'q' or Ctrl + C")
    time.sleep(2)

def update(*args):
    for arg in args:
        arg.update()

def render(*args):
    for arg in args:
        arg.render()


class Wind(object):
    mean = 45.0
    sdt_dev = 10.0
    value = 0
    direction = 0

    def __init__(self, window):
        self.window = window

    def update(self):
        self.value = uniform(0.3, 0.9)
        self.direction = int(gauss(self.mean, self.sdt_dev))

    def render_angle(self):
        x, y = 2, MAX_Y - 1
        self.window.addstr(y, x, 'Value:')
        self.window.addstr(y, x + 6, "{0:.1f}".format(self.value))
        for val in range(int(self.value*10)):
            self.window.addstr(y - val - 1, x + 4, '=')

    def render_direction(self):
        x, y = 15, MAX_Y -1
        self.window.addstr(y, x, 'Direction:')
        self.window.addstr(y, x + 10, str(self.direction))
        for val in range(int(self.direction / 10.0)):
            self.window.addstr(y - val - 1, x + 5, '=')

    def render(self):
        self.window.addstr(MAX_Y, 11, 'Wind')
        self.render_angle()
        self.render_direction()


class Route(object):
    current_pos = 1
    percentage = 0

    def __init__(self, window=None):
        self.start_point = (0, 0)
        self.end_point = (randint(10, 30), randint(10, 30))
        self.length = math.sqrt(self.end_point[0] * self.end_point[0] +
                                    self.end_point[1] * self.end_point[1])
        self.window = window
        self.title = 'Route'

    def update(self):
        self.current_pos += 1
        self.percentage = self.current_pos / self.length * 100
        if self.percentage >= 100.0:
            self.end_flight()

    def render(self):
        x, y = 2, 1
        MAX_LENGTH = MAX_X - 15
        self.window.addstr(y, x, self.title + ': ' +
                            "{0:.1f}".format(self.percentage) + '%')
        self.window.addstr(y, x + 14, 'Length: ' + "{0:.1f}".format(self.length))

        self.window.addstr(y + 1, x, 'Start point: (' + str(self.start_point[0]) +
                                        ", " + str(self.start_point[1]) + ')')

        self.window.addstr(y + 2, x, 'End point: (' + str(self.end_point[0]) +
                                        ", " + str(self.end_point[1]) + ')')

        self.window.addstr(y + 3, x, 'start:')
        self.window.addstr(y + 3, MAX_X -3, ':end')
        for val in range(int(MAX_LENGTH * self.percentage / 100)):
            self.window.addstr(y + 3, x + val + 7, '=')

    def end_flight(self):
        self.window.clear()
        self.window.addstr(5, 5, 'Flight has ended')
        time.sleep(1)
        exit()

class Plane(object):
    oryginal_angle = 0
    direction_angle = 0.0

    def __init__(self, route, wind, window=None):
        self.window = window
        self.calculate_direction(route)
        self.wind = wind

    def calculate_direction(self, route):
        self.direction_angle = math.degrees(math.asin(route.end_point[1] / route.length))
        self.oryginal_angle = self.direction_angle

    def update(self):
        self.direction_angle = wind.direction - self.direction_angle * self.wind.value

    def render_calculated(self):
        x, y = 35, MAX_Y -1
        self.window.addstr(y, x, 'Calculated angle:')
        self.window.addstr(y, x + 17, "{0:.1f}".format(self.oryginal_angle))
        for val in range(int(self.oryginal_angle / 10.0)):
            self.window.addstr(y - val - 1, x + 9, '=')

    def render_corrected(self):
        x, y = 60, MAX_Y -1
        self.window.addstr(y, x, 'Correction:')
        self.window.addstr(y, x + 11, "{0:.1f}".format(self.direction_angle))
        for val in range(int(self.direction_angle / 10.0)):
            self.window.addstr(y - val - 1, x + 6, '=')

    def render(self):
        self.window.addstr(MAX_Y, 55, 'Plane')
        self.render_calculated()
        self.render_corrected()



if __name__ == '__main__':
    curses.initscr()
    curses.beep()
    curses.beep()
    window = curses.newwin(HEIGHT, WIDTH, 0, 0)
    window.timeout(TIMEOUT)
    window.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    window.border(0)

    wind = Wind(window)
    route = Route(window)
    plane = Plane(route, wind, window)
    print_start_text(window)


    while True:
        window.clear()
        window.border(0)
        window.addstr(0, 5, TITLE)

        render(wind, route, plane)

        event = window.getch()
        if event == ord('q'):
            break


        update(wind, route, plane)
        time.sleep(1)


    curses.endwin()
