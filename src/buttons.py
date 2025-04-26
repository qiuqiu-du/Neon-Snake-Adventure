import pygame
from .constants import *
import os

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


class SettingsButton:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager
        self.size = 30
        self.x = WIDTH - self.size - 10
        self.y = 10
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.color = (50, 50, 50)
        self.hover_color = (100, 100, 100)
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, 'assets', 'gear_icon.png')
        original_img = pygame.image.load(icon_path).convert_alpha()
        self.gear_image = pygame.transform.smoothscale(
            original_img,
            (self.size - 5, self.size - 5))

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 1)
        screen.blit(self.gear_image,
                   (self.x + (self.size - self.gear_image.get_width()) // 2 + 1,
                    self.y + (self.size - self.gear_image.get_height()) // 2 + 0.85))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


class LeaderboardButton:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager
        self.width = 100
        self.height = 30
        self.x = WIDTH - self.width - 30 - 2 * 10
        self.y = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (50, 50, 50)
        self.hover_color = (100, 100, 100)
        self.text = ui_manager.small_font.render("Leaderboard", True, WHITE)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 1)
        screen.blit(self.text,
                   (self.x + (self.width - self.text.get_width()) // 2,
                    self.y + (self.height - self.text.get_height()) // 2))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


class BackButton:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager
        self.width = 80
        self.height = 30
        self.x = 10
        self.y = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (50, 50, 50)
        self.hover_color = (100, 100, 100)
        self.text = ui_manager.small_font.render("Back", True, WHITE)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 1)
        screen.blit(self.text,
                   (self.x + (self.width - self.text.get_width()) // 2,
                    self.y + (self.height - self.text.get_height()) // 2))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)