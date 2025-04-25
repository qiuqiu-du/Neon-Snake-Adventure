import pygame
from src.game import SnakeGame
from src.utils import set_english_input

def main():
    pygame.init()
    set_english_input()
    game = SnakeGame()
    game.gameLoop()

if __name__ == "__main__":
    main()