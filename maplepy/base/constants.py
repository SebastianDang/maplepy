from typing import Final
from enum import Enum

import pygame

PYGAME_FLAGS: Final = pygame.HWSURFACE | pygame.HWACCEL | pygame.SRCALPHA | pygame.RESIZABLE
CAMERA_SPEED = 4

class GAME_STATE(Enum):
    LOADING = 0
    DEFAULT = 1
