#!/usr/bin/env python
#-*- coding:utf-8 -*-
# gridmap.py
# Author: 임희창, 박태헌


class GridNode(object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.is_obs = False
        self.in_result = False
        self.is_start = False
        self.is_goal = False
        self.previous = None
        self.visited = False
        self.mindistance = float('inf')
        self.h_value = float('inf')
        self.isopen = False

    def __lt__(self, other):
        return self.h_value < other.h_value

    def __cmp__(self, other):
        return cmp(self.h_value, other.h_value)

    def __eq__(self, other):
        return self.h_value == other.h_value

    def __gt__(self, other):
        return self.h_value > other.h_value


class GridMap():
    "Square grid map"
    def __init__(self, col, row, diagonal=False):
        "make row * col gridmap. from (0, 0) to (row - 1, col - 1)"
        self.can_diagonal_move = diagonal
        self.matrix = [[GridNode(i, j) for i in xrange(col)] \
                                        for j in xrange(row)]
        self.row = row
        self.col = col
        self.start_set = False
        self.goal_set = False

    def put_single_obs(self, x, y):
        "put an obstacle on (x, y)"
        self.matrix[y][x].is_obs = True

    def put_multiple_obs(self, arg_list):
        "put multiple obstacles"
        for x, y in arg_list:
            self.matrix[y][x].is_obs = True

    def remove_single_obs(self, x, y):
        self.matrix[y][x].is_obs = False

    def remove_multiple_obs(self, *args):
        for x, y in args:
            self.matrix[y][x].is_obs = False

    def set_start(self, x, y):
        self.matrix[y][x].is_start = True
        self.start = self.matrix[y][x]
        self.start_set = True

    def set_goal(self, x, y):
        self.matrix[y][x].is_goal = True
        self.goal = self.matrix[y][x]
        self.goal_set = True

    def randomize(self):
        "ramdomly make obstacles on gridmap and set start and goal"
        from random import random, choice
        notobs = []
        for row in self.matrix:
            for node in row:
                if random() < 0.2:
                    node.is_obs = True
                else:
                    notobs.append(node)
        s = choice(notobs)
        s.is_start = True
        notobs.remove(s)
        g = choice(notobs)
        g.is_goal = True
        self.start = s
        self.goal = g
        self.start_set = True
        self.goal_set = True

    def print_grid(self):
        "print gridmap pretty"
        for row in self.matrix:
            for node in row:
                if node.is_obs:
                    print '\033[1m\033[31m#\033[0m',
                elif node.is_start:
                    print '\033[1m\033[33mS\033[0m',
                elif node.is_goal:
                    print '\033[1m\033[33mG\033[0m',
                elif node.in_result:
                    print '\033[1m\033[32m*\033[0m',
                elif node.visited:
                    print '\033[1m\033[34m@\033[0m',
                else:
                    print '\033[37mo\033[0m',
            print

    def save_grid(self, name='result.txt'):
        "save gridmap in text file"
        f = open(name, 'a')
        for row in self.matrix:
            for node in row:
                if node.is_obs:
                    f.write('# ')
                elif node.is_start:
                    f.write('S ')
                elif node.is_goal:
                    f.write('G ')
                elif node.in_result:
                    f.write('* ')
                elif node.visited:
                    f.write('@ ')
                else:
                    f.write('o ')
        f.close()

    def print_mindistances(self):
        for row in self.matrix:
            for node in row:
                print node.mindistance,
            print


if __name__ == '__main__':
    grid = GridMap(30, 15)
    grid.print_grid()
    print
    grid.put_multiple_obs((2, 4), (1, 1), (11, 3), (12, 3), (13, 3))
    grid.print_grid()
    print
    grid = GridMap(40, 20)
    grid.randomize()
    grid.print_grid()
    print grid.row
    print grid.col
