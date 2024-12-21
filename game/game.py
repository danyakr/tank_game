import pygame
import sys
from game import objects, resources, game_loop, menus

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Танки')
pygame.display.set_icon(pygame.image.load(resources.get_path('tank1.png')))

fontUI = pygame.font.Font(None, 30)
fontBig = pygame.font.Font(None, 70)

resources.load_resources()


main_menu = menus.MainMenu(window, fontUI, fontBig, resources)
game_over_menu = menus.GameOverMenu(window, fontUI, fontBig, resources)

running = True
current_menu = main_menu
while running:
    action = current_menu.run()
    if action == 'quit':
        running = False
        pygame.quit()
        sys.exit() # Добавлено для правильного завершения
    elif isinstance(action, menus.Menu):
        current_menu = action
    elif action == 'start_game':
      objects.objects = [] # Важно сбросить список объектов перед началом игры
      current_menu = game_loop.GameLoop(window, fontUI, fontBig, resources).run()
      if current_menu == 'quit':
        running = False
      elif current_menu == 'game_over':
        current_menu = game_over_menu
