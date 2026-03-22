import pygame

# 색상 정의
BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
CYAN   = (0,   255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0,   128)
GREEN  = (0,   255, 0)
RED    = (255, 0,   0)
BLUE   = (0,   0,   255)
ORANGE = (255, 165, 0)

# 테트리미노 모양 (각 회전 상태 포함)
SHAPES = {
    'I': {
        'color': CYAN,
        'rotations': [
            [(0,0),(1,0),(2,0),(3,0)],
            [(0,0),(0,1),(0,2),(0,3)],
        ]
    },
    'O': {
        'color': YELLOW,
        'rotations': [
            [(0,0),(1,0),(0,1),(1,1)],
        ]
    },
    'T': {
        'color': PURPLE,
        'rotations': [
            [(0,0),(1,0),(2,0),(1,1)],
            [(0,0),(0,1),(0,2),(1,1)],
            [(0,1),(1,1),(2,1),(1,0)],
            [(1,0),(1,1),(1,2),(0,1)],
        ]
    },
    'S': {
        'color': GREEN,
        'rotations': [
            [(1,0),(2,0),(0,1),(1,1)],
            [(0,0),(0,1),(1,1),(1,2)],
        ]
    },
    'Z': {
        'color': RED,
        'rotations': [
            [(0,0),(1,0),(1,1),(2,1)],
            [(1,0),(0,1),(1,1),(0,2)],
        ]
    },
    'J': {
        'color': BLUE,
        'rotations': [
            [(0,0),(0,1),(1,1),(2,1)],
            [(0,0),(1,0),(0,1),(0,2)],
            [(0,0),(1,0),(2,0),(2,1)],
            [(1,0),(1,1),(0,2),(1,2)],
        ]
    },
    'L': {
        'color': ORANGE,
        'rotations': [
            [(2,0),(0,1),(1,1),(2,1)],
            [(0,0),(0,1),(0,2),(1,2)],
            [(0,0),(1,0),(2,0),(0,1)],
            [(0,0),(1,0),(1,1),(1,2)],
        ]
    },
}

SHAPE_NAMES = list(SHAPES.keys())


class Piece:
    def __init__(self, name, x=3, y=0):
        self.name = name
        self.color = SHAPES[name]['color']
        self.rotations = SHAPES[name]['rotations']
        self.rotation_index = 0
        self.x = x
        self.y = y

    @property
    def blocks(self):
        return self.rotations[self.rotation_index]

    def rotate(self):
        self.rotation_index = (self.rotation_index + 1) % len(self.rotations)

    def rotate_back(self):
        self.rotation_index = (self.rotation_index - 1) % len(self.rotations)

    def get_absolute_blocks(self):
        return [(self.x + bx, self.y + by) for bx, by in self.blocks]
