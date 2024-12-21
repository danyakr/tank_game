from random import randint

from objects import *
from menu import *


pygame.display.set_caption('Танки')
pygame.display.set_icon(pygame.image.load('images/tank1.png'))


def start_game():
    global play, is_win, objects, bullets, tank1, tank2, timer, bonus_timer, old_is_move, is_move, keys

    bullets = []
    objects = []

    tank1 = Tank('blue', 50, 50, 1, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE), objects)
    tank2 = Tank('red', 700, 500, 3, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN), objects)

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

    bonusTimer = 180
    timer = 0
    isMove = False
    isWin = False

    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False

        keys = pygame.key.get_pressed()

        timer += 1
        if timer >= 260 and not isWin:
            if oldIsMove != isMove:
                if isMove:
                    sndMove.play()
                    sndEngine.stop()
                else:
                    sndMove.stop()
                    sndEngine.play(-1)

        oldIsMove = isMove
        isMove = False
        for obj in objects:
            if obj.type == 'tank': isMove = isMove or obj.is_move

        if bonusTimer > 0:
            bonusTimer -= 1
        else:
            Bonus(randint(50, WIDTH - 50), randint(50, HEIGHT - 50), randint(0, len(imgBonuses) - 1))
            bonusTimer = randint(120, 240)

        for bullet in bullets: bullet.update(keys)
        for obj in objects: obj.update(keys)

        window.fill('black')
        for bullet in bullets: bullet.draw()
        for obj in objects: obj.draw()

        i = 0
        for obj in objects:
            if obj.type == 'tank':
                pygame.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))

                text = fontUI.render(str(obj.rank), 1, 'black')
                rect = text.get_rect(center=(5 + i * 70 + 11, 5 + 11))
                window.blit(text, rect)

                text = fontUI.render(str(obj.hp), 1, obj.color)
                rect = text.get_rect(center=(5 + i * 70 + TILE, 5 + 11))
                window.blit(text, rect)
                i += 1

        # Проверка на победу и подготовка к переходу в меню Game Over
        t = 0
        for obj in objects:
            if obj.type == 'tank':
                t += 1
                tankWin = obj

        if t == 1 and not isWin:
            isWin = True
            timer = 0  # Сбрасываем таймер

            # Отображение победителя - вынесено из цикла
            window.fill('black')  # Очищаем экран
            text = fontBig.render('ПОБЕДИЛ', 1, 'white')
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
            window.blit(text, rect)

            pygame.draw.rect(window, tankWin.color, (WIDTH // 2 - 100, HEIGHT // 2, 200, 200))
            pygame.display.update()  # Обновляем экран
            pygame.time.delay(1500)  # Ждем 1.5 секунды

            play = False  # Завершаем игру
            action = game_over_menu.run()
            return game_over_menu

        pygame.display.update()
        clock.tick(FPS)

    return main_menu # Возвращаем меню после завершения игры

def show_settings():
    print("Настройки")

def show_instructions():
    print("Инструкции")


# Главное меню
main_menu_buttons = [
    Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 40, "Начать игру", 'green', 'darkgreen', start_game),
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 40, "Настройки", 'blue', 'darkblue', show_settings),
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 40, "Инструкция", 'yellow', 'yellowgreen', show_instructions),
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 130, 200, 40, "Выход", 'red', 'darkred', lambda: 'quit'),
]
main_menu = Menu(main_menu_buttons, window)


# Конечное меню
game_over_buttons = [
    Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 40, "Попробовать снова", 'green', 'darkgreen', start_game),
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 40, "В главное меню", 'blue', 'darkblue', lambda: main_menu),
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 40, "Выход", 'red', 'darkred', lambda: 'quit'),
]
game_over_menu = Menu(game_over_buttons, window, "Игра окончена")


# Цикл игры
play = False
action = main_menu.run()
while action != 'quit':
    if action == main_menu:
        action = main_menu.run()
    elif action == start_game:
        # игровой цикл
        while play:
            # обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    action = 'quit' # выход из меню и игры

            keys = pygame.key.get_pressed()

            timer += 1
            if timer >= 260 and not is_win:
                if old_is_move != is_move:
                    if is_move:
                        sndMove.play()
                        sndEngine.stop()
                    else:
                        sndMove.stop()
                        sndEngine.play(-1)

            old_is_move = is_move
            is_move = False
            for obj in objects:
                if obj.type == 'tank': is_move = is_move or obj.is_move

            if bonus_timer > 0:
                bonus_timer -= 1
            else:
                Bonus(randint(50, WIDTH - 50), randint(50, HEIGHT - 50), randint(0, len(imgBonuses) - 1))
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

                    text = fontUI.render(str(obj.rank), 1, 'black')
                    rect = text.get_rect(center=(5 + i * 70 + 11, 5 + 11))
                    window.blit(text, rect)

                    text = fontUI.render(str(obj.hp), 1, obj.color)
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
            # ... (ваш код отрисовки) ...

            if is_win and timer > 1000 :
                action = game_over_menu.run()
                play = False


            pygame.display.update()
            clock.tick(FPS)
    else:
        action = main_menu.run() # Если какое то другое действие

pygame.quit()
