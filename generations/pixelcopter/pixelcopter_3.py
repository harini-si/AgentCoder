
import pygame
import sys
import random

WIDTH, HEIGHT = 1000, 1000
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern

class Game:
    def __init__(self):
        """
        Initialize the game
        self.screen is the Pygame display surface
        self.clock is the Pygame Clock
        self.game_over is a boolean representing whether the game is over
        self.player is the Pixelcopter instance
        self.obstacles is a Pygame sprite Group containing Obstacle instances
        self.all_sprites is a Pygame sprite Group containing all sprites
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

    def spawn_obstacle(self):
        """
        Spawn obstacles in the game world
        """
        top_height = random.randint(50, HEIGHT-150 - CAVERN_WIDTH)
        bottom_height = HEIGHT - top_height - CAVERN_WIDTH
        obstacle = Obstacle(top_height, top_height + CAVERN_WIDTH)
        self.obstacles.add(obstacle)
        self.all_sprites.add(obstacle)

    def reset_game(self):
        """
        Reset the game to its initial state
        """
        self.game_over = False
        self.player.rect.centery = HEIGHT // 2
        self.player.velocity = 0
        self.obstacles.empty()

    def run(self, event):
        """
        Run the game loop
        event is the current Pygame event
        Returns False if the game should exit, True otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.player.jump()

        self.screen.fill(BLACK)

        self.player.update()
        self.obstacles.update()

        # Check for collisions
        if pygame.sprite.spritecollide(self.player, self.obstacles, False):
            self.game_over = True

        if self.game_over:
            pygame.font.init()
            font = pygame.font.SysFont(None, 100)
            text = font.render('Game Over!', True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(2000)
            self.reset_game()

        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(FPS)
        self.spawn_obstacle()

        return True

class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(100, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += 1
        self.rect.y += self.velocity

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -10

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top, bottom):
        super().__init__()
        self.image = pygame.Surface((50, HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (WIDTH, 0)

    def update(self):
        self.rect.x -= 5

        if self.rect.right < 0:
            self.kill()

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run(pygame.event.poll())
