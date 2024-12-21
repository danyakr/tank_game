from resources import *

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
        text_surface = fontUI.render(self.text, True, 'black')
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self):
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            return self.action()

class Menu:
    def __init__(self, buttons, window, title="Меню"):
        self.buttons = buttons
        self.window = window
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
            text_surface = fontBig.render(self.title, True, 'white')
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            window.blit(text_surface, text_rect)

            for button in self.buttons:
                button.draw(window)

            pygame.display.update()
            clock.tick(FPS)
