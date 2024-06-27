
import pygame
import sys
import random
import math

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PLATFORM_WIDTH = 200
PLATFORM_HEIGHT = 20
PLATFORM_COLOR = (128, 128, 128)
PLAYER_COLOR = (0, 255, 0)
PRINCESS_COLOR = (255, 0, 0)
COIN_COLOR = (255, 255, 0)
FIREBALL_COLOR = (255, 165, 0)
PLAYER_SPEED = 5
JUMP_HEIGHT = 25
GRAVITY = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - 50
        self.y_speed = 0
        
    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_w]:
            self.jump()
        self.apply_gravity()
        
        self.check_collision(platforms)
        
    def jump(self):
        self.rect.y -= JUMP_HEIGHT
        self.y_speed = -JUMP_HEIGHT
        
    def apply_gravity(self):
        self.rect.y += self.y_speed
        self.y_speed += GRAVITY
        
    def check_collision(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.rect.bottom = platform.rect.top
                self.y_speed = 0
            
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Princess(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(PRINCESS_COLOR)
        self.rect = self.image.get_rect()
        self.set_position(platforms)
        
    def set_position(self, platforms):
        platform = random.choice(platforms)
        self.rect.x = random.randint(platform.rect.left, platform.rect.right)
        self.rect.y = platform.rect.top - 50

class Coin(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(COIN_COLOR)
        self.rect = self.image.get_rect()
        self.set_position(platforms)
        
    def set_position(self, platforms):
        platform = random.choice(platforms)
        self.rect.x = random.randint(platform.rect.left, platform.rect.right)
        self.rect.y = random.randint(platform.rect.top - 50, platform.rect.top - 20)

class Fireball(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(FIREBALL_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH)
        self.rect.y = 0
        self.y_speed = 5
        
    def update(self, platforms):
        self.rect.y += self.y_speed
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.rect.y = platform.rect.top - 20
                self.y_speed = 0

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()
        
    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.lives = 15
        self.player = Player()
        self.platforms = [Platform(0, 800), Platform(300, 700), Platform(600, 600), Platform(200, 500), Platform(500, 400)]
        self.princess = Princess(self.platforms)
        self.coins = [Coin(self.platforms) for _ in range(10)]
        self.fireballs = []
        
    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        if not self.game_over:
            self.screen.fill((0, 0, 0))
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w]:
                self.player.update(self.platforms)
                
            self.screen.blit(self.player.image, self.player.rect)
            for platform in self.platforms:
                self.screen.blit(platform.image, platform.rect)
            self.screen.blit(self.princess.image, self.princess.rect)
            for coin in self.coins:
                self.screen.blit(coin.image, coin.rect)
            for fireball in self.fireballs:
                fireball.update(self.platforms)
                self.screen.blit(fireball.image, fireball.rect)
            
            pygame.display.flip()
            self.clock.tick(30)
            
        else:
            print("Game Over")
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        game.run(pygame.event.poll())
