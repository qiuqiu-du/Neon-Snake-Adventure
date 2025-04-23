import pygame
from game import SnakeGame

def main():
    pygame.init()
    game = SnakeGame()
    game.gameLoop()

if __name__ == "__main__":
    main()