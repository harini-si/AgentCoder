
import pygame
import sys
import random
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PLATFORM_HEIGHT = 20

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - PLATFORM_HEIGHT - self.rect.height
        self.velocity_x = 0
        self.velocity_y = 0
        self.jump_power = -10
        self.gravity = 0.5

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Apply gravity
        self.velocity_y += self.gravity

        # Check boundaries
        if self.rect.y > SCREEN_HEIGHT - PLATFORM_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - PLATFORM_HEIGHT - self.rect.height
            self.velocity_y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.Surface((width, PLATFORM_HEIGHT))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Princess(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = random.choice(platforms).rect.x
        self.rect.y = random.choice(platforms).rect.y - 20

class Fireball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = 0
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

class Game(pygame.sprite.Sprite):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.lives = 15
        self.player = Player()
        self.platforms = [Platform(100, 300, 100),
                          Platform(300, 250, 100),
                          Platform(500, 200, 100),
                          Platform(700, 150, 100),
                          Platform(900, 100, 100)]
        self.princess = Princess(self.platforms)
        self.fireballs = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        for _ in range(10):
            coin = Coin()
            self.coins.add(coin)
        self.all_sprites = pygame.sprite.Group(self.player, self.platforms, self.princess, self.fireballs, self.coins)

    def check_platform_collisions(self):
        for platform in self.platforms:
            if pygame.sprite.collide_rect(self.player, platform):
                if self.player.rect.bottom > platform.rect.centery and self.player.rect.bottom < platform.rect.y + 5:
                    self.player.rect.bottom = platform.rect.y
                    self.player.velocity_y = 0

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.velocity_x = -5
        elif keys[pygame.K_d]:
            self.player.velocity_x = 5
        else:
            self.player.velocity_x = 0

        if keys[pygame.K_w] and self.player.rect.bottom == SCREEN_HEIGHT - PLATFORM_HEIGHT - self.player.rect.height:
            self.player.velocity_y = self.player.jump_power

        self.player.update()
        self.check_platform_collisions()

        if pygame.sprite.spritecollide(self.player, self.fireballs, True):
            self.score -= 25
            self.lives -= 1

        collected_coins = pygame.sprite.spritecollide(self.player, self.coins, True)
        self.score += len(collected_coins) * 5

        if pygame.sprite.collide_rect(self.player, self.princess):
            self.score += 50
            self.princess.rect.x = random.choice(self.platforms).rect.x
            self.princess.rect.y = random.choice(self.platforms).rect.y - 20

        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(30)

        if self.lives <= 0:
            self.game_over = True

        return not self.game_over

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run(pygame.event.poll())
    pygame.quit()
