from resources import *


DIRECTS = [[0,-1], [1,0], [0,1], [-1,0]]
TILE = 32

MOVE_SPEED = [5, 2, 2, 1, 2, 3, 3, 2]
BULLET_SPEED = [4, 5, 6, 5, 5, 5, 6, 7]
BULLET_DAMAGE = [1, 1, 2, 3, 2, 2, 3, 4]
SHOT_DELAY = [60, 50, 30, 40, 30, 25, 25, 30]

bullets = []
objects = []

class Tank:
    def __init__(self, color, px, py, direct, keysList):
        objects.append(self)
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
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
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center = self.rect.center)


    def update(self, keys):
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center = self.rect.center)

        self.moveSpeed = MOVE_SPEED[self.rank]
        self.bulletDamage = BULLET_DAMAGE[self.rank]
        self.bulletSpeed = BULLET_SPEED[self.rank]
        self.shotDelay = SHOT_DELAY[self.rank]

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
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0: self.shotTimer -= 1

        for obj in objects:
            if obj != self and obj.type == 'block':
                if self.rect.colliderect(obj) or self.rect.x < 0 or self.rect.x > WIDTH - 30 or self.rect.y < 0 or self.rect.y > HEIGHT - 30:
                    self.rect.topleft = oldX, oldY

    def draw(self):
        window.blit(self.image, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            sndDead.play()
            print(self.color, 'is dead')


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

        bullets.append(self)
        sndShot.play()

    def update(self, keys):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.type != 'bang' and obj.type != 'bonus':
                    if obj.rect.collidepoint(self.px, self.py):
                        obj.damage(self.damage)
                        bullets.remove(self)
                        Bang(self.px, self.py)
                        sndDestroy.play()
                        break

    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)

class Bang:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'bang'

        self.px, self.py = px, py
        self.frame = 0

    def update(self, keys):
        self.frame += 0.2
        if self.frame >= 5: objects.remove(self)

    def draw(self):
        img = imgBangs[int(self.frame)]
        rect = img.get_rect(center = (self.px, self.py))
        window.blit(img, rect)

class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1

    def update(self, keys):
        pass

    def draw(self):
        window.blit(imgBrick, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0: objects.remove(self)

class Bonus:
    def __init__(self, px, py, bonusNum):
        objects.append(self)
        self.type = 'bonus'

        self.px, self.py = px, py
        self.bonusNum = bonusNum
        self.timer = 600

        self.image = imgBonuses[self.bonusNum]
        self.rect = self.image.get_rect(center = (self.px, self.py))

    def update(self, keys):
        if self.timer > 0: self.timer -= 1
        else: objects.remove(self)

        for obj in objects:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                if self.bonusNum == 0:
                    if obj.rank < len(imgTanks) - 1:
                        obj.rank += 1
                        sndStar.play()
                        objects.remove(self)
                        break
                elif self.bonusNum == 1:
                    obj.hp += 1
                    sndLive.play()
                    objects.remove(self)
                    break


    def draw(self):
        if self.timer % 30 < 15:
            window.blit(self.image, self.rect)

