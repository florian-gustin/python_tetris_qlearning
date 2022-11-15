from random import randint

import pygame


def rand_tetrimino():
    return randint(1, 2) # randint(3, 5)


ACTION_LEFT = "LEFT"
ACTION_RIGHT = "RIGHT"
ACTION_ROTATE = "ROTATE"
ACTION_NOTHING = "NOTHING"

AGENT_ACTIONS = {
    pygame.K_LEFT: ACTION_LEFT,
    pygame.K_RIGHT: ACTION_RIGHT,
    pygame.K_UP: ACTION_ROTATE,
    0: ACTION_NOTHING
}

PYGAME_ACTIONS = {
    ACTION_LEFT: pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT, mod=pygame.KMOD_NONE),
    ACTION_RIGHT: pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT, mod=pygame.KMOD_NONE),
    ACTION_ROTATE: pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP, mod=pygame.KMOD_NONE),
    ACTION_NOTHING: pygame.event.Event(pygame.KEYDOWN, key=0, mod=pygame.KMOD_NONE)
}

ACTIONS = [
    ACTION_LEFT,
    ACTION_RIGHT,
    ACTION_ROTATE,
    ACTION_NOTHING
]
