from numpy import array
import numpy as np
from food import Food


class Snake:
    class Segment:

        def __init__(self, position: array):
            self.pos = position

    def __init__(self, grid_dimension: array, start_pos: array, direction: int = 0):
        self.grid_dim = grid_dimension
        self.segments = []
        self.direction = direction
        self.next_dir = direction
        self.is_growing = 2
        self.dead = False

        self.head_index = 0

        self.foods = []

        self.add_segment(start_pos)
        self.add_food()

    def add_segment(self, position):
        if True in np.greater(position, self.grid_dim):
            raise ValueError("Snake tried to create a segment outside of grid dimension")
        index = (self.head_index - 1 + len(self.segments)) % len(self.segments)
        self.segments.insert(index, self.Segment(position))
        print(self.get_segment_positions())
        return index

    def get_segment_positions(self):
        out = []
        for segment in self.segments:
            out.append(segment.pos)
        return out

    def get_food_positions(self):
        out = []
        for food in self.foods:
            out.append(food.pos)
        return out

    def move(self):
        new_head_pos = None
        length = len(self.segments)
        self.direction = self.next_dir
        match self.direction:
            case 0:
                new_head_pos = self.segments[self.head_index].pos + [0, -1]
            case 1:
                new_head_pos = self.segments[self.head_index].pos + [1, 0]
            case 2:
                new_head_pos = self.segments[self.head_index].pos + [0, 1]
            case 3:
                new_head_pos = self.segments[self.head_index].pos + [-1, 0]

        if self.is_out_of_bounds(new_head_pos) or self.is_on_pos(new_head_pos):
            self.dead = True

        if not self.dead:

            for food in self.foods:
                if self.is_on_pos(food.pos):
                    self.foods.remove(food)
                    self.grow()
                    self.add_food()

            if self.is_growing:
                self.add_segment(new_head_pos)
                self.is_growing -= 1
            else:
                self.head_index = (self.head_index - 1) % len(self.segments)
                self.segments[self.head_index].pos = new_head_pos
                self.head_index = (self.head_index + len(self.segments) - 1) % len(self.segments)

    def is_out_of_bounds(self, position):
        if True in np.greater_equal(position, self.grid_dim):
            return True
        elif True in np.less(position, array([0, 0])):
            return True
        return False

    def is_on_pos(self, pos):
        for segment in self.segments:
            if segment.pos[0] == pos[0] and segment.pos[1] == pos[1]:
                return True
        return False

    def grow(self):
        self.is_growing += 1

    def change_dir(self, direction: int):
        if not (direction + 2) % 4 == self.direction:
            self.next_dir = direction

    def add_food(self):
        pos = np.random.randint([0, 0], self.grid_dim)
        self.foods.append(Food(pos))

