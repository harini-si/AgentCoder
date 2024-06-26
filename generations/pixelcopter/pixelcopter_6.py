
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
        bottom_height = HEIGHT - top_height - CAVERN_WIDTH
        obstacle = Obstacle(top_height, bottom_height)
        self.obstacles.add(obstacle)
        self.all_sprites.add(obstacle)

    def reset_game(self):
        """
        Reset the game to its initial state
        """
        self.game_over = False
        self.player.rect.centery = HEIGHT // 2
        for obstacle in self.obstacles:
            obstacle.kill()
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
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                self.player.jump()

        self.screen.fill(BLACK)

        self.all_sprites.update()

        if not self.game_over:
            self.spawn_obstacle()

            collisions = pygame.sprite.spritecollide(self.player, self.obstacles, False)
            if collisions or self.player.rect.top <= 0 or self.player.rect.bottom >= HEIGHT:
                self.game_over = True

        if self.game_over:
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over!", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, text_rect)

            self.reset_game()

        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f"Score: {self.player.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

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
        self.rect = self.image.get_rect(center=(100, HEIGHT // 2))
        self.velocity = 0
        self.score = 0

    def update(self):
        """
        Update the Pixelcopter's position
        """
        self.velocity += 1.5
        self.rect.y += self.velocity
        self.score += 1

    def jump(self):
        """
        Make the Pixelcopter jump
        """
        self.velocity = -15

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top, bottom):
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
        self.rect = self.image.get_rect()

        top_rect = pygame.Rect(0, 0, 50, top)
        bottom_rect = pygame.Rect(0, top + CAVERN_WIDTH, 50, bottom)

        pygame.draw.rect(self.image, BLACK, top_rect)
        pygame.draw.rect(self.image, BLACK, bottom_rect)

        self.rect.topleft = (WIDTH, 0)
        self.velocity = -5

    def update(self):
        """
        Update the obstacle's position
        """
        self.rect.x += self.velocity
        if self.rect.right < 0:
            self.kill()

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run(None)
