import enum
from typing import Tuple, List

import random
import pygame
from common import SCREEN_WIDTH,SCREEN_HEIGHT,WHITE,RED,BLUE,FPS

# Khởi tạo Pygame
pygame.init()

# Tạo màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hứng hoa quả")
clock = pygame.time.Clock()

# Load các sprite và scale chúng
BACKGROUND_SPRITE = pygame.image.load("assets/background.jpg").convert_alpha()
BACKGROUND_SPRITE.set_alpha(128)
BACKGROUND_SPRITE = pygame.transform.scale(BACKGROUND_SPRITE, [SCREEN_WIDTH, SCREEN_HEIGHT])

APPLE_SPRITE = pygame.transform.scale(pygame.image.load("assets/apple-5902283_960_720.webp"), (50, 50))
STRAWBERRY_SPRITE = pygame.transform.scale(pygame.image.load("assets/strawberry-7895270_960_720.webp"), (50, 50))
BOMB_SPRITE = pygame.transform.scale(pygame.image.load("assets/z5289339670048_73bc8aa2488b04d55eaee73a671332b5.jpg"), (50, 50))
BASKET_SPRITE = pygame.transform.scale(pygame.image.load("assets/basket.jpg"), (100, 100))


# Khai báo lớp giỏ
class Basket:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        self.image: pygame.Surface = BASKET_SPRITE
        self.move_speed = 5  # Adjust speed as needed
        self.move_left_pressed = False
        self.move_right_pressed = False


    def handle_event(self, event): #Hàm di chuyển để hứng quả
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_left_pressed = True
            elif event.key == pygame.K_RIGHT:
                self.move_right_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.move_left_pressed = False
            elif event.key == pygame.K_RIGHT:
                self.move_right_pressed = False

    def update(self):
        if self.move_left_pressed:
            self.move_left()
        elif self.move_right_pressed:
            self.move_right()

    def move_left(self) -> None:
        self.x -= self.move_speed
        if self.x < 0:
            self.x = 0

    def move_right(self) ->None:
        self.x += self.move_speed
        if self.x > SCREEN_WIDTH - self.image.get_width():
            self.x = SCREEN_WIDTH - self.image.get_width()
# Khai báo enum loại hoa quả
class ItemType(enum.Enum):
    APPLE = 0
    STRAWBERRY = 1
    BOMB = 2


# Khai báo lớp quả
class FruitItem:
    def __init__(self, x: float, y: float, type: ItemType) -> None:
        self.x: float = x
        self.y: float = y
        self.type: ItemType = type

        if type == ItemType.APPLE:
            self.image = APPLE_SPRITE
        elif type == ItemType.STRAWBERRY:
            self.image = STRAWBERRY_SPRITE
        else:
            self.image = BOMB_SPRITE
        self.fall_speed = random.randint(2, 5)

    def update(self) -> None:
        # Cập nhật vị trí của quả
        self.y += self.fall_speed

        # Kiểm tra nếu quả rơi xuống dưới cùng màn hình
        if self.y > SCREEN_HEIGHT:
            self.reset()

    def reset(self) -> None:
        # Đặt lại vị trí của quả khi rơi xuống dưới cùng màn hình
        self.x = random.randint(0, SCREEN_WIDTH - self.image.get_width())  # Vị trí ngẫu nhiên
        self.y = random.randint(-200, -100)  # Vị trí ở trên đỉnh màn hình
        self.fall_speed = random.randint(2, 5)  # Tốc độ rơi ngẫu nhiên mới

def collision(basket, fruit):
    basket_rect = pygame.Rect(basket.x, basket.y, basket.image.get_width(), basket.image.get_height())
    fruit_rect = pygame.Rect(fruit.x, fruit.y, fruit.image.get_width(), fruit.image.get_height())
    return basket_rect.colliderect(fruit_rect)


def calculate_score(basket, item, score, collision_handled):
    if not collision_handled and collision(basket, item):
        collision_handled = True
        if item.type == ItemType.APPLE or item.type == ItemType.STRAWBERRY:
            score += 10
        else:
            score -= 5
        item.reset()
    else:
        collision_handled = False
    return score, collision_handled

score = 0
font = pygame.font.SysFont(None, 36)
PLAY_TIME = 10
WINNING_SCORE = 50
time_remaining = PLAY_TIME * FPS
collision_handled = False
game_over = False
MAX_APPLES = 5
MAX_STRAWBERRIES = 3
MAX_BOMBS = 2
apple_timer = 0
strawberry_timer = 0
bomb_timer = 0

# Khởi tạo giỏ
basket = Basket(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)

# Khởi tạo danh sách các quả
list_items: List[FruitItem] = []

# Thời gian giữa mỗi quả mới xuất hiện (đơn vị: frame)
TIME_BETWEEN_FRUITS = 60

# Vòng lặp chính của trò chơi
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            basket.handle_event(event)
    basket.update()

    # Xóa màn hình
    screen.fill(WHITE)

    # Hiển thị hình nền
    screen.blit(BACKGROUND_SPRITE, (0, 0))

    # Cập nhật và hiển thị các quả
    for item in list_items:
        item.update()
        screen.blit(item.image, (item.x, item.y))
        # Kiểm tra va chạm giữa giỏ và quả
        if collision(basket, item):
            print("Collision occurred!")
            score, collision_handled = calculate_score(basket, item, score, collision_handled)

    # Hiển thị giỏ
    screen.blit(basket.image, (basket.x, basket.y))

    # Hiển thị điểm số
    text = font.render("Score: " + str(score), True, RED)
    screen.blit(text, (10, 10))

    # Hiển thị thời gian còn lại
    time_text = font.render("Time: " + str(max(0, time_remaining // FPS)), True, BLUE)
    screen.blit(time_text, (350, 10))

    # Cập nhật màn hình
    pygame.display.flip()

    # Đặt tốc độ khung hình
    clock.tick(FPS)

    # Giảm thời gian còn lại sau mỗi khung hình
    if not game_over:
        time_remaining -= 1

    # Kiểm tra thời gian và tạo một quả mới nếu thời gian đạt đến
    apple_timer += 1
    if apple_timer >= TIME_BETWEEN_FRUITS:
        new_fruit = FruitItem(random.randint(0, SCREEN_WIDTH - 50), random.randint(-200, -100), ItemType.APPLE)
        list_items.append(new_fruit)
        apple_timer = 0  # Đặt lại biến đếm thời gian cho quả táo

    strawberry_timer += 1
    if strawberry_timer >= TIME_BETWEEN_FRUITS:
        new_fruit = FruitItem(random.randint(0, SCREEN_WIDTH - 50), random.randint(-200, -100), ItemType.STRAWBERRY)
        list_items.append(new_fruit)
        strawberry_timer = 0  # Đặt lại biến đếm thời gian cho quả dâu

    bomb_timer += 1
    if bomb_timer >= TIME_BETWEEN_FRUITS:
        new_fruit = FruitItem(random.randint(0, SCREEN_WIDTH - 50), random.randint(-200, -100), ItemType.BOMB)
        list_items.append(new_fruit)
        bomb_timer = 0  # Đặt lại biến đếm thời gian cho quả bom

    # Kiểm tra va chạm với biên của màn hình
    if basket.x < 0:
        basket.x = 0
    elif basket.x > SCREEN_WIDTH - basket.image.get_width():
        basket.x = SCREEN_WIDTH - basket.image.get_width()

# Kết thúc Pygame
pygame.quit()
