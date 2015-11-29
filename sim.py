from enum import Enum
from threading import Timer, Event, Thread
from queue import Queue

def call_repeatedly(interval, func):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func()
    Thread(target=loop).start()
    return stopped.set


class Direction(Enum):
    North = 0
    East = 1
    South = 2
    West = 3

class Square(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    def __hash__(self):
        return hash((self.x, self.y))

class World(object):
    def __init__(self):
        self.grid = [[None for x in range(self.width())] for x in range(self.height())]
        self.move_queue = Queue()
    def place(self, x, y , thing):
        self.grid[x][y] = thing
    def width(self):
        return 10
    def height(self):
        return 10



world = World()

def move(thing):
    pass

class Creature(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = Direction.East

    def run_turn(self):
        print("point: {0} , {1}".format(self.x,self.y))
        sq = self.square_ahead()
        if sq is not None:
            self.move(sq.x,sq.y)
            return
        print("aha")
        sq = self.square_left()
        if sq is not None:
            self.turn_left()
            sq = self.square_ahead()
            if sq is not None:
                self.move(sq.x,sq.y)
                return


    def turn_left(self):
        if self.direction is Direction.North:
            self.direction = Direction.West
            return
        elif self.direction is Direction.East:
            self.direction = Direction.North
            return

        elif self.direction is Direction.South:
            self.direction = Direction.East
            return

        elif self.direction is Direction.West:
            self.direction = Direction.South
            return

    def square_ahead(self):
        if self.direction is Direction.North:
            if self.y+1 > world.height() - 1:
                return None
            return Square(self.x,self.y+1)

        elif self.direction is Direction.East:
            if self.x+1 > world.width() - 1:
                print("end of the line")
                return None
            return Square(self.x+1,self.y)

        elif self.direction is Direction.South:
            if self.y-1 < 0:
                return None
            return Square(self.x,self.y-1)

        elif self.direction is Direction.West:
            if self.x-1 < 0:
                return None
            return Square(self.x-1,self.y)

    def square_left(self):
        if self.direction is Direction.North:
            if self.x-1 < 0:
                return None
            return Square(self.x-1,self.y)

        elif self.direction is Direction.East:
            if self.y+1 > world.width():
                return None
            return Square(self.x,self.y +1)

        elif self.direction is Direction.South:
            if self.x+1 > world.height():
                return None
            return Square(self.x+1,self.y)

        elif self.direction is Direction.West:
            if self.y-1 < 0:
                return None
            return Square(self.x,self.y-1)

    def move(self, x, y):
        world.move_queue.put((self, x, y))


def process_move_queue():
    if not world.move_queue.empty():
        thing,x,y = world.move_queue.get()
        thing.x = x
        thing.y = y
        world.grid[x][y] = thing

creature = Creature()

call_repeatedly(.5,creature.run_turn)
call_repeatedly(.05, process_move_queue)