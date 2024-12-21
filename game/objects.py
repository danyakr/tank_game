import pygame
from game import resources
from pygame.locals import *


class objects:
    objects = []


class Tank:
    def __init__(self, color, px, py, direct, keysList):
        objects.objects.append(self)
        self.type = 'tank'
        self.color = color
        self.rect = pygame.Rect(px, py, resources.TILE, resources.TILE)
        self.direct = direct
        self.moveSpeed = 2
        self.shotTimer = 0
        self.shotDelay = 60
        self.bulletSpeed = 5
        self.bulletDamage = 1
        self.isMove = False
        self.hp = 5
        self.keyLEFT = keysList[0]
        self.keyRIGHT = keysList[1]
        self.keyUP = keysList[2]
        self.keyDOWN = keysList[3]
        self.keySHOT = keysList[4]
        self.rank = 0
        self.image = pygame.transform.rotate(resources.img_tanks[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, keys):
        self.image = pygame.transform.rotate(resources.img_tanks[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center=self.rect.center)

        self.moveSpeed = resources.MOVE_SPEED[self.rank]
        self.bulletDamage = resources.BULLET_DAMAGE[self.rank]
        self.bulletSpeed = resources.BULLET_SPEED[self.rank]
        self.shotDelay = resources.SHOT_DELAY[self.rank]

        oldX, oldY = self.rect.topleft
        if keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
            self.isMove = True
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
            self.isMove = True
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2
            self.isMove = True
        elif keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
            self.isMove = True
        else:
            self.isMove = False

        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = resources.DIRECTS[self.direct][0] * self.bulletSpeed
            dy = resources.DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0:
            self.shotTimer -= 1

        for obj in objects.objects:
            if obj != self and obj.type == 'block':
                if self.rect.colliderect(obj):
                    self.rect.topleft = oldX, oldY

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.objects.remove(self)
            resources.snd_dead.play()
            print(self.color, 'is dead')


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage
        objects.objects.append(self)
        resources.snd_shot.play()

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > resources.WIDTH or self.py < 0 or self.py > resources.HEIGHT:
            objects.objects.remove(self)
        else:
            for obj in objects.objects:
                if obj != self.parent and obj.type != 'bang' and obj.type != 'bonus':
                    if obj.rect.collidepoint(self.px, self.py):
                        obj.damage(self.damage)
                        objects.objects.remove(self)
                        Bang(self.px, self.py)
                        resources.snd_destroy.play()
                        break

    def draw(self, surface):
        pygame.draw.circle(surface, 'yellow', (self.px, self.py), 2)


class Bang:
    def __init__(self, px, py):
        objects.objects.append(self)
        self.type = 'bang'
        self.px, self.py = px, py
        self.frame = 0

    def update(self):
        self.frame += 0.2
        if self.frame >= 5:
            objects.objects.remove(self)

    def draw(self, surface):
        img = resources.img_bangs[int(self.frame)]
        rect = img.get_rect(center=(self.px, self.py))
        surface.blit(img, rect)


class Block:
    def __init__(self, px, py, size):
        objects.objects.append(self)
        self.type = 'block'
        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(resources.img_brick, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.objects.remove(self)


class Bonus:
    def __init__(self, px, py, bonusNum):
        objects.objects.append(self)
        self.type = 'bonus'
        self.px, self.py = px, py
        self.bonusNum = bonusNum
        self.timer = 600
        self.image = resources.img_bonuses[self.bonusNum]
        self.rect = self.image.get_rect(center=(self.px, self.py))

    def update(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            objects.objects.remove(self)

        for obj in objects.objects:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                if self.bonusNum == 0:
                    if obj.rank < len(resources.img_tanks) - 1:
                        obj.rank += 1
                        resources.snd_star.play()
                        objects.objects.remove(self)
                        break
                elif self.bonusNum == 1:
                    obj.hp += 1
                    resources.snd_live.play()
                    objects.objects.remove(self)
                    break

    def draw(self, surface):
        if self.timer % 30 < 15:
            surface.blit(self.image, self.rect)

