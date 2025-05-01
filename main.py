import pygame
import os
from src.game import SnakeGame
from src.utils import set_english_input

def main():
    pygame.init()
    base_path = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_path, 'assets', 'logo.ico')
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Neon Snake Adventure')

    set_english_input()
    game = SnakeGame()
    game.gameLoop()

if __name__ == "__main__":
    main()