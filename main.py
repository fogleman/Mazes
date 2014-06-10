from itertools import product
import cairo
import random

OFFSETS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]

class Maze(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.removed = set()
    def check_neighbor(self, (x, y)):
        return x >= 0 and y >= 0 and x < self.width and y < self.height
    def get_neighbors(self, (x, y)):
        neighbors = [(x + dx, y + dy) for dx, dy in OFFSETS]
        neighbors = filter(self.check_neighbor, neighbors)
        return neighbors
    def remove_wall(self, a, b):
        self.removed.add((a, b))
        self.removed.add((b, a))
    def generate(self):
        unvisited = set(product(range(self.width), range(self.height)))
        current = random.choice(list(unvisited))
        unvisited.remove(current)
        stack = []
        while unvisited:
            neighbors = set(self.get_neighbors(current)) & unvisited
            if neighbors:
                neighbor = random.choice(list(neighbors))
                self.remove_wall(current, neighbor)
                stack.append(current)
                current = neighbor
                unvisited.remove(current)
            elif stack:
                current = stack.pop()
            else:
                current = random.choice(list(unvisited))
                unvisited.remove(current)
    def render(self, path):
        size = 32
        pad = size
        width = self.width * size + pad * 2
        height = self.height * size + pad * 2
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
        dc = cairo.Context(surface)
        dc.set_source_rgb(1, 1, 1)
        dc.paint()
        dc.set_source_rgb(0, 0, 0)
        dc.set_line_width(6)
        dc.set_line_cap(cairo.LINE_CAP_ROUND)
        for i, j in product(range(self.width), range(self.height)):
            x1, y1 = i * size + pad, j * size + pad
            x2, y2 = x1 + size, y1 + size
            if ((i, j), (i, j - 1)) not in self.removed:
                dc.move_to(x1, y1)
                dc.line_to(x2, y1)
            if ((i, j), (i, j + 1)) not in self.removed:
                dc.move_to(x1, y2)
                dc.line_to(x2, y2)
            if ((i, j), (i - 1, j)) not in self.removed:
                dc.move_to(x1, y1)
                dc.line_to(x1, y2)
            if ((i, j), (i + 1, j)) not in self.removed:
                dc.move_to(x2, y1)
                dc.line_to(x2, y2)
        dc.stroke()
        surface.write_to_png(path)

def main():
    maze = Maze(24, 24)
    maze.generate()
    maze.render('output.png')

if __name__ == '__main__':
    main()
