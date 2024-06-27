
import pygame
import sys
import random
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
GROUND_HEIGHT = 50
PLATFORM_HEIGHT = 50
PLATFORM_WIDTH = 200

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))  # Red color for player
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.rect.height
        self.player_position = {'x': self.rect.x, 'y': self.rect.y}
        self.velocity = 7
        self.is_jumping = False
        self.jump_count = 10
        self.gravity = 1
        self.lives = 15
        self.score = 0

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.rect.x -= self.velocity
        if keys[pygame.K_d]:
            self.rect.x += self.velocity
        if keys[pygame.K_w] and not self.is_jumping:
            self.is_jumping = True

        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10

        if self.rect.y < SCREEN_HEIGHT - GROUND_HEIGHT - self.rect.height:
            on_platform = False
            for platform in platforms:
                if platform.rect.colliderect(self.rect):
                    on_platform = True
                    self.rect.y = platform.rect.y - self.rect.height
            if not on_platform:
                self.rect.y += self.gravity
        else:
            self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.rect.height

        self.player_position['x'] = self.rect.x
        self.player_position['y'] = self.rect.y

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill((0, 255, 0))  # Green color for platform
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Princess(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 0))  # Yellow color for princess
        self.rect = self.image.get_rect()
        self.set_position(platforms)

    def set_position(self, platforms):
        platform = random.choice(platforms)
        self.rect.x = platform.rect.x + random.randint(0, PLATFORM_WIDTH - self.rect.width)
        self.rect.y = platform.rect.y - self.rect.height

class Fireball(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 255))  # Purple color for fireball
        self.rect = self.image.get_rect()
        self.set_position(platforms)

    def set_position(self, platforms):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = 0
        while True:
            intersect = False
            for platform in platforms:
                if platform.rect.colliderect(self.rect):
                    intersect = True
            if intersect:
                self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            else:
                break

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 165, 0))  # Orange color for coin
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - GROUND_HEIGHT - self.rect.height)

class Game(pygame.sprite.Sprite):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.player = Player()
        self.princess = Princess(self.platforms)
        self.coins = pygame.sprite.Group([Coin() for _ in range(10)])
        self.fireballs = pygame.sprite.Group()
        self.platforms = [Platform(100, 400), Platform(400, 300), Platform(700, 200), Platform(200, 600), Platform(600, 500)]

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.player.update(self.platforms)
        princess_collected = pygame.sprite.spritecollide(self.player, [self.princess], True)
        if princess_collected:
            self.score += 50
            self.princess.set_position(self.platforms)

        coin_collected = pygame.sprite.spritecollide(self.player, self.coins, True)
        self.score += len(coin_collected) * 5

        if len(self.fireballs) < 5:
            self.fireballs.add(Fireball(self.platforms))

        for fireball in self.fireballs:
            if fireball.rect.colliderect(self.player.rect):
                self.score -= 25
                self.player.lives -= 1
                self.fireballs.remove(fireball)
                if self.player.lives == 0:
                    self.game_over = True

        self.screen.fill((0, 0, 0))  # Black background

        for platform in self.platforms:
            pygame.draw.rect(self.screen, (0, 255, 0), platform.rect)

        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.princess.image, self.princess.rect)
        self.coins.draw(self.screen)
        self.fireballs.draw(self.screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        lives_text = font.render("Lives: " + str(self.player.lives), True, (255, 255, 255))
        self.screen.blit(lives_text, (10, 50))

        pygame.display.flip()
        self.clock.tick(30)

        return not self.game_over

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
