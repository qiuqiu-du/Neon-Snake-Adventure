from .constants import *
import pygame
import os

# 加载蛇身体图片
BODY_IMAGES = {
    'straight': None,
    'turn': None,
    'tail': None,
    'tail-curled': None,  # 蜷缩的尾巴图片
    'head-mo': None,  # 张嘴的头部图片
    'head-mc': None   # 闭嘴的头部图片
}

def load_body_images():
    """加载蛇身体图片资源"""
    try:
        straight = pygame.image.load(os.path.join('assets', 'body', 'straight.png'))
        turn = pygame.image.load(os.path.join('assets', 'body', 'turn.png'))
        tail = pygame.image.load(os.path.join('assets', 'body', 'tail.png'))
        tail_curled = pygame.image.load(os.path.join('assets', 'body', 'tail-curled.png'))
        head_mo = pygame.image.load(os.path.join('assets', 'body', 'head-mo.png'))
        head_mc = pygame.image.load(os.path.join('assets', 'body', 'head-mc.png'))
        
        straight = pygame.transform.scale(straight, (SNAKE_BLOCK, SNAKE_BLOCK))
        turn = pygame.transform.scale(turn, (SNAKE_BLOCK, SNAKE_BLOCK))
        tail = pygame.transform.scale(tail, (SNAKE_BLOCK, SNAKE_BLOCK))
        tail_curled = pygame.transform.scale(tail_curled, (SNAKE_BLOCK, SNAKE_BLOCK))
        head_mo = pygame.transform.scale(head_mo, (SNAKE_BLOCK, SNAKE_BLOCK))
        head_mc = pygame.transform.scale(head_mc, (SNAKE_BLOCK, SNAKE_BLOCK))

        BODY_IMAGES['straight'] = straight.convert_alpha()
        BODY_IMAGES['turn'] = turn.convert_alpha()
        BODY_IMAGES['tail'] = tail.convert_alpha()
        BODY_IMAGES['tail-curled'] = tail_curled.convert_alpha()
        BODY_IMAGES['head-mo'] = head_mo.convert_alpha()
        BODY_IMAGES['head-mc'] = head_mc.convert_alpha()
    except Exception as e:
        print(f"Warning: Snake body images not found. Using default rectangles instead. Error: {e}")

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

def draw_snake_head(screen, snake_list, near_food, color, use_skin=True):
    """绘制蛇的头部"""
    if not snake_list:
        return
        
    snake_Head = snake_list[-1]
    x, y, direction = snake_Head
    
    if not use_skin or not BODY_IMAGES['head-mc']:
        # 如果没有图片资源或不需要使用皮肤，使用默认的矩形绘制
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
    else:
        # 使用图片资源
        image = BODY_IMAGES['head-mo'] if near_food else BODY_IMAGES['head-mc']
        angle = get_rotation_angle(direction)
        if direction == 'LEFT':
            image = pygame.transform.flip(image, False, True)
        rotated_image = pygame.transform.rotate(image, angle)
        screen.blit(rotated_image, (x, y))

def get_rotation_angle(direction):
    """根据方向获取旋转角度"""
    if direction == "RIGHT":
        return 0
    elif direction == "DOWN":
        return 270
    elif direction == "LEFT":
        return 180
    else:  # UP
        return 90

def get_turn_angle(current_direction, next_direction):
    """根据当前方向和下一个方向获取转弯角度"""
    # 定义所有可能的转弯情况
    turn_cases = {
        # 右下方转弯（基准情况）ok
        ("RIGHT", "DOWN"): 0,
        # 左上方转弯（与右下方关于中心对称）
        ("UP", "LEFT"): 270,
        
        # 左下方转弯（与右下方关于垂直中线对称）ok
        ("DOWN", "LEFT"): 270,
        # 右上方转弯（与左下方关于中心对称）
        ("RIGHT", "UP"): 180,
        
        # 左下方转弯（与右下方关于水平中线对称）
        ("LEFT", "DOWN"): 0,
        # 右上方转弯（与左下方关于中心对称）ok
        ("UP", "RIGHT"): 90,
        
        # 左上方转弯（与右下方关于水平中线对称）ok
        ("LEFT", "UP"): 180,
        # 右下方转弯（与左上方关于中心对称）
        ("DOWN", "RIGHT"): 90
    }
    return turn_cases.get((current_direction, next_direction), 0)

def draw_snake_body(screen, snake_list, color, use_skin=True):
    """绘制蛇的身体部分"""
    if not use_skin or not BODY_IMAGES['straight']:
        # 如果没有图片资源或不需要使用皮肤，使用默认的矩形绘制
        for segment in snake_list[0:-1]:
            pygame.draw.rect(screen, color, [segment[0], segment[1], SNAKE_BLOCK, SNAKE_BLOCK])
        return

    # 绘制身体部分
    for i in range(1, len(snake_list) - 1):
        current_pos = snake_list[i]
        current_direction = current_pos[2]
        next_direction = snake_list[i+1][2]
        
        # 选择正确的图片和旋转角度
        if current_direction == next_direction:
            # 直行部分
            image = BODY_IMAGES['straight']
            angle = get_rotation_angle(current_direction)
        else:
            # 转弯部分
            image = BODY_IMAGES['turn']
            angle = get_turn_angle(current_direction, next_direction)
            # 对特定情况水平翻转
            if (current_direction, next_direction) in {("UP", "LEFT"), ("RIGHT", "UP"), 
                                                    ("LEFT", "DOWN"), ("DOWN", "RIGHT")}:
                image = pygame.transform.flip(image, True, False)
        
        # 旋转并绘制图片
        rotated_image = pygame.transform.rotate(image, angle)
        screen.blit(rotated_image, (current_pos[0], current_pos[1]))
    
    # 绘制尾部
    if len(snake_list) > 1:
        tail_pos = snake_list[0]
        tail_direction = tail_pos[2]
        next_direction = snake_list[1][2]
        if tail_direction == next_direction:
            tail_angle = get_rotation_angle(tail_direction)
        else:
            tail_angle = get_rotation_angle(next_direction)
            
        # 根据时间交替显示伸直和蜷缩的尾巴
        current_time = pygame.time.get_ticks()
        is_curled = (current_time // 500) % 2 == 0  # 每0.5秒切换一次
        
        tail_image = BODY_IMAGES['tail-curled'] if is_curled else BODY_IMAGES['tail']
        rotated_tail = pygame.transform.rotate(tail_image, tail_angle)
        screen.blit(rotated_tail, (tail_pos[0], tail_pos[1]))