
import pygame
import sys
import random
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = [0, 0]

    def update(self, platforms):
        self.rect.x += self.velocity[0]
        self.check_collision(platforms, 0)
        
        self.rect.y += self.velocity[1]
        self.check_collision(platforms, 1)

    def check_collision(self, platforms, direction):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if direction == 0:
                    if self.velocity[0] > 0:
                        self.rect.right = platform.rect.left
                    if self.velocity[0] < 0:
                        self.rect.left = platform.rect.right
                if direction == 1:
                    if self.velocity[1] > 0:
                        self.rect.bottom = platform.rect.top
                        self.velocity[1] = 0
                    if self.velocity[1] < 0:
                        self.rect.top = platform.rect.bottom
                        self.velocity[1] = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft=(x, y))

class Princess(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(topleft=(x, y))

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = [0, 5]

    def update(self):
        self.rect.y += self.velocity[1]

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.lives = 15
        self.player = Player(100, 100)
        self.princess = Princess(700, 100)
        self.platforms = [Platform(0, 900), Platform(200, 800),
                          Platform(400, 700), Platform(600, 600),
                          Platform(800, 500)]
        self.fireballs = []
        for _ in range(10):
            x = random.randint(0, SCREEN_WIDTH - 20)
            y = random.randint(-SCREEN_HEIGHT, 0)
            self.fireballs.append(Fireball(x, y))
        self.coins = []
        for _ in range(10):
            x = random.randint(0, SCREEN_WIDTH - 15)
            y = random.randint(0, SCREEN_HEIGHT - 15)
            self.coins.append(Coin(x, y))

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.velocity[0] = -5
        elif keys[pygame.K_d]:
            self.player.velocity[0] = 5
        else:
            self.player.velocity[0] = 0

        if keys[pygame.K_w] and self.player.velocity[1] == 0:
            self.player.velocity[1] = -10

        self.player.update(self.platforms)

        for fireball in self.fireballs:
            fireball.update()

        self.screen.fill((0, 0, 0))

        for platform in self.platforms:
            pygame.draw.rect(self.screen, WHITE, platform.rect)

        for coin in self.coins:
            pygame.draw.rect(self.screen, RED, coin.rect)

        pygame.draw.rect(self.screen, YELLOW, self.princess.rect)
        pygame.draw.rect(self.screen, RED, self.player.rect)

        for fireball in self.fireballs:
            pygame.draw.rect(self.screen, RED, fireball.rect)

        pygame.display.flip()
        self.clock.tick(30)

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        game.run(pygame.event)
