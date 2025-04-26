import pygame
import json
from .constants import *
from .utils import load_high_score
from .buttons import SettingsButton, LeaderboardButton, BackButton


class UIManager:
    def __init__(self):
        # Initialize fonts
        try:
            self.font = pygame.font.SysFont("arial", 40)
            self.small_font = pygame.font.SysFont("arial", 20)
            self.medium_font = pygame.font.SysFont("arial", 30)
            self.large_font = pygame.font.SysFont("arial", 50)
        except:
            self.font = pygame.font.SysFont(None, 40)
            self.small_font = pygame.font.SysFont(None, 20)
            self.medium_font = pygame.font.SysFont(None, 30)
            self.large_font = pygame.font.SysFont(None, 50)

        # Initialize buttons
        self.settings_button = SettingsButton(self)
        self.leaderboard_button = LeaderboardButton(self)

        # Initialize difficulty (default to hard)
        self.difficulty = "hard"

    def message(self, screen, msg, color, y_offset=0, font = None):
        if font is None:
            font = self.font  # 在运行时动态获取
        mesg = font.render(msg, True, color)
        screen.blit(mesg, [WIDTH / 2 - mesg.get_width() / 2, HEIGHT / 2 - mesg.get_height() / 2 + y_offset])

    def draw_border(self, screen, color):
        pygame.draw.rect(screen, color, [0, 0, WIDTH, BORDER_WIDTH])
        pygame.draw.rect(screen, color, [0, 0, BORDER_WIDTH, HEIGHT])
        pygame.draw.rect(screen, color, [0, HEIGHT - BORDER_WIDTH, WIDTH, BORDER_WIDTH])
        pygame.draw.rect(screen, color, [WIDTH - BORDER_WIDTH, 0, BORDER_WIDTH, HEIGHT])

    def show_start_screen(self, screen):
        running = True
        while running:
            screen.fill(BLACK)

            # Draw title and other start screen elements
            self.message(screen, "SNAKE GAME", GREEN, -80, self.large_font)
            self.message(screen, "Press SPACE to Start", WHITE, 40, self.medium_font)

            # Draw the buttons
            self.settings_button.draw(screen)
            self.leaderboard_button.draw(screen)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Handle button clicks
                if self.settings_button.is_clicked(event):
                    self.show_settings_screen(screen)
                if self.leaderboard_button.is_clicked(event):
                    self.show_leaderboard_screen(screen)

                # Handle space key to start game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    running = False

    def show_leaderboard_screen(self, screen):
        # Create text surfaces
        title_text = self.large_font.render("Leaderboard", True, WHITE)
        easy_title = self.font.render("Easy Mode Top 5", True, GREEN)
        hard_title = self.font.render("Hard Mode Top 5", True, RED)
        back_button = BackButton(self)

        # Define column headers and fixed widths
        headers = ["Score", "Time", "Date"]
        col_widths = [100, 80, 120]  # Fixed widths for each column
        base_x = WIDTH // 4 - sum(col_widths) // 2  # Center the table

        running = True
        while running:
            screen.fill(BLACK)

            # Draw title and back button
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
            back_button.draw(screen)

            # Load leaderboard data
            try:
                with open("leaderboard.json", "r") as f:
                    leaderboard_data = json.load(f)
            except:
                leaderboard_data = {"easy": [], "hard": []}

            # Draw easy leaderboard
            screen.blit(easy_title, (WIDTH // 4 - easy_title.get_width() // 2, 120))

            # Draw column headers (centered in their columns)
            for i, (header, width) in enumerate(zip(headers, col_widths)):
                header_text = self.small_font.render(header, True, WHITE)
                screen.blit(header_text, (base_x + sum(col_widths[:i]) + (width - header_text.get_width()) // 2, 170))

            # Sort entries: first by score (descending), then by time (ascending)
            easy_entries = sorted(leaderboard_data["easy"],
                                key=lambda x: (-x["score"], x["time"]))[:5]

            # Draw entries (centered in their columns)
            for i, entry in enumerate(easy_entries):
                # Create text surfaces with fixed formatting
                score_text = self.small_font.render(f"{entry['score']:5d}", True, WHITE)  # 5-digit score
                time_text = self.small_font.render(f"{entry['time']:4.1f}s", True, WHITE)  # 4.1f format
                date_text = self.small_font.render(entry['date'], True, WHITE)

                # Calculate positions with center alignment
                screen.blit(score_text, (base_x + (col_widths[0] - 1.3 * score_text.get_width()) // 2, 200 + i * 30))
                screen.blit(time_text, (base_x + col_widths[0] + (col_widths[1] - time_text.get_width()) // 2, 200 + i * 30))
                screen.blit(date_text, (base_x + col_widths[0] + col_widths[1] + (col_widths[2] - date_text.get_width()) // 2, 200 + i * 30))

            # Draw hard leaderboard
            screen.blit(hard_title, (3 * WIDTH // 4 - hard_title.get_width() // 2, 120))

            # Draw column headers for hard mode
            hard_base_x = 3 * WIDTH // 4 - sum(col_widths) // 2
            for i, (header, width) in enumerate(zip(headers, col_widths)):
                header_text = self.small_font.render(header, True, WHITE)
                screen.blit(header_text, (hard_base_x + sum(col_widths[:i]) + (width - header_text.get_width()) // 2, 170))

            # Sort hard entries same way
            hard_entries = sorted(leaderboard_data["hard"],
                                key=lambda x: (-x["score"], x["time"]))[:5]

            # Draw hard entries
            for i, entry in enumerate(hard_entries):
                score_text = self.small_font.render(f"{entry['score']:5d}", True, WHITE)
                time_text = self.small_font.render(f"{entry['time']:4.1f}s", True, WHITE)
                date_text = self.small_font.render(entry['date'], True, WHITE)

                screen.blit(score_text, (hard_base_x + (col_widths[0] - 1.3* score_text.get_width()) // 2, 200 + i * 30))
                screen.blit(time_text, (hard_base_x + col_widths[0] + (col_widths[1] - time_text.get_width()) // 2, 200 + i * 30))
                screen.blit(date_text, (hard_base_x + col_widths[0] + col_widths[1] + (col_widths[2] - date_text.get_width()) // 2, 200 + i * 30))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if back_button.is_clicked(event):
                    running = False

    def show_settings_screen(self, screen):
        # Create UI elements
        checkbox_size = 20
        checkbox_y_offset = -15  # 微调垂直对齐

        # 计算水平居中位置（将复选框和文字视为一个整体）
        easy_x = WIDTH // 2 - (checkbox_size + 10 + self.font.size("Easy")[0]) // 2
        hard_x = WIDTH // 2 - (checkbox_size + 10 + self.font.size("Hard")[0]) // 2

        easy_checkbox = pygame.Rect(easy_x, HEIGHT // 2 - 50, checkbox_size, checkbox_size)
        hard_checkbox = pygame.Rect(hard_x, HEIGHT // 2, checkbox_size, checkbox_size)

        # Text surfaces
        easy_text = self.font.render("Easy", True, WHITE)
        hard_text = self.font.render("Hard", True, WHITE)
        title_text = self.large_font.render("Settings", True, WHITE)
        back_button = BackButton(self)

        running = True
        while running:
            screen.fill(BLACK)

            # Draw title
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

            # Draw back button
            back_button.draw(screen)

            # Draw checkboxes and labels (now perfectly aligned)
            pygame.draw.rect(screen, WHITE, easy_checkbox, 2)
            if self.difficulty == "easy":
                pygame.draw.rect(screen, GREEN, (easy_checkbox.x + 3, easy_checkbox.y + 3,
                                                 easy_checkbox.width - 6, easy_checkbox.height - 6))

            pygame.draw.rect(screen, WHITE, hard_checkbox, 2)
            if self.difficulty == "hard":
                pygame.draw.rect(screen, GREEN, (hard_checkbox.x + 3, hard_checkbox.y + 3,
                                                 hard_checkbox.width - 6, hard_checkbox.height - 6))

            # 文字位置与复选框水平居中
            screen.blit(easy_text, (easy_checkbox.x + checkbox_size + 30, easy_checkbox.y + checkbox_y_offset))
            screen.blit(hard_text, (hard_checkbox.x + checkbox_size + 30, hard_checkbox.y + checkbox_y_offset))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(event):
                        running = False
                    elif easy_checkbox.collidepoint(event.pos):
                        self.difficulty = "easy"
                    elif hard_checkbox.collidepoint(event.pos):
                        self.difficulty = "hard"