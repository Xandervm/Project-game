import pygame
import random
from os import path

FONT_NAME = "arial"
WIDTH = 480
HEIGHT = 600
FPS = 60
img_dir = path.join(path.dirname(__file__), 'img')
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gimma")
clock = pygame.time.Clock()

# Colours

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
