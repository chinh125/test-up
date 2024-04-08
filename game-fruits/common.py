from pygame import color

SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600

FPS: int = 60

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# # Load các sprite và scale chúng
# BACKGROUND_SPRITE = pygame.image.load("assets/c550ba8f791e8b559ac51285648a47d6.jpg").convert_alpha()
# BACKGROUND_SPRITE.set_alpha(128)
# BACKGROUND_SPRITE = pygame.transform.scale(BACKGROUND_SPRITE, [SCREEN_WIDTH, SCREEN_HEIGHT])

# APPLE_SPRITE = pygame.transform.scale(pygame.image.load("assets/items/apple-5902283_960_720.webp"), (50, 50))
# STRAWBERRY_SPRITE = pygame.transform.scale(pygame.image.load("assets/items/strawberry-7895270_960_720.webp"), (50, 50))
# BOMB_SPRITE = pygame.transform.scale(pygame.image.load("assets/items/bomb-png-5a371a5a414438.7272917215135606662673-removebg-preview.png"), (70, 50))
# PLAYER_SPRITE_LEFT = pygame.transform.scale(pygame.image.load("assets/players/player_left.png"), (100, 100))
# PLAYER_SPRITE_RIGHT = pygame.transform.scale(pygame.image.load("assets/players/player_right.png"), (100, 100))
# PLAYER_JUMP_LEFT = pygame.transform.scale(pygame.image.load("assets/players/player_jump_left.png"), (100, 100))
# PLAYER_JUMP_RIGHT = pygame.transform.scale(pygame.image.load("assets/players/player_jump_right.png"), (100, 100))