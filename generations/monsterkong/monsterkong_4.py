
import pygame
import sys
import random
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = True

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.vel_x = -5
        elif keys[pygame.K_d]:
            self.vel_x = 5
        else:
            self.vel_x = 0
        
        self.rect.x += self.vel_x

        self.check_collisions(platforms)
        
        if not self.on_ground:
            self.vel_y += 0.3
            self.rect.y += self.vel_y

            if self.rect.y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
                self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
                self.vel_y = 0
                self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vel_y = -8
            self.on_ground = False

    def check_collisions(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                if self.vel_x < 0:
                    self.rect.left = platform.rect.right
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                if self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Princess(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([platform.rect.x for platform in platforms])
        self.rect.y = [platform.rect.y for platform in platforms if platform.rect.x == self.rect.x][0]

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 5

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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
        self.platforms = [Platform(300, 600), Platform(450, 500), Platform(200, 400), Platform(600, 350), Platform(350, 250)]
        self.princess = Princess(self.platforms)
        self.fireballs = []
        self.coins = [Coin(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(10]

    def run(self, event):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return False

        if not self.game_over:
            self.player.update(self.platforms)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player.jump()

            for fireball in self.fireballs:
                fireball.update()
                if fireball.rect.colliderect(self.player.rect):
                    self.lives -= 1
                    self.score -= 25
                    self.fireballs.remove(fireball)
                for platform in self.platforms:
                    if fireball.rect.bottom >= platform.rect.top and fireball.rect.colliderect(platform.rect):
                        self.fireballs.remove(fireball)

            collected_coins = pygame.sprite.spritecollide(self.player, self.coins, True)
            self.score += len(collected_coins) * 5

            if self.player.rect.colliderect(self.princess.rect):
                self.score += 50
                self.princess.rect.x = random.choice([platform.rect.x for platform in self.platforms])
                self.princess.rect.y = [platform.rect.y for platform in self.platforms if platform.rect.x == self.princess.rect.x][0]

            self.screen.fill(WHITE)

            if self.lives <= 0:
                self.game_over = True

            for platform in self.platforms:
                pygame.draw.rect(self.screen, YELLOW, platform.rect)

            pygame.draw.rect(self.screen, BLUE, self.princess.rect)
            pygame.draw.rect(self.screen, RED, self.player.rect)

            for fireball in self.fireballs:
                pygame.draw.rect(self.screen, RED, fireball.rect)

            for coin in self.coins:
                pygame.draw.rect(self.screen, YELLOW, coin.rect)

            font = pygame.font.Font(None, 36)
            text = font.render("Score: " + str(self.score) + " Lives: " + str(self.lives), True, (0, 0, 0))
            self.screen.blit(text, (10, 10))

            pygame.display.flip()
            self.clock.tick(30)

        return True

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
