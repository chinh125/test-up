import enum
from typing import List
import random
import pygame
from common import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, RED, BLUE, FPS

# Khởi tạo Pygame
pygame.init()

# Tạo màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hứng hoa quả")
clock = pygame.time.Clock()

# Load các sprite và scale chúng
BACKGROUND_SPRITE = pygame.image.load("assets/c550ba8f791e8b559ac51285648a47d6.jpg").convert_alpha()
BACKGROUND_SPRITE.set_alpha(128)
BACKGROUND_SPRITE = pygame.transform.scale(BACKGROUND_SPRITE, [SCREEN_WIDTH, SCREEN_HEIGHT])

APPLE_SPRITE = pygame.transform.scale(pygame.image.load("assets/items/apple-5902283_960_720.webp"), (50, 50))
STRAWBERRY_SPRITE = pygame.transform.scale(pygame.image.load("assets/items/strawberry-7895270_960_720.webp"), (50, 50))
BOMB_SPRITE = pygame.transform.scale(pygame.image.load("assets/items/bomb-png-5a371a5a414438.7272917215135606662673-removebg-preview.png"), (70, 50))
PLAYER_SPRITE_LEFT = pygame.transform.scale(pygame.image.load("assets/players/player_1.png"), (100, 100))
PLAYER_SPRITE_RIGHT = pygame.transform.scale(pygame.image.load("assets/players/player_2.png"), (100, 100))
PLAYER_JUMP_LEFT = pygame.transform.scale(pygame.image.load("assets/players/player_jump_1.png"), (100, 100))
PLAYER_JUMP_RIGHT = pygame.transform.scale(pygame.image.load("assets/players/player_jump_2.png"), (100, 100))

# Thêm các phím mới cho chức năng nhảy
JUMP_KEY = pygame.K_UP

class Player:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        self.image_left: pygame.Surface = PLAYER_SPRITE_LEFT
        self.image_right: pygame.Surface = PLAYER_SPRITE_RIGHT
        self.image_jump_left: pygame.Surface = PLAYER_JUMP_LEFT
        self.image_jump_right: pygame.Surface = PLAYER_JUMP_RIGHT
        self.image: pygame.Surface = self.image_left  # Mặc định là hình quay trái
        self.move_speed = 6  # Tốc độ di chuyển bên trái và bên phải
        self.jump_speed = 10  # Tốc độ nhảy
        self.move_left_pressed = False
        self.move_right_pressed = False
        self.jump_pressed = False
        self.jumping = False  # Trạng thái nhảy
        self.jump_height = 150  # Độ cao của nhảy
        self.jump_remaining = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_left_pressed = True
                self.image = self.image_right  # Chuyển hình sang trái
            elif event.key == pygame.K_RIGHT:
                self.move_right_pressed = True
                self.image = self.image_left  # Chuyển hình sang phải
            elif event.key == JUMP_KEY and not self.jump_pressed and not self.jumping:
                self.jump_pressed = True
                self.jumping = True
                self.jump_remaining = self.jump_height
                # Xác định hướng nhảy
                if self.image == self.image_left:
                    self.image = self.image_jump_left
                elif self.image == self.image_right:
                    self.image = self.image_jump_right
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.move_left_pressed = False
            elif event.key == pygame.K_RIGHT:
                self.move_right_pressed = False
            elif event.key == JUMP_KEY:
                self.jump_pressed = False

    def update(self):
        if self.move_left_pressed:
            self.move_left()
        elif self.move_right_pressed:
            self.move_right()
        if self.jump_remaining > 0:
            self.jump()
        elif self.jumping:
            self.fall()  # Rơi xuống sau khi nhảy
        else:
            # Kiểm tra hướng di chuyển trước khi cập nhật hình ảnh
            if self.image == self.image_jump_left:
                self.image = self.image_left
            elif self.image == self.image_jump_right:
                self.image = self.image_right

    def move_left(self) -> None:
        self.x -= self.move_speed
        if self.x < 0:
            self.x = 0

    def move_right(self) ->None:
        self.x += self.move_speed
        if self.x > SCREEN_WIDTH - self.image.get_width():
            self.x = SCREEN_WIDTH - self.image.get_width()

    def jump(self):
        self.y -= self.jump_speed
        self.jump_remaining -= self.jump_speed
        if self.jump_remaining <= 0:
            self.jump_remaining = 0

    def fall(self):
        self.y += self.jump_speed
        if self.y >= SCREEN_HEIGHT - self.image.get_height():
            self.y = SCREEN_HEIGHT - self.image.get_height()
            self.jumping = False  # Kết thúc quá trình rơi xuống

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)  # Tạo một đối tượng Player

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
        self.fall_speed = 4

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

# Khởi tạo danh sách các quả
list_items: List[FruitItem] = [
    FruitItem(random.randint(0, SCREEN_WIDTH - 50), random.randint(-300, -100), ItemType.APPLE),
    FruitItem(random.randint(0, SCREEN_WIDTH - 50), random.randint(-390, -100), ItemType.STRAWBERRY),
    FruitItem(random.randint(0, SCREEN_WIDTH - 50), random.randint(-500, -100), ItemType.APPLE),
    FruitItem(random.randint(0, SCREEN_WIDTH - 50), random.randint(-200, -100), ItemType.STRAWBERRY),
    FruitItem(random.randint(0, SCREEN_WIDTH - 50), random.randint(-250, -100), ItemType.BOMB),
    FruitItem(random.randint(0, SCREEN_WIDTH - 50), random.randint(-350, -100), ItemType.BOMB),
]

def collision(player, fruit):
    player_rect = pygame.Rect(player.x, player.y, player.image.get_width(), player.image.get_height())
    fruit_rect = pygame.Rect(fruit.x, fruit.y, fruit.image.get_width(), fruit.image.get_height())
    return player_rect.colliderect(fruit_rect)


def calculate_score(player, item, score, collision_handled):
    if not collision_handled and collision(player, item):
        collision_handled = True
        if item.type == ItemType.APPLE or item.type == ItemType.STRAWBERRY:
            score += 10
        else:
            score = 0
        item.reset()
    else:
        collision_handled = False
    return score, collision_handled

score = 0
font = pygame.font.SysFont(None, 36)
PLAY_TIME = 10
time_remaining = PLAY_TIME * FPS
# Khởi tạo biến cờ để kiểm tra va chạm
collision_handled = False
game_over = False

# Vòng lặp chính của trò chơi
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            player.handle_event(event)
    player.update()
    # Xóa màn hình
    screen.fill(WHITE)

    # Hiển thị hình nền
    screen.blit(BACKGROUND_SPRITE, (0, 0))

    # Cập nhật và hiển thị các quả
    for item in list_items:
        item.update()
        screen.blit(item.image, (item.x, item.y))

        # Tính điểm
        score, collision_handled = calculate_score(player, item, score, collision_handled)

        # Kiểm tra va chạm giữa người và quả
        if collision(player, item):
            print("Collision occurred!")

    # Hiển thị người
    screen.blit(player.image, (player.x, player.y))

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

    # Kiểm tra kết thúc trò chơi
    if time_remaining <= 0:
        game_over = True

    # Giảm thời gian còn lại sau mỗi khung hình
    if not game_over:
        time_remaining -= 1

# Kết thúc Pygame
pygame.quit()