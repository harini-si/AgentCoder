
import pygame
import sys
import random

WIDTH, HEIGHT = 1000, 1000
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
GRAVITY = 1


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
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pygame Helicopter Game")
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
        obstacle = Obstacle()
        self.obstacles.add(obstacle)
        self.all_sprites.add(obstacle)

    def reset_game(self):
        """
        Reset the game to its initial state
        """
        for sprite in self.all_sprites:
            sprite.kill()
        self.game_over = False
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites.add(self.player)

    def run(self, event):
        """
        Run the game loop
        event is the current Pygame event
        Returns False if the game should exit, True otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and not self.game_over:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

        if not self.game_over:
            self.player.update()
            self.obstacles.update()

            if len(self.obstacles) == 0:
                self.spawn_obstacle()

            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)

            if pygame.sprite.spritecollide(self.player, self.obstacles, False):
                self.game_over = True
                font = pygame.font.SysFont(None, 70)
                text = font.render("Game Over!", True, WHITE)
                self.screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2))

        pygame.display.flip()
        self.clock.tick(FPS)
        return True


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the Pixelcopter
        self.image is the Pygame Surface representing the Pixelcopter
        self.rect is the Pygame Rect representing the Pixelcopter's position and size
        self.velocity is the Pixelcopter's vertical velocity
        """
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.velocity = 0

    def update(self):
        """
        Update the Pixelcopter's position
        """
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        """
        Make the Pixelcopter jump
        """
        self.velocity = -15


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize an obstacle
        top is the top y-coordinate of the obstacle's gap (if applicable)
        bottom is the bottom y-coordinate of the obstacle's gap (if applicable)
        self.image is the Pygame Surface representing the obstacle
        self.rect is the Pygame Rect representing the obstacle's position and size
        """
        super().__init__()
        self.image = pygame.Surface((CAVERN_WIDTH, HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = WIDTH
        self.rect.top = 0
        self.velocity = 5

    def update(self):
        """
        Update the obstacle's position
        """
        self.rect.x -= self.velocity
        if self.rect.right < 0:
            self.kill()


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

