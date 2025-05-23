import time
import random
import pygame
from .constants import *
from .snake import draw_snake_head,draw_snake_body, is_near_food, get_snake_color
from .food import generate_food

class BackgroundGame:
    def __init__(self, screen, ui_manager, difficulty="hard"):
        self.screen = screen
        self.ui_manager = ui_manager
        self.difficulty = difficulty
        self.reset_game()
        self.last_update = time.time()
        # Set update interval based on difficulty
        self.update_interval = 1.0 / (EASY_SPEED if difficulty == "easy" else HARD_SPEED)
        self.last_direction_change = time.time()
        self.current_direction_duration = 0
        self.min_direction_duration = 0.05  # Minimum time to keep same direction (seconds)

    def reset_game(self):
        self.x1 = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
        self.y1 = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
        self.x1_change = SNAKE_BLOCK
        self.y1_change = 0
        self.snake_List = []
        self.length_of_snake = 1
        self.current_score = 0
        self.start_time = time.time()
        self.foodx, self.foody, self.food_color, self.food_value, self.food_spawn_time, self.food_lifetime = generate_food(0, self.snake_List)
        self.direction = "RIGHT"
        self.game_active = True
        self.last_direction_change = time.time()
        self.current_direction_duration = 0

    def update(self):
        current_time = time.time()
        if current_time - self.last_update < self.update_interval or not self.game_active:
            return
        self.last_update = current_time
        self.current_direction_duration = current_time - self.last_direction_change

        # AI decision making - more human-like algorithm
        if self.game_active:
            possible_moves = self.get_possible_moves(self.direction)
            best_move = self.choose_best_move(possible_moves)

            # Only change direction if it's safe and better
            if best_move != self.direction and self.current_direction_duration >= self.min_direction_duration:
                if best_move == "LEFT" and self.x1_change == 0:
                    self.x1_change = -SNAKE_BLOCK
                    self.y1_change = 0
                    self.last_direction_change = current_time
                    self.direction = "LEFT"
                elif best_move == "RIGHT" and self.x1_change == 0:
                    self.x1_change = SNAKE_BLOCK
                    self.y1_change = 0
                    self.last_direction_change = current_time
                    self.direction = "RIGHT"
                elif best_move == "UP" and self.y1_change == 0:
                    self.y1_change = -SNAKE_BLOCK
                    self.x1_change = 0
                    self.last_direction_change = current_time
                    self.direction = "UP"
                elif best_move == "DOWN" and self.y1_change == 0:
                    self.y1_change = SNAKE_BLOCK
                    self.x1_change = 0
                    self.last_direction_change = current_time
                    self.direction = "DOWN"

            # Update snake position
            self.x1 += self.x1_change
            self.y1 += self.y1_change

            # Check wall collision
            if (self.x1 + SNAKE_BLOCK / 2 >= WIDTH or self.x1 + SNAKE_BLOCK / 2 < 0
                    or self.y1 + SNAKE_BLOCK / 2 >= HEIGHT or self.y1 + SNAKE_BLOCK / 2 < 0):
                self.reset_game()
                return

            # Update snake body
            snake_Head = [self.x1, self.y1, self.direction]
            self.snake_List.append(snake_Head)
            if len(self.snake_List) > self.length_of_snake:
                del self.snake_List[0]

            # Check self collision
            for x in self.snake_List[:-1]:
                if x[0] == snake_Head[0] and x[1] == snake_Head[1]:
                    self.reset_game()
                    return

            # Check food collision
            if self.x1 == self.foodx and self.y1 == self.foody:
                self.current_score += self.food_value
                self.length_of_snake += self.food_value
                self.foodx, self.foody, self.food_color, self.food_value, self.food_spawn_time, self.food_lifetime = generate_food(
                    time.time() - self.start_time, self.snake_List)

    def get_possible_moves(self,current_direction):
        moves = []
        # Check if moves are valid (won't hit wall or self)
        # Left
        if (self.x1 + SNAKE_BLOCK / 2 - SNAKE_BLOCK >= 0 and 
            not any(x[0] == self.x1 - SNAKE_BLOCK and x[1] == self.y1 for x in self.snake_List[:-1])
            and current_direction != "RIGHT"):
            moves.append("LEFT")
        # Right
        if (self.x1 + SNAKE_BLOCK / 2 + SNAKE_BLOCK < WIDTH and 
            not any(x[0] == self.x1 + SNAKE_BLOCK and x[1] == self.y1 for x in self.snake_List[:-1])
            and current_direction != "LEFT"):
            moves.append("RIGHT")
        # Up
        if (self.y1 + SNAKE_BLOCK / 2  - SNAKE_BLOCK >= 0 and 
            not any(x[0] == self.x1 and x[1] == self.y1 - SNAKE_BLOCK for x in self.snake_List[:-1])
            and current_direction != "DOWN"):
            moves.append("UP")
        # Down
        if (self.y1 + SNAKE_BLOCK / 2  + SNAKE_BLOCK < HEIGHT and 
            not any(x[0] == self.x1 and x[1] == self.y1 + SNAKE_BLOCK for x in self.snake_List[:-1])
            and current_direction != "UP"):
            moves.append("DOWN")

        return moves if moves else ["LEFT", "RIGHT", "UP", "DOWN"]  # If no safe moves, return all (will die)

    def choose_best_move(self, possible_moves):
        # Prefer current direction if it's safe and aligned with food
        current_direction = self.direction
        if current_direction in possible_moves:
            if (current_direction == "LEFT" and self.foodx < self.x1) or \
                    (current_direction == "RIGHT" and self.foodx > self.x1) or \
                    (current_direction == "UP" and self.foody < self.y1) or \
                    (current_direction == "DOWN" and self.foody > self.y1):
                return current_direction

        # Otherwise, choose direction that minimizes distance to food
        best_move = []
        min_distance = float('inf')

        for move in possible_moves:
            if move == "LEFT":
                new_x = self.x1 - SNAKE_BLOCK
                new_y = self.y1
            elif move == "RIGHT":
                new_x = self.x1 + SNAKE_BLOCK
                new_y = self.y1
            elif move == "UP":
                new_x = self.x1
                new_y = self.y1 - SNAKE_BLOCK
            elif move == "DOWN":
                new_x = self.x1
                new_y = self.y1 + SNAKE_BLOCK

            distance = ((new_x - self.foodx) ** 2 + (new_y - self.foody) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                best_move = [move]
            elif distance == min_distance:
                min_distance = distance
                best_move.append(move)

        return random.choice(best_move) if best_move else random.choice(possible_moves)

    def draw(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))

        # Draw food
        pygame.draw.ellipse(self.screen, self.food_color, [self.foodx, self.foody, SNAKE_BLOCK/1.05, SNAKE_BLOCK/1.05])

        # Draw snake
        snake_color = get_snake_color(self.current_score)
        near_food = is_near_food(self.x1, self.y1, self.foodx, self.foody)
        draw_snake_head(self.screen, self.snake_List, near_food, snake_color, use_skin=False)
        draw_snake_body(self.screen, self.snake_List, snake_color, use_skin=False)
