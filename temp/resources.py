import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

fontUI = pygame.font.Font(None, 30)
fontBig = pygame.font.Font(None, 70)

imgBrick = pygame.image.load('images/block_brick.png')

imgTanks = [
    pygame.image.load('images/tank1.png'),
    pygame.image.load('images/tank2.png'),
    pygame.image.load('images/tank3.png'),
    pygame.image.load('images/tank4.png'),
    pygame.image.load('images/tank5.png'),
    pygame.image.load('images/tank6.png'),
    pygame.image.load('images/tank7.png'),
    pygame.image.load('images/tank8.png'),]

imgBangs = [
    pygame.image.load('images/bang1.png'),
    pygame.image.load('images/bang2.png'),
    pygame.image.load('images/bang3.png'),
    pygame.image.load('images/bang2.png'),
    pygame.image.load('images/bang1.png'),]

imgBonuses = [
    pygame.image.load('images/bonus_star.png'),
    pygame.image.load('images/bonus_tank.png'),]


sndShot = pygame.mixer.Sound('sounds/shot.wav')
sndDestroy = pygame.mixer.Sound('sounds/destroy.wav')
sndDead = pygame.mixer.Sound('sounds/dead.wav')
sndLive = pygame.mixer.Sound('sounds/live.wav')
sndStar = pygame.mixer.Sound('sounds/star.wav')
sndEngine = pygame.mixer.Sound('sounds/engine.wav')
sndEngine.set_volume(0.5)
sndMove = pygame.mixer.Sound('sounds/move.wav')
sndMove.set_volume(0.5)

pygame.mixer.music.load('sounds/level_start.mp3')
pygame.mixer.music.play()