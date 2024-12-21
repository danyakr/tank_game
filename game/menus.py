import pygame
from game1 import resources

pygame.font.init()

class Button:
    def __init__(self, x, y, w, h, text, color, hover_color, action, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = pygame.Color(color)
        self.hover_color = pygame.Color(hover_color)
        self.action = action
        self.font = font

    def draw(self, surface):
        color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(surface, color, self.rect)
        text_surface = self.font.render(self.text, True, 'black')
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self):
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            return self.action

class Menu:
    def __init__(self, buttons, title="Меню", fontUI=None, fontBig=None, resources=None):
        self.buttons = buttons
        self.title = title
        self.fontUI = fontUI
        self.fontBig = fontBig
        self.resources = resources

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        action = button.check_click()
                        if action:
                            return action

            self.resources.window.fill('black')
            if self.fontBig:
                text_surface = self.fontBig.render(self.title, True, 'white')
                text_rect = text_surface.get_rect(center=(self.resources.WIDTH // 2, self.resources.HEIGHT // 4))
                self.resources.window.blit(text_surface, text_rect)

            for button in self.buttons:
                button.draw(self.resources.window)

            pygame.display.update()
            clock.tick(self.resources.FPS)


class MainMenu(Menu):
    def __init__(self, window, fontUI, fontBig, resources):
        buttons = [
            Button(resources.WIDTH // 2 - 100, resources.HEIGHT // 2 - 50, 200, 40, "Начать игру", 'green', 'darkgreen',
                   'start_game', fontUI),
            Button(resources.WIDTH // 2 - 100, resources.HEIGHT // 2 + 10, 200, 40, "Настройки", 'blue', 'darkblue',
                   lambda: print('Настройки'), fontUI),
            Button(resources.WIDTH // 2 - 100, resources.HEIGHT // 2 + 70, 200, 40, "Инструкция", 'yellow',
                   'yellowgreen', lambda: print('Инструкции'), fontUI),
            Button(resources.WIDTH // 2 - 100, resources.HEIGHT // 2 + 130, 200, 40, "Выход", 'red', 'darkred',
                   'quit', fontUI),
        ]
        super().__init__(buttons, "Главное меню", fontUI, fontBig, resources)

class GameOverMenu(Menu):
    def __init__(self, window, fontUI, fontBig, resources):
        buttons = [
            Button(resources.WIDTH // 2 - 100, resources.HEIGHT // 2 - 50, 200, 40, "Попробовать снова", 'green',
                   'darkgreen', 'start_game', fontUI),
            Button(resources.WIDTH // 2 - 100, resources.HEIGHT // 2 + 10, 200, 40, "В главное меню", 'blue', 'darkblue',
                   lambda: main_menu, fontUI),
            Button(resources.WIDTH // 2 - 100, resources.HEIGHT // 2 + 70, 200, 40, "Выход", 'red', 'darkred',
                   'quit', fontUI),
        ]
        super().__init__(buttons, "Игра окончена", fontUI, fontBig, resources)
