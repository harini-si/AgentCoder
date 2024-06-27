
import pygame
import sys
import random
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20

class Player(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the player:
            self.rect is the pygame.Rect rectangle representing the player
            self.player_position is a dictionary of the 'x' and 'y' positions of the player
        """
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.player_position = {'x': self.rect.centerx, 'y': self.rect.centery}
        self.velocity = 5
        self.jump_height = 20
        self.jump = False
        self.jump_count = self.jump_height

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.velocity
        if keys[pygame.K_d]:
            self.rect.x += self.velocity
        if keys[pygame.K_w] and not self.jump:
            self.jump = True

        if self.jump:
            if self.jump_count >= -self.jump_height:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.jump = False
                self.jump_count = self.jump_height


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        Initialize the platform
        self.rect is the pygame.Rect rectangle representing the platform
        """
        super().__init__()
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Princess(pygame.sprite.Sprite):
    def __init__(self, platform):
        """
        Initialize the princess
        self.rect is the pygame.Rect rectangle representing the princess
        """
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(platform.rect.left, platform.rect.right), platform.rect.top)

class Fireball(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the fireball
        self.rect is the pygame.Rect rectangle representing the fireball
        """
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, SCREEN_WIDTH), 0)
        self.velocity = random.randint(2, 6)

    def update(self):
        self.rect.y += self.velocity

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        """
        self.rect is the pygame.Rect rectangle representing the coin
        """
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

class Game(pygame.sprite.Sprite):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.reset_game()

    def reset_game(self):
        """
        Initialize / reset the game
        self.game_over is a boolean representing whether the game is over
        self.score keeps track of the player's score
        self.lives keeps track of the player's remaining lives
        self.player is the Player instance
        self.platforms is a list of Platform instances (it should not be empty)
        self.princess is the Princess instance
        """
        self.game_over = False
        self.score = 0
        self.lives = 15
        self.player = Player()
        self.princess = Princess(random.choice(list(self.platforms)))
        self.all_sprites.add(self.player, self.princess)

        platform_y = SCREEN_HEIGHT - 100
        for i in range(5):
            platform = Platform(random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH), platform_y)
            self.all_sprites.add(platform)
            self.platforms.add(platform)

        for _ in range(10):
            self.coins.add(Coin())

    def run(self, event):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False

        self.all_sprites.update()

        if self.lives <= 0:
            self.game_over = True

        if self.player.rect.colliderect(self.princess.rect):
            self.score += 50
            self.princess.rect.center = (random.randint(0, SCREEN_WIDTH), random.choice(list(self.platforms)).rect.top)

        hit_fireballs = pygame.sprite.spritecollide(self.player, self.fireballs, True)
        if hit_fireballs:
            self.score -= 25
            self.lives -= 1

        hit_coins = pygame.sprite.spritecollide(self.player, self.coins, True)
        if hit_coins:
            self.score += 5

        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))

        pygame.display.flip()
        self.clock.tick(30)
        return True

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        running = game.run(pygame.event.poll())
    pygame.quit()

