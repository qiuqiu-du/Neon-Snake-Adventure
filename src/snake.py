from .constants import *
import pygame

def get_snake_color(score):
    color_steps = [
        (0, WHITE),
        (15, CYAN),
        (30, NEON_BLUE),
        (45, LIME_GREEN),
        (60, NEON_YELLOW),
        (75, NEON_ORANGE),
        (90, NEON_PINK),
        (105, ELECTRIC_BLUE),
    ]
    for threshold, color in reversed(color_steps):
        if score >= threshold:
            return color
    return WHITE

def is_near_food(head_x, head_y, food_x, food_y):
    """Check if head is within 2 blocks of food"""
    return (abs(head_x - food_x) <= SNAKE_BLOCK * 3 and
            abs(head_y - food_y) <= SNAKE_BLOCK * 3)

def draw_snake_head(screen, x, y, direction, color, near_food=False):
    # Draw the base square
    pygame.draw.rect(screen, color, [x, y, SNAKE_BLOCK, SNAKE_BLOCK])

    # Calculate eye and mouth positions
    eye_size = SNAKE_BLOCK // 6
    eye_offset = SNAKE_BLOCK // 4
    mouth_thickness = SNAKE_BLOCK // 8
    mouth_length = SNAKE_BLOCK // 3
    mouth_offset = SNAKE_BLOCK // 5  # Distance from edge

    if direction == "RIGHT":
        # Eyes on left side
        left_eye = (x + eye_offset, y + eye_offset)
        right_eye = (x + eye_offset, y + SNAKE_BLOCK - eye_offset)
        # Mouth position
        if near_food:
            # Open mouth (red ellipse)
            mouth_x = x + SNAKE_BLOCK - mouth_offset - 1.5 * mouth_thickness
            mouth_y = y + SNAKE_BLOCK // 2 - mouth_length // 2
            mouth_width = mouth_thickness * 2
            mouth_height = mouth_length
        else:
            # Normal closed mouth
            mouth_x = x + SNAKE_BLOCK - mouth_offset - mouth_thickness
            mouth_y = y + SNAKE_BLOCK // 2 - mouth_length // 2
            mouth_width = mouth_thickness
            mouth_height = mouth_length

    elif direction == "LEFT":
        # Eyes on right side
        left_eye = (x + SNAKE_BLOCK - eye_offset, y + eye_offset)
        right_eye = (x + SNAKE_BLOCK - eye_offset, y + SNAKE_BLOCK - eye_offset)
        # Mouth position
        if near_food:
            mouth_x = x + mouth_offset - 0.5 * mouth_thickness
            mouth_y = y + SNAKE_BLOCK // 2 - mouth_length // 2
            mouth_width = mouth_thickness * 2
            mouth_height = mouth_length

        else:
            mouth_x = x + mouth_offset
            mouth_y = y + SNAKE_BLOCK // 2 - mouth_length // 2
            mouth_width = mouth_thickness
            mouth_height = mouth_length

    elif direction == "UP":
        # Eyes on bottom side
        left_eye = (x + eye_offset, y + SNAKE_BLOCK - eye_offset)
        right_eye = (x + SNAKE_BLOCK - eye_offset, y + SNAKE_BLOCK - eye_offset)
        # Mouth position
        if near_food:
            mouth_x = x + SNAKE_BLOCK // 2 - mouth_length // 2
            mouth_y = y + mouth_offset - 0.5 * mouth_thickness
            mouth_width = mouth_length
            mouth_height = mouth_thickness * 2
        else:
            mouth_x = x + SNAKE_BLOCK // 2 - mouth_length // 2
            mouth_y = y + mouth_offset
            mouth_width = mouth_length
            mouth_height = mouth_thickness

    elif direction == "DOWN":
        # Eyes on top side
        left_eye = (x + eye_offset, y + eye_offset)
        right_eye = (x + SNAKE_BLOCK - eye_offset, y + eye_offset)
        # Mouth position
        if near_food:
            mouth_x = x + SNAKE_BLOCK // 2 - mouth_length // 2
            mouth_y = y + SNAKE_BLOCK - mouth_offset - 1.5 * mouth_thickness
            mouth_width = mouth_length
            mouth_height = mouth_thickness * 2
        else:
            mouth_x = x + SNAKE_BLOCK // 2 - mouth_length // 2
            mouth_y = y + SNAKE_BLOCK - mouth_offset - mouth_thickness
            mouth_width = mouth_length
            mouth_height = mouth_thickness


    # Draw eyes (with white highlights)
    pygame.draw.circle(screen, BLACK, left_eye, eye_size)
    pygame.draw.circle(screen, WHITE, (left_eye[0] + eye_size//3, left_eye[1] - eye_size//3), eye_size//3)
    pygame.draw.circle(screen, BLACK, right_eye, eye_size)
    pygame.draw.circle(screen, WHITE, (right_eye[0] - eye_size//3, right_eye[1] - eye_size//3), eye_size//3)

    if near_food:
        pygame.draw.ellipse(screen, RED,
                            [mouth_x, mouth_y, mouth_width, mouth_height])
    else:
        pygame.draw.rect(screen, BLACK,
                         [mouth_x, mouth_y, mouth_width, mouth_height])