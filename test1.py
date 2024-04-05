import pygame
import random
import sys

# Khởi tạo màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Khởi tạo cấu hình màn hình
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Khởi tạo game
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Color Swap Challenge")
        self.clock = pygame.time.Clock()
        self.square_size = 50
        self.square_x = SCREEN_WIDTH // 2 - self.square_size // 2
        self.square_y = SCREEN_HEIGHT - self.square_size * 2
        self.square_color = WHITE
        self.obstacle_color = random.choice([RED, GREEN, BLUE])
        self.obstacle_y = 0
        self.obstacle_speed = 5
        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.change_color()

            self.screen.fill(WHITE)

            # Vẽ hình vuông
            pygame.draw.rect(self.screen, self.square_color, (self.square_x, self.square_y, self.square_size, self.square_size))

            # Vẽ chướng ngại vật
            pygame.draw.rect(self.screen, self.obstacle_color, (0, self.obstacle_y, SCREEN_WIDTH, self.square_size))

            # Di chuyển chướng ngại vật
            self.obstacle_y += self.obstacle_speed
            if self.obstacle_y > SCREEN_HEIGHT:
                self.obstacle_y = 0
                self.obstacle_color = random.choice([RED, GREEN, BLUE])
                self.score += 1

            # Kiểm tra va chạm
            if self.square_y < self.obstacle_y + self.square_size and self.square_x < SCREEN_WIDTH // 2:
                if self.square_color == self.obstacle_color:
                    running = False

            # Hiển thị điểm số
            score_text = self.font.render("Score: " + str(self.score), True, (0, 0, 0))
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)

    def change_color(self):
        colors = [WHITE, RED, GREEN, BLUE]
        colors.remove(self.square_color)
        self.square_color = random.choice(colors)

if __name__ == "__main__":
    game = Game()
    game.run()
