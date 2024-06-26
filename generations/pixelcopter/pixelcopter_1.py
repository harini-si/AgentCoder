
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
        top_height = random.randint(50, HEIGHT // 2)
        obstacle = Obstacle(top=top_height)
        self.obstacles.add(obstacle)
        self.all_sprites.add(obstacle)

    def reset_game(self):
        """
        Reset the game to its initial state
        """
        self.game_over = False
        self.obstacles.empty()
        self.player.rect.center = (100, HEIGHT // 2)

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

        self.player.update()
        self.obstacles.update()

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        if pygame.sprite.spritecollide(self.player, self.obstacles, False):
            self.game_over = True

        if self.game_over:
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over!", 1, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, text_rect)
            pygame.display.flip()

            pygame.time.wait(2000)  # Delay before starting new game
            self.reset_game()

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
        self.rect = self.image.get_rect(center=(100, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        """
        Update the Pixelcopter's position
        """
        self.velocity += 0.5  # Gravity
        self.rect.y += self.velocity

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.jump()

        if pygame.mouse.get_pressed()[0]:
            self.jump()

        if self.rect.bottom > HEIGHT or self.rect.top < 0:
            game.game_over = True

    def jump(self):
        """
        Make the Pixelcopter jump
        """
        self.velocity = -10


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None):
        """
        Initialize an obstacle
        top is the top y-coordinate of the obstacle's gap (if applicable)
        bottom is the bottom y-coordinate of the obstacle's gap (if applicable)
        self.image is the Pygame Surface representing the obstacle
        self.rect is the Pygame Rect representing the obstacle's position and size
        """
        super().__init__()
        self.image = pygame.Surface((50, HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH + 25, top))
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
    running = True
    while running:
        for event in pygame.event.get():
            running = game.run(event)
