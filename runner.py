import json

import pygame
from random import randint


pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption('Танки')
pygame.display.set_icon(pygame.image.load('images/tank1.png'))

font_ui = pygame.font.Font(None, 30)
font_big = pygame.font.Font(None, 70)

img_brick = pygame.image.load('images/block_brick.png')

img_tanks = [
    pygame.image.load('images/tank1.png'),
    pygame.image.load('images/tank2.png'),
    pygame.image.load('images/tank3.png'),
    pygame.image.load('images/tank4.png'),
    pygame.image.load('images/tank5.png'),
    pygame.image.load('images/tank6.png'),
    pygame.image.load('images/tank7.png'),
    pygame.image.load('images/tank8.png'),
]

img_bangs = [
    pygame.image.load('images/bang1.png'),
    pygame.image.load('images/bang2.png'),
    pygame.image.load('images/bang3.png'),
    pygame.image.load('images/bang2.png'),
    pygame.image.load('images/bang1.png'),
]

img_bonuses = [
    pygame.image.load('images/bonus_star.png'),
    pygame.image.load('images/bonus_tank.png'),
]


snd_shot = pygame.mixer.Sound('sounds/shot.wav')
snd_destroy = pygame.mixer.Sound('sounds/destroy.wav')
snd_dead = pygame.mixer.Sound('sounds/dead.wav')
snd_live = pygame.mixer.Sound('sounds/live.wav')
snd_star = pygame.mixer.Sound('sounds/star.wav')
snd_engine = pygame.mixer.Sound('sounds/engine.wav')
snd_engine.set_volume(0.5)
snd_move = pygame.mixer.Sound('sounds/move.wav')
snd_move.set_volume(0.5)

pygame.mixer.music.load('sounds/level_start.mp3')
pygame.mixer.music.play()

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]
TILE = 32

MOVE_SPEED = [1, 2, 2, 1, 2, 3, 3, 2]
BULLET_SPEED = [4, 5, 6, 5, 5, 5, 6, 7]
BULLET_DAMAGE = [1, 1, 2, 3, 2, 2, 3, 4]
SHOT_DELAY = [60, 50, 30, 40, 30, 25, 25, 30]


class Tank:
    def __init__(self, color, px, py, direct, keys_list):
        objects.append(self)
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.move_speed = 2

        self.shot_timer = 0
        self.shot_delay = 60
        self.bullet_speed = 5
        self.bullet_damage = 1
        self.is_move = False

        self.hp = 5

        self.keyLEFT = keys_list[0]
        self.keyRIGHT = keys_list[1]
        self.keyUP = keys_list[2]
        self.keyDOWN = keys_list[3]
        self.keySHOT = keys_list[4]

        self.rank = 0
        self.image = pygame.transform.rotate(img_tanks[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.image = pygame.transform.rotate(img_tanks[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center=self.rect.center)

        self.move_speed = MOVE_SPEED[self.rank]
        self.bullet_damage = BULLET_DAMAGE[self.rank]
        self.bullet_speed = BULLET_SPEED[self.rank]
        self.shot_delay = SHOT_DELAY[self.rank]

        oldX, oldY = self.rect.topleft
        if keys[self.keyUP]:
            self.rect.y -= self.move_speed
            self.direct = 0
            self.is_move = True
        elif keys[self.keyRIGHT]:
            self.rect.x += self.move_speed
            self.direct = 1
            self.is_move = True
        elif keys[self.keyDOWN]:
            self.rect.y += self.move_speed
            self.direct = 2
            self.is_move = True
        elif keys[self.keyLEFT]:
            self.rect.x -= self.move_speed
            self.direct = 3
            self.is_move = True
        else:
            self.is_move = False

        if keys[self.keySHOT] and self.shot_timer == 0:
            dx = DIRECTS[self.direct][0] * self.bullet_speed
            dy = DIRECTS[self.direct][1] * self.bullet_speed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bullet_damage)
            self.shot_timer = self.shot_delay

        if self.shot_timer > 0:
            self.shot_timer -= 1

        for obj in objects:
            if obj != self and obj.type == 'block':
                if (self.rect.colliderect(obj) or
                        self.rect.x < 0 or self.rect.x > WIDTH - 30 or self.rect.y < 0 or self.rect.y > HEIGHT - 30):
                    self.rect.topleft = oldX, oldY

    def draw(self):
        window.blit(self.image, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            snd_dead.play()
            print(self.color, 'is dead')


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

        bullets.append(self)
        snd_shot.play()

    def update(self):
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
                        snd_destroy.play()
                        break

    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)


class Bang:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'bang'

        self.px, self.py = px, py
        self.frame = 0

    def update(self):
        self.frame += 0.2
        if self.frame >= 5:
            objects.remove(self)

    def draw(self):
        img = img_bangs[int(self.frame)]
        rect = img.get_rect(center=(self.px, self.py))
        window.blit(img, rect)


class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1

    def update(self):
        pass

    def draw(self):
        window.blit(img_brick, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)


class Bonus:
    def __init__(self, px, py, bonus_num):
        objects.append(self)
        self.type = 'bonus'

        self.px, self.py = px, py
        self.bonus_num = bonus_num
        self.timer = 600

        self.image = img_bonuses[self.bonus_num]
        self.rect = self.image.get_rect(center=(self.px, self.py))

    def update(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            objects.remove(self)

        for obj in objects:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                if self.bonus_num == 0:
                    if obj.rank < len(img_tanks) - 1:
                        obj.rank += 1
                        snd_star.play()
                        objects.remove(self)
                        break
                elif self.bonus_num == 1:
                    obj.hp += 1
                    snd_live.play()
                    objects.remove(self)
                    break

    def draw(self):
        if self.timer % 30 < 15:
            window.blit(self.image, self.rect)


class Button:
    def __init__(self, x, y, w, h, text, color, hover_color, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, surface):
        color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(surface, color, self.rect)
        text_surface = font_ui.render(self.text, True, 'black')
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self):
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            return self.action()


class Menu:
    def __init__(self, buttons, title='Меню'):
        self.buttons = buttons
        self.title = title

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    action = None
                    for button in self.buttons:
                        action = button.check_click()
                        if action == 'quit':
                            return 'quit'
                        elif action:
                            return action

            window.fill('black')
            text_surface = font_big.render(self.title, True, 'white')
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            window.blit(text_surface, text_rect)

            for button in self.buttons:
                button.draw(window)

            pygame.display.update()
            clock.tick(FPS)


def start_game():
    global play, is_win, objects, bullets, tank1, tank2, timer, bonus_timer, old_is_move, is_move, keys
    bullets = []
    objects = []
    tank1 = Tank('blue', 50, 50, 1, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
    tank2 = Tank('red', 700, 500, 3, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN))

    for _ in range(100):
        while True:
            x = randint(0, WIDTH // TILE - 1) * TILE
            y = randint(1, HEIGHT // TILE - 1) * TILE
            rect = pygame.Rect(x, y, TILE, TILE)
            fined = False
            for obj in objects:
                if rect.colliderect(obj): fined = True
            if not fined: break

        Block(x, y, TILE)

    bonus_timer = 180
    timer = 0
    is_move = False
    is_win = False

    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False

        keys = pygame.key.get_pressed()

        timer += 1
        if timer >= 260 and not is_win:
            if old_is_move != is_move:
                if is_move:
                    snd_move.play()
                    snd_engine.stop()
                else:
                    snd_move.stop()
                    snd_engine.play(-1)

        old_is_move = is_move
        is_move = False
        for obj in objects:
            if obj.type == 'tank': is_move = is_move or obj.is_move

        if bonus_timer > 0:
            bonus_timer -= 1
        else:
            Bonus(randint(50, WIDTH - 50), randint(50, HEIGHT - 50), randint(0, len(img_bonuses) - 1))
            bonus_timer = randint(120, 240)

        for bullet in bullets: bullet.update()
        for obj in objects: obj.update()

        window.fill('black')
        for bullet in bullets: bullet.draw()
        for obj in objects: obj.draw()

        i = 0
        for obj in objects:
            if obj.type == 'tank':
                pygame.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))

                text = font_ui.render(str(obj.rank), 1, 'black')
                rect = text.get_rect(center=(5 + i * 70 + 11, 5 + 11))
                window.blit(text, rect)

                text = font_ui.render(str(obj.hp), 1, obj.color)
                rect = text.get_rect(center=(5 + i * 70 + TILE, 5 + 11))
                window.blit(text, rect)
                i += 1

        # Проверка на победу и подготовка к переходу в меню Game Over
        t = 0
        for obj in objects:
            if obj.type == 'tank':
                t += 1
                tankWin = obj

        if t == 1 and not is_win:
            is_win = True
            timer = 0

            window.fill('black')
            text = font_big.render('ПОБЕДИЛ', 1, 'white')
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
            window.blit(text, rect)

            pygame.draw.rect(window, tankWin.color, (WIDTH // 2 - 100, HEIGHT // 2, 200, 200))
            pygame.display.update()
            pygame.time.delay(1500)

            play = False
            action = game_over_menu.run()
            return game_over_menu

        pygame.display.update()
        clock.tick(FPS)

    return main_menu


# Функция для загрузки громкости из файла
def load_volume():
    try:
        with open('settings.json', 'r') as f:
            data = json.load(f)
            return data.get('volume', 0.5)  # Если в файле нет громкости, возвращаем 0.5
    except FileNotFoundError:
        return 0.5  # Если файла нет, устанавливаем громкость на 50%


# Функция для сохранения громкости в файл
def save_volume(volume):
    data = {'volume': volume}
    with open('settings.json', 'w') as f:
        json.dump(data, f)


def show_settings():
    global snd_engine, snd_shot, snd_destroy, snd_dead, snd_live, snd_star, snd_move
    settings_running = True
    volume = load_volume()  # Загружаем громкость из файла

    # Применяем громкость
    update_volume(volume)

    while settings_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Вернуться в меню
                    return  # Возвращаемся обратно в главное меню
                elif event.key == pygame.K_UP:  # Увеличить громкость
                    volume = min(volume + 0.05, 1.0)  # Ограничиваем громкость 100%
                    update_volume(volume)
                    save_volume(volume)  # Сохраняем новое значение громкости
                elif event.key == pygame.K_DOWN:  # Уменьшить громкость
                    volume = max(volume - 0.05, 0.0)
                    update_volume(volume)
                    save_volume(volume)  # Сохраняем новое значение громкости

        window.fill('black')
        text = font_big.render('Настройки', True, 'white')
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        window.blit(text, rect)

        # Показываем громкость
        volume_text = font_ui.render(f'Громкость: {int(volume * 100)}%', True, 'white')
        rect = volume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(volume_text, rect)

        # Кнопка "Вернуться в меню"
        back_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 40, "В главное меню", 'blue', 'darkblue',
                             lambda: None)
        back_button.draw(window)

        pygame.display.update()
        clock.tick(FPS)


# Функция для обновления громкости всех звуков
def update_volume(volume):
    snd_engine.set_volume(volume)
    snd_shot.set_volume(volume)
    snd_destroy.set_volume(volume)
    snd_dead.set_volume(volume)
    snd_live.set_volume(volume)
    snd_star.set_volume(volume)
    snd_move.set_volume(volume)


# Функция для отображения инструкций и управления с прокруткой с помощью колесика мыши
def show_instructions():
    instructions_text = [
        "Танки: Руководство по игре",
        "",
        "Цель:",
        "Уничтожьте всех противников и останьтесь последним танком ",
        "на поле боя!",
        "",
        "Управление:",
        "",
        "Игрок 1: WASD и Пробел",
        "• W/S: Вперед/Назад",
        "• A/D: Влево/Вправо",
        "• Пробел: Выстрел",
        "",
        "Игрок 2: Стрелки и Enter",
        "• ↑/↓: Вперед/Назад",
        "• ←/→: Влево/Вправо",
        "• Enter: Выстрел",
        "",
        "Характеристики Танка:",
        "• Ранг: Определяет скорость, урон и скорострельность. ",
        "Начинаете с 1 ранга.",
        "• Здоровье (HP): Количество очков здоровья. ",
        "Увеличивается с ростом ранга.",
        "",
        "Бонусы:",
        "• Звезда: Повышает ранг танка, улучшая характеристики.",
        "• Дополнительное здоровье: Восстанавливает 1 HP.",
        "",
        "Тактика:",
        "Используйте блоки как укрытие, захватывайте бонусы ",
        "и выбирайте тактику в зависимости от ранга вашего танка!",
        "",
        "Удачи!",
        "Нажмите Escape для возврата в меню."
    ]

    # Переменные для управления прокруткой
    scroll_offset = 0
    scroll_speed = 45  # Скорость прокрутки (по пикселям)
    max_scroll = len(instructions_text) * 50 - window.get_height()  # Ограничение по прокрутке

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Прокрутка вверх или вниз
                if event.key == pygame.K_DOWN:
                    scroll_offset = min(scroll_offset + scroll_speed, max_scroll)
                elif event.key == pygame.K_UP:
                    scroll_offset = max(scroll_offset - scroll_speed, 0)
                # Выход в главное меню при нажатии клавиши Escape
                elif event.key == pygame.K_ESCAPE:
                    return main_menu
                # Возвращаемся в главное меню при нажатии Space или Enter
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return main_menu
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Прокрутка колесиком мыши
                if event.button == 4:  # Колесико вверх
                    scroll_offset = max(scroll_offset - scroll_speed, 0)
                elif event.button == 5:  # Колесико вниз
                    scroll_offset = min(scroll_offset + scroll_speed, max_scroll)

        window.fill('black')

        # Отображаем текст инструкций с учетом прокрутки
        y_offset = 50 - scroll_offset
        for line in instructions_text:
            text_surface = font_ui.render(line, True, 'white')
            window.blit(text_surface, (50, y_offset))
            y_offset += 40  # расстояние между строками

        # Отображение заднего фона полосы прокрутки
        scroll_bar_bg_height = window.get_height() - 20  # Задний фон полосы
        scroll_bar_bg_position = (window.get_width() - 20, 10)
        pygame.draw.rect(window, (50, 50, 50), (scroll_bar_bg_position[0], scroll_bar_bg_position[1], 10, scroll_bar_bg_height))

        # Отображение полосы прокрутки
        scroll_bar_height = window.get_height() * (window.get_height() / (len(instructions_text) * 50))
        scroll_bar_position = (window.get_width() - 20, 10 + (scroll_offset / max_scroll) * (window.get_height() - scroll_bar_height - 20))
        pygame.draw.rect(window, (255, 255, 255), (scroll_bar_position[0], scroll_bar_position[1], 10, scroll_bar_height))

        pygame.display.update()
        clock.tick(FPS)


main_menu_buttons = [
    Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 40, "Начать игру", 'green', 'darkgreen', start_game),
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 40, "Настройки", 'blue', 'darkblue', show_settings),
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 40, "Инструкция", 'yellow', 'yellowgreen', show_instructions),
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 130, 200, 40, "Выход", 'red', 'darkred', lambda: 'quit'),
]
main_menu = Menu(main_menu_buttons)


game_over_buttons = [
    Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 40, "Попробовать снова", 'green', 'darkgreen', start_game),
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 40, "В главное меню", 'blue', 'darkblue', lambda: main_menu),
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 40, "Выход", 'red', 'darkred', lambda: 'quit'),
]
game_over_menu = Menu(game_over_buttons, "Игра окончена")

# Цикл игры
play = False
action = main_menu.run()
while action != 'quit':
    if action == main_menu:
        action = main_menu.run()
    elif action == start_game:
        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    action = 'quit'

            keys = pygame.key.get_pressed()

            timer += 1
            if timer >= 260 and not is_win:
                if old_is_move != is_move:
                    if is_move:
                        snd_move.play()
                        snd_engine.stop()
                    else:
                        snd_move.stop()
                        snd_engine.play(-1)

            old_is_move = is_move
            is_move = False
            for obj in objects:
                if obj.type == 'tank':
                    is_move = is_move or obj.is_move

            if bonus_timer > 0:
                bonus_timer -= 1
            else:
                Bonus(randint(50, WIDTH - 50), randint(50, HEIGHT - 50), randint(0, len(img_bonuses) - 1))
                bonus_timer = randint(120, 240)

            for bullet in bullets:
                bullet.update()

            for obj in objects:
                obj.update()

            window.fill('black')
            for bullet in bullets:
                bullet.draw()

            for obj in objects:
                obj.draw()

            i = 0
            for obj in objects:
                if obj.type == 'tank':
                    pygame.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))

                    text = font_ui.render(str(obj.rank), 1, 'black')
                    rect = text.get_rect(center=(5 + i * 70 + 11, 5 + 11))
                    window.blit(text, rect)

                    text = font_ui.render(str(obj.hp), 1, obj.color)
                    rect = text.get_rect(center=(5 + i * 70 + TILE, 5 + 11))
                    window.blit(text, rect)
                    i += 1

            # Проверка на победу и переход в меню Game Over
            t = 0
            for obj in objects:
                if obj.type == 'tank':
                    t += 1
            if t == 1 and not is_win:
                is_win = True
                timer = 1000

            window.fill('black')

            if is_win and timer > 1000:
                action = game_over_menu.run()
                play = False

            pygame.display.update()
            clock.tick(FPS)
    else:
        action = main_menu.run()

pygame.quit()
