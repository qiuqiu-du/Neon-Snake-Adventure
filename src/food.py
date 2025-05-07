import random
import time

from .constants import *

def generate_food(game_spawn_time = None, snake_list = None):
    """生成食物，确保不与蛇身体重叠"""
    while True:
        food_type = random.random()
        x = round(random.randrange(BORDER_WIDTH + SNAKE_BLOCK, WIDTH - BORDER_WIDTH - SNAKE_BLOCK * 2) / SNAKE_BLOCK) * SNAKE_BLOCK
        y = round(random.randrange(BORDER_WIDTH + SNAKE_BLOCK, HEIGHT - BORDER_WIDTH - SNAKE_BLOCK * 2) / SNAKE_BLOCK) * SNAKE_BLOCK
        
        # 如果没有蛇身体或位置不重叠，则生成食物
        if snake_list is None or not any(segment[0] == x and segment[1] == y for segment in snake_list):
            if game_spawn_time is None:
                spawn_time = time.time()
            else:
                spawn_time = game_spawn_time

            if food_type <= 0.85:
                return (x, y, GREEN, 1, spawn_time, None)
            elif food_type <= 0.95:
                return (x, y, BLUE, 2, spawn_time, FOOD2_LIFETIME)
            else:
                return (x, y, GOLD, 5, spawn_time, FOOD3_LIFETIME)