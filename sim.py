from enum import Enum

class Direction(Enum):
    North = 0
    East = 1
    South = 2
    West = 3

class World(object):
    def __init__(self):
        self.grid = [[None for x in range(20)] for x in range(20)]
        self.move_queue = list()
    def place(self, x, y , thing):
        self.grid[x][y] = thing



world = World()

def move(thing):
    pass

class Creature(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = Direction.North

    def run_turn(self):
        things = self.get_visible_things()
    def get_visible_things(self):
        on_the_right = world[self.x+1][self.y]
        on_the_left = world[self.x-1][self.y]
        if self.direction == Direction.North:
            facing = world[self.x][self.y-1]
    def move(self, x, y):
        world.move_queue.append((self, x, y))
