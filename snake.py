from constants import *

def get_snake_color(score):
    color_steps = [
        (0, WHITE),
        (15, PURPLE),
        (30, ORANGE),
        (45, CYAN),
        (60, PINK),
        (75, GOLD)
    ]
    for threshold, color in reversed(color_steps):
        if score >= threshold:
            return color
    return WHITE