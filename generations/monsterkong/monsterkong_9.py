
import pygame
import sys
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)
        self.gravity = 1
        self.vel_y = 0
        self.jump_power = -15

    def update(self, platforms):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5

        if keys[pygame.K_w] and self.rect.y >= 0:
            self.vel_y = self.jump_power

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0

        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Princess(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 200, 200))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_y = 5

    def update(self, platforms):
        self.rect.y += self.vel_y
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Game:
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
        self.princess = Princess(random.randint(0, SCREEN_WIDTH - 30), random.randint(100, 300))

        self.platforms = [Platform(0, 400), Platform(200, 350), Platform(400, 300), Platform(600, 250), Platform(800, 200)]

        self.coins = pygame.sprite.Group()
        for _ in range(10):
            coin = Coin(random.randint(0, SCREEN_WIDTH - 20), random.randint(100, 300))
            self.coins.add(coin)

        self.fireballs = pygame.sprite.Group()
        self.fireball_timer = 0

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.fill((0, 0, 0))

        if not self.game_over:
            self.player.update(self.platforms)

            for platform in self.platforms:
                pygame.draw.rect(self.screen, (0, 255, 0), platform.rect)

            for coin in self.coins:
                pygame.draw.ellipse(self.screen, (255, 255, 255), coin.rect)
                if self.player.rect.colliderect(coin.rect):
                    self.score += 5
                    coin.kill()

            for fireball in self.fireballs:
                fireball.update(self.platforms)
                pygame.draw.ellipse(self.screen, (255, 255, 0), fireball.rect)
                if self.player.rect.colliderect(fireball.rect):
                    self.score -= 25
                    self.lives -= 1
                    fireball.kill()

            if pygame.sprite.spritecollide(self.player, [self.princess], False):
                self.score += 50
                self.princess.rect.topleft = (random.randint(0, SCREEN_WIDTH - 30), random.randint(100, 300))

            self.player.rect.clamp_ip(self.screen.get_rect())
            pygame.draw.rect(self.screen, (255, 0, 0), self.player.rect)

            pygame.draw.rect(self.screen, (255, 200, 200), self.princess.rect)

            self.fireball_timer += 1
            if self.fireball_timer == 60:
                self.fireball = Fireball(random.randint(0, SCREEN_WIDTH - 20), 0)
                self.fireballs.add(self.fireball)
                self.fireball_timer = 0

            pygame.display.flip()

            if self.lives == 0:
                self.game_over = True

        return not self.game_over

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run(pygame.event.get())

    pygame.quit()
