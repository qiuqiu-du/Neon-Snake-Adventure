import pygame
from constants import *

class PauseButton:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager
        self.width = 80
        self.height = 30
        self.x = WIDTH - self.width - 10
        self.y = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (100, 100, 100)
        self.hover_color = (150, 150, 150)
        self.pause_text = ui_manager.small_font.render("Pause", True, WHITE)
        self.resume_text = ui_manager.small_font.render("Resume", True, WHITE)

    def draw(self, screen, paused):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 1)

        text = self.resume_text if paused else self.pause_text
        screen.blit(text, (self.x + (self.width - text.get_width()) // 2,
                         self.y + (self.height - text.get_height()) // 2))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)