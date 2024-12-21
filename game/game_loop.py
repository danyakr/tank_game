from random import randint

import pygame
from game1 import objects, resources
from pygame.locals import *

class GameLoop:
    def __init__(self, window, fontUI, fontBig, resources):
        self.window = window
        self.fontUI = fontUI
        self.fontBig = fontBig
        self.resources = resources
        self.bullets = []
        self.objects = objects.objects

        self.tank1 = objects.Tank('blue', 50, 50, 1, (K_a, K_d, K_w, K_s, K_SPACE))
        self.tank2 = objects.Tank('red', 700, 500, 3, (K_LEFT, K_RIGHT, K_UP, K_DOWN, K_RETURN))
        self.create_blocks()

        self.bonusTimer = 180
        self.timer = 0
        self.oldIsMove = False
        self.isMove = False
        self.isWin = False


    def create_blocks(self):
        for _ in range(100):
            while True:
                x = randint(0, self.resources.WIDTH // self.resources.TILE - 1) * self.resources.TILE
                y = randint(1, self.resources.HEIGHT // self.resources.TILE - 1) * self.resources.TILE
                rect = pygame.Rect(x, y, self.resources.TILE, self.resources.TILE)
                fined = False
                for obj in self.objects:
                    if rect.colliderect(obj.rect):
                        fined = True
                        break
                if not fined:
                    break
            objects.Block(x, y, self.resources.TILE)

    def run(self):
        pygame.mixer.music.load(self.resources.get_path('level_start.mp3'))
        pygame.mixer.music.play()
        play = True
        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    return 'quit'


            keys = pygame.key.get_pressed()
            self.timer += 1
            if self.timer >= 260 and not self.isWin:
                if self.oldIsMove != self.isMove:
                    if self.isMove:
                        self.resources.snd_move.play()
                        self.resources.snd_engine.stop()
                    else:
                        self.resources.snd_move.stop()
                        self.resources.snd_engine.play(-1)

            self.oldIsMove = self.isMove
            self.isMove = False
            for obj in self.objects:
                if obj.type == 'tank':
                    self.isMove = self.isMove or obj.is_move
                    obj.update(keys)

            if self.bonusTimer > 0:
                self.bonusTimer -= 1
            else:
                objects.Bonus(randint(50, self.resources.WIDTH - 50), randint(50, self.resources.HEIGHT - 50),
                              randint(0, len(self.resources.img_bonuses) - 1))
                self.bonusTimer = randint(120, 240)

            for bullet in self.bullets:
                bullet.update()

            for obj in self.objects:
                obj.update()

            self.window.fill('black')
            for bullet in self.bullets:
                bullet.draw(self.window)
            for obj in self.objects:
                obj.draw(self.window)

            i = 0
            for obj in self.objects:
                if obj.type == 'tank':
                    pygame.draw.rect(self.window, obj.color, (5 + i * 70, 5, 22, 22))

                    text = self.fontUI.render(str(obj.rank), 1, 'black')
                    rect = text.get_rect(center=(5 + i * 70 + 11, 5 + 11))
                    self.window.blit(text, rect)

                    text = self.fontUI.render(str(obj.hp), 1, obj.color)
                    rect = text.get_rect(center=(5 + i * 70 + self.resources.TILE, 5 + 11))
                    self.window.blit(text, rect)
                    i += 1

            # проверка на победу
            t = 0
            for obj in self.objects:
                if obj.type == 'tank':
                    t += 1
                    tankWin = obj

            if t == 1 and not self.isWin:
                self.isWin = True
                self.timer = 0

                self.window.fill('black')
                text = self.fontBig.render('ПОБЕДИЛ', 1, 'white')
                rect = text.get_rect(center=(self.resources.WIDTH // 2, self.resources.HEIGHT // 2 - 100))
                self.window.blit(text, rect)
                pygame.draw.rect(self.window, tankWin.color,
                                 (self.resources.WIDTH // 2 - 100, self.resources.HEIGHT // 2, 200, 200))
                pygame.display.update()
                pygame.time.delay(1500)
                return 'game_over'

            pygame.display.update()
            clock.tick(self.resources.FPS)
        return 'quit'
