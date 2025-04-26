import pygame
import time
from .snake import *
from .buttons import PauseButton
from .food import generate_food
from .ui import UIManager
from .constants import *
from .utils import *


class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.ui_manager = UIManager()
        self.pause_button = PauseButton(self.ui_manager)
        self.direction = "RIGHT"

    def gameLoop(self):
        game_over = False
        game_close = False
        paused = False
        game_active = False
        new_record = False
        start_time = 0
        elapsed_time = 0
        current_score = 0

        x1 = WIDTH / 2
        y1 = HEIGHT / 2
        x1_change = 0
        y1_change = 0

        snake_List = []
        Length_of_snake = 1

        foodx, foody, food_color, food_value, food_spawn_time, food_lifetime = generate_food(elapsed_time)

        self.ui_manager.show_start_screen(self.screen)
        high_score = load_high_score(self.ui_manager.difficulty)
        game_speed = HARD_SPEED if self.ui_manager.difficulty =="hard" else EASY_SPEED

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.pause_button.is_clicked(event):
                    paused = not paused
                    if paused:
                        pause_time = time.time()
                    else:
                        start_time += time.time() - pause_time

                if event.type == pygame.KEYDOWN:
                    if game_active and not game_close and event.key == pygame.K_p:
                        paused = not paused
                        if paused:
                            pause_time = time.time()
                        else:
                            start_time += time.time() - pause_time

                    if not game_active and not game_close and not paused:
                        if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                            game_active = True
                            start_time = time.time()
                            if event.key == pygame.K_LEFT:
                                x1_change = -SNAKE_BLOCK
                                y1_change = 0
                            elif event.key == pygame.K_RIGHT:
                                x1_change = SNAKE_BLOCK
                                y1_change = 0
                            elif event.key == pygame.K_UP:
                                y1_change = -SNAKE_BLOCK
                                x1_change = 0
                            elif event.key == pygame.K_DOWN:
                                y1_change = SNAKE_BLOCK
                                x1_change = 0

                    elif game_active and not paused and not game_close:
                        if event.key == pygame.K_LEFT and x1_change == 0:
                            x1_change = -SNAKE_BLOCK
                            y1_change = 0
                        elif event.key == pygame.K_RIGHT and x1_change == 0:
                            x1_change = SNAKE_BLOCK
                            y1_change = 0
                        elif event.key == pygame.K_UP and y1_change == 0:
                            y1_change = -SNAKE_BLOCK
                            x1_change = 0
                        elif event.key == pygame.K_DOWN and y1_change == 0:
                            y1_change = SNAKE_BLOCK
                            x1_change = 0

                    elif game_close:
                        if event.key == pygame.K_q:
                            game_over = True
                        if event.key == pygame.K_c:
                            return self.gameLoop()

            if game_close:
                self.screen.fill(BLACK)
                self.ui_manager.message(self.screen, "GAME OVER", RED, -80, self.ui_manager.large_font)
                self.ui_manager.message(self.screen, "Press Q-Quit or C-Play Again", WHITE, 0)
                self.ui_manager.message(self.screen, f"Score: {current_score}  High Score: {high_score}", WHITE, 80,self.ui_manager.medium_font)
                if new_record:
                    self.ui_manager.message(self.screen, "New Record !", GOLD, 140,
                                            self.ui_manager.medium_font)
                pygame.display.update()
                continue

            if paused:
                self.screen.fill(BLACK)
                pause_text = self.ui_manager.font.render("PAUSED", True, WHITE)
                continue_text = self.ui_manager.small_font.render("Press P to Resume", True, WHITE)
                self.screen.blit(pause_text,
                                 [WIDTH / 2 - pause_text.get_width() / 2,
                                  HEIGHT / 2 - pause_text.get_height() / 2 - 30])
                self.screen.blit(continue_text, [WIDTH / 2 - continue_text.get_width() / 2, HEIGHT / 2 + 30])
                self.pause_button.draw(self.screen, paused)
                pygame.display.update()
                continue

            if game_active:
                elapsed_time = time.time() - start_time

            if (x1 + SNAKE_BLOCK/2 >= WIDTH - BORDER_WIDTH or x1 + SNAKE_BLOCK/2 < BORDER_WIDTH
                    or y1+ SNAKE_BLOCK/2 >= HEIGHT - BORDER_WIDTH or y1+ SNAKE_BLOCK/2 < BORDER_WIDTH):
                save_game_result(current_score, elapsed_time, self.ui_manager.difficulty)
                game_close = True
            x1 += x1_change
            y1 += y1_change

            self.screen.fill(BLACK)
            self.ui_manager.draw_border(self.screen, get_snake_color(current_score))

            # check if the food should blink
            current_time = time.time()
            food_should_draw = True

            if self.ui_manager.difficulty =="hard":
                if food_lifetime:
                    time_remaining = food_lifetime - (elapsed_time - food_spawn_time)

                    if time_remaining <= 0:
                        foodx, foody, food_color, food_value, food_spawn_time, food_lifetime = generate_food(elapsed_time)
                    elif time_remaining <= BLINK_START:
                        # Blink during last 3 seconds (toggle visibility every second)
                        food_should_draw = int(elapsed_time * 2) % 2 == 0

            # Only draw food if it should be visible
            if food_should_draw:
                pygame.draw.rect(self.screen, food_color, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

            snake_Head = [x1, y1]
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            if x1_change > 0:
                self.direction = "RIGHT"
            elif x1_change < 0:
                self.direction = "LEFT"
            elif y1_change < 0:
                self.direction = "UP"
            elif y1_change > 0:
                self.direction = "DOWN"

            snake_color = get_snake_color(current_score)
            near_food = is_near_food(x1, y1, foodx, foody)
            draw_snake_head(self.screen, snake_Head[0], snake_Head[1],
                          self.direction, snake_color, near_food)
            for x in snake_List[:-1]:
                pygame.draw.rect(self.screen, snake_color, [x[0], x[1], SNAKE_BLOCK, SNAKE_BLOCK])


            if x1 == foodx and y1 == foody:
                Length_of_snake += food_value
                current_score += food_value
                if current_score > high_score:
                    high_score = current_score
                    new_record = True
                foodx, foody, food_color, food_value, food_spawn_time, food_lifetime = generate_food(elapsed_time)

            time_text = self.ui_manager.small_font.render(f"Time: {int(elapsed_time)}s", True, WHITE)
            score_text = self.ui_manager.small_font.render(f"Score: {current_score}  High Score: {high_score}  easy", True, WHITE)
            self.screen.blit(time_text, [10, 10])
            self.screen.blit(score_text, [WIDTH / 2 - score_text.get_width() / 2, 10])

            # Always draw the pause button
            self.pause_button.draw(self.screen, paused)

            pygame.display.update()
            self.clock.tick(game_speed)

        pygame.quit()
        exit()