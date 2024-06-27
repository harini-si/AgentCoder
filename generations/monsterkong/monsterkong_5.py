
import pygame
import sys
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.vel_x = 0
        self.vel_y = 0
        self.is_jumping = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.vel_x = -5
        elif keys[pygame.K_d]:
            self.vel_x = 5
        else:
            self.vel_x = 0

        if keys[pygame.K_w] and not self.is_jumping:
            self.is_jumping = True
            self.vel_y = -10

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.is_jumping = False
            self.vel_y = 0


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Princess(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0

    def update(self):
        self.rect.y += 10

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.coins = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()

        for _ in range(10):
            x = random.randint(0, SCREEN_WIDTH - 20)
            y = random.randint(0, SCREEN_HEIGHT - 20)
            coin = Coin(x, y)
            self.coins.add(coin)

        self.total_lives = 15

    def reset_game(self):
        self.game_over = False
        self.score = 0

        self.player = Player()

        self.platforms = [
            Platform(200, SCREEN_HEIGHT - 200),
            Platform(400, SCREEN_HEIGHT - 300),
            Platform(600, SCREEN_HEIGHT - 250),
            Platform(200, SCREEN_HEIGHT - 400),
            Platform(400, SCREEN_HEIGHT - 500)
        ]

        princess_platform = random.choice(self.platforms)
        self.princess = Princess(princess_platform.rect.x, princess_platform.rect.y - 60)

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        self.screen.fill(BLACK)

        if not self.game_over:
            self.player.update()

            for platform in self.platforms:
                pygame.draw.rect(self.screen, GREEN, platform.rect)

            for coin in self.coins:
                if pygame.sprite.collide_rect(self.player, coin):
                    self.score += 5
                    coin.rect.x = -100

                self.screen.blit(coin.image, coin.rect)

            for fireball in self.fireballs:
                fireball.update()
                if fireball.rect.y > SCREEN_HEIGHT:
                    fireball.rect.y = 0
                    fireball.rect.x = random.randint(0, SCREEN_WIDTH - 20)

                if pygame.sprite.collide_rect(self.player, fireball):
                    self.score -= 25
                    self.total_lives -= 1

                    if self.total_lives == 0:
                        self.game_over = True

            pygame.draw.rect(self.screen, YELLOW, self.princess.rect)
            self.screen.blit(self.princess.image, self.princess.rect)

            self.fireballs.draw(self.screen)
            self.fireballs.update()

            self.player.rect.clamp_ip(self.screen.get_rect())
            self.screen.blit(self.player.image, self.player.rect)

            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {self.score}', True, WHITE)
            lives_text = font.render(f'Lives: {self.total_lives}', True, WHITE)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (10, 50))

            pygame.display.flip()
            self.clock.tick(30)

        return True


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True

    while running:
        running = game.run(pygame.event)

    pygame.quit()
