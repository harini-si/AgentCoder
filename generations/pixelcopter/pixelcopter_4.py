
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
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")
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
        top_height = random.randint(50, HEIGHT - 50 - CAVERN_WIDTH)
        obstacle = Obstacle(top_height=top_height, bottom_height=top_height + CAVERN_WIDTH)
        self.obstacles.add(obstacle)
        self.all_sprites.add(obstacle)

    def reset_game(self):
        """
        Reset the game to its initial state
        """
        self.game_over = False
        self.player.rect.centery = HEIGHT // 2
        self.obstacles.empty()
        self.all_sprites.empty()
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

        self.screen.fill(BLACK)
        self.all_sprites.update()

        # Check collision with obstacles
        if pygame.sprite.spritecollide(self.player, self.obstacles, False):
            self.game_over = True

        # Check collision with game boundaries
        if self.player.rect.top <= 0 or self.player.rect.bottom >= HEIGHT:
            self.game_over = True

        if self.game_over:
            self.reset_game()

        self.spawn_obstacle()

        self.all_sprites.draw(self.screen)

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
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.velocity = 0

    def update(self):
        """
        Update the Pixelcopter's position
        """
        self.velocity += 0.5  # Gravity
        self.rect.y += self.velocity

    def jump(self):
        """
        Make the Pixelcopter jump
        """
        self.velocity = -10

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top_height, bottom_height):
        """
        Initialize an obstacle
        top_height is the top y-coordinate of the obstacle's gap
        bottom_height is the bottom y-coordinate of the obstacle's gap
        self.image is the Pygame Surface representing the obstacle
        self.rect is the Pygame Rect representing the obstacle's position and size
        """
        super().__init__()
        self.image = pygame.Surface((50, HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (WIDTH, 0)
        self.rect.height = top_height
        self.rect2 = self.image.get_rect()
        self.rect2.topleft = (WIDTH, bottom_height)
        self.rect2.height = HEIGHT - bottom_height

    def update(self):
        """
        Update the obstacle's position
        """
        self.rect.x -= 5
        self.rect2.x -= 5
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
