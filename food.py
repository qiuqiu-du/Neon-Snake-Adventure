import random
import time
from constants import *

def generate_food():
    food_type = random.random()
    x = round(random.randrange(BORDER_WIDTH + SNAKE_BLOCK, WIDTH - BORDER_WIDTH - SNAKE_BLOCK * 2) / SNAKE_BLOCK) * SNAKE_BLOCK
    y = round(random.randrange(BORDER_WIDTH + SNAKE_BLOCK, HEIGHT - BORDER_WIDTH - SNAKE_BLOCK * 2) / SNAKE_BLOCK) * SNAKE_BLOCK
    spawn_time = time.time()

    if food_type <= 0.85:
        return (x, y, GREEN, 1, spawn_time, None)
    elif food_type <= 0.95:
        return (x, y, BLUE, 2, spawn_time, FOOD2_LIFETIME)
    else:
        return (x, y, GOLD, 5, spawn_time, FOOD3_LIFETIME)