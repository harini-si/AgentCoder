
import pygame
import sys
import random
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_COLOR = (100, 100, 100)
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 40
PLAYER_COLOR = (0, 255, 0)
PRINCESS_WIDTH = 20
PRINCESS_HEIGHT = 40
PRINCESS_COLOR = (255, 0, 255)
FIREBALL_WIDTH = 20
FIREBALL_HEIGHT = 20
FIREBALL_COLOR = (255, 0, 0)
COIN_WIDTH = 15
COIN_HEIGHT = 15
COIN_COLOR = (255, 255, 0)
FIREBALL_SPEED = 5
COIN_POINTS = 5

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(topleft=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT))
        self.velocity = pygame.math.Vector2(0, 0)
        self.jump_power = -15
        self.gravity = 0.8
        
    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.velocity.x = -5
        elif keys[pygame.K_d]:
            self.velocity.x = 5
        else:
            self.velocity.x = 0
            
        if keys[pygame.K_w] and self.rect.colliderect(ground.rect):
            self.velocity.y = self.jump_power
            
        self.velocity.y += self.gravity
        self.rect.move_ip(self.velocity.x, self.velocity.y)
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity.y > 0:
                self.rect.bottom = platform.rect.top
                self.velocity.y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))

class Princess(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PRINCESS_WIDTH, PRINCESS_HEIGHT))
        self.image.fill(PRINCESS_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((FIREBALL_WIDTH, FIREBALL_HEIGHT))
        self.image.fill(FIREBALL_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, platforms):
        self.rect.y += FIREBALL_SPEED
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((COIN_WIDTH, COIN_HEIGHT))
        self.image.fill(COIN_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))

class Game(pygame.sprite.Sprite):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()
        
    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.lives = 15
        self.player = Player()
        self.princess = None
        self.platforms = []
        self.fireballs = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.create_level()
        self.spawn_princess()
        self.spawn_coins()
        
    def create_level(self):
        ground = Platform(0, SCREEN_HEIGHT - 20)
        self.platforms.append(ground)
        for i in range(5):
            x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
            y = random.randint(100, SCREEN_HEIGHT - 200)
            platform = Platform(x, y)
            self.platforms.append(platform)

    def spawn_princess(self):
        platform = random.choice(self.platforms)
        self.princess = Princess(platform.rect.x + platform.rect.width // 2 - PRINCESS_WIDTH // 2, platform.rect.y - PRINCESS_HEIGHT)

    def spawn_fireball(self):
        x = random.randint(0, SCREEN_WIDTH - FIREBALL_WIDTH)
        fireball = Fireball(x, 0)
        self.fireballs.add(fireball)

    def spawn_coins(self):
        for _ in range(10):
            x = random.randint(0, SCREEN_WIDTH - COIN_WIDTH)
            y = random.randint(100, SCREEN_HEIGHT - 200)
            coin = Coin(x, y)
            self.coins.add(coin)

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
        self.screen.fill((255, 255, 255))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return False

        self.player.update(self.platforms)
        self.screen.blit(self.player.image, self.player.rect)

        for platform in self.platforms:
            self.screen.blit(platform.image, platform.rect)

        for coin in self.coins:
            self.screen.blit(coin.image, coin.rect)
            if self.player.rect.colliderect(coin.rect):
                self.score += COIN_POINTS
                coin.kill()
                
        for fireball in self.fireballs:
            fireball.update(self.platforms)
            self.screen.blit(fireball.image, fireball.rect)
            if self.player.rect.colliderect(fireball.rect):
                self.lives -= 1
                self.score -= 25
                fireball.kill()

        if self.player.rect.colliderect(self.princess.rect):
            self.score += 50
            self.spawn_princess()

        font = pygame.font.SysFont(None, 36)
        score_text = font.render('Score: ' + str(self.score), True, (0, 0, 0))
        lives_text = font.render('Lives: ' + str(self.lives), True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))

        pygame.display.flip()
        self.clock.tick(30)

        if self.lives <= 0:
            return False

        return True

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    game = Game()
    running = True
    while running:
        running = game.run(pygame.event.poll())
    pygame.quit()
