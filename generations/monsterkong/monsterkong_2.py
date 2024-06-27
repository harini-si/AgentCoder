
import pygame
import sys
import random
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN_HEIGHT  # Start at the bottom of the screen
        self.rect.centerx = SCREEN_WIDTH // 2
        self.player_speed = 5
        self.player_jump = 15
        self.velocity = 0
        self.on_ground = True

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.player_speed
        if keys[pygame.K_d]:
            self.rect.x += self.player_speed

        if keys[pygame.K_w] and self.on_ground:
            self.velocity = -self.player_jump
            self.on_ground = False

        self.velocity += 0.8  # Gravity
        self.rect.y += self.velocity

        self.on_ground = False  # Reset flag
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity = 0
                    self.on_ground = True

        if self.rect.top >= SCREEN_HEIGHT:  # Fall off the screen
            self.rect.bottom = 0
            self.velocity = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((80, 20))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Princess(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 255))
        self.rect = self.image.get_rect()
        self.reset_position(platforms)

    def reset_position(self, platforms):
        platform = random.choice(platforms)
        self.rect.centerx = random.randint(platform.rect.left, platform.rect.right)
        self.rect.bottom = platform.rect.top

class Fireball(pygame.sprite.Sprite):
    def __init__(self, yPos):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = yPos

    def update(self, platforms):
        self.rect.y += 5
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platformer Game")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.lives = 15
        self.player = Player()
        self.platforms = [Platform(200, 600), Platform(400, 500), Platform(600, 400), Platform(300, 300), Platform(700, 200)]
        self.princess = Princess(self.platforms)
        self.coins = pygame.sprite.Group([Coin() for _ in range(10)])
        self.fireballs = pygame.sprite.Group()

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.fill((0, 0, 0))

        self.player.update(self.platforms)

        if random.randint(0, 100) < 3:
            self.fireballs.add(Fireball(0))

        self.fireballs.update(self.platforms)

        self.screen.blit(self.player.image, self.player.rect)
        for platform in self.platforms:
            self.screen.blit(platform.image, platform.rect)
        self.screen.blit(self.princess.image, self.princess.rect)

        for coin in self.coins:
            self.screen.blit(coin.image, coin.rect)

        for fireball in self.fireballs:
            self.screen.blit(fireball.image, fireball.rect)

        pygame.display.flip()
        self.clock.tick(30)

if __name__ == "__main__":
    game = Game()
    while True:
        game.run(pygame.event.get())
