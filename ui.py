import pygame
from constants import *
from utils import load_high_score  # 新增导入


class UIManager:
    def __init__(self):
        # 初始化字体
        try:
            self.font = pygame.font.SysFont("arial", 40)
            self.small_font = pygame.font.SysFont("arial", 20)
        except:
            self.font = pygame.font.SysFont(None, 40)
            self.small_font = pygame.font.SysFont(None, 20)

    def message(self, screen, msg, color, y_offset=0):
        mesg = self.font.render(msg, True, color)
        screen.blit(mesg, [WIDTH / 2 - mesg.get_width() / 2, HEIGHT / 2 - mesg.get_height() / 2 + y_offset])

    def draw_border(self, screen, score, color):
        pygame.draw.rect(screen, color, [0, 0, WIDTH, BORDER_WIDTH])
        pygame.draw.rect(screen, color, [0, 0, BORDER_WIDTH, HEIGHT])
        pygame.draw.rect(screen, color, [0, HEIGHT - BORDER_WIDTH, WIDTH, BORDER_WIDTH])
        pygame.draw.rect(screen, color, [WIDTH - BORDER_WIDTH, 0, BORDER_WIDTH, HEIGHT])

    def show_start_screen(self, screen):
        screen.fill(BLACK)
        self.message(screen, "SNAKE GAME", GREEN, -80)
        self.message(screen, "Press Any Key to Start", WHITE, 0)

        high_score = load_high_score()
        if high_score >= 0:
            score_text = self.small_font.render(f"High Score: {high_score}", True, WHITE)
            screen.blit(score_text, [WIDTH / 2 - score_text.get_width() / 2, HEIGHT / 2 + 70])

        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False