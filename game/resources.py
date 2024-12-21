import pygame
import os

TILE = 32
WIDTH = 800
HEIGHT = 600

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]

MOVE_SPEED = [5, 2, 2, 1, 2, 3, 3, 2]
BULLET_SPEED = [4, 5, 6, 5, 5, 5, 6, 7]
BULLET_DAMAGE = [1, 1, 2, 3, 2, 2, 3, 4]
SHOT_DELAY = [60, 50, 30, 40, 30, 25, 25, 30]

imgBrick = None
imgTanks = []
imgBangs = []
imgBonuses = []

sndShot = None
sndDestroy = None
sndDead = None
sndLive = None
sndStar = None
sndEngine = None
sndMove = None

def get_path(filename):
    return os.path.join('images', filename) if 'png' in filename else os.path.join('sounds', filename)


def load_resources():
    global imgBrick, imgTanks, imgBangs, imgBonuses, sndShot, sndDestroy, sndDead, sndLive, sndStar, sndEngine, sndMove
    imgBrick = pygame.image.load(get_path('block_brick.png'))
    imgTanks.extend([pygame.image.load(get_path(f'tank{i + 1}.png')) for i in range(8)])
    imgBangs.extend([pygame.image.load(get_path(f'bang{i + 1}.png')) for i in range(5)])
    imgBonuses.extend([pygame.image.load(get_path(f'bonus_{i}.png')) for i in ('star', 'tank')])

    sndShot = pygame.mixer.Sound(get_path('shot.wav'))
    sndDestroy = pygame.mixer.Sound(get_path('destroy.wav'))
    sndDead = pygame.mixer.Sound(get_path('dead.wav'))
    sndLive = pygame.mixer.Sound(get_path('live.wav'))
    sndStar = pygame.mixer.Sound(get_path('star.wav'))
    sndEngine = pygame.mixer.Sound(get_path('engine.wav'))
    sndEngine.set_volume(0.5)
    sndMove = pygame.mixer.Sound(get_path('move.wav'))
    sndMove.set_volume(0.5)
