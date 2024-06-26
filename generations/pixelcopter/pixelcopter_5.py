
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
        top_height = random.randint(50, HEIGHT - CAVERN_WIDTH - 50)
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
        self.obstacles.empty()

    def run(self, event):
        """
        Run the game loop
        event is the current Pygame event
        Returns False if the game should exit, True otherwise
        """
        self.screen.fill(BLACK)

        for obstacle in self.obstacles:
            obstacle.update()
            if pygame.sprite.collide_rect(self.player, obstacle):
                self.game_over = True

        self.all_sprites.update()

        if self.player.rect.top <= 0 or self.player.rect.bottom >= HEIGHT:
            self.game_over = True

        if self.game_over:
            font = pygame.font.Font(None, 64)
            text = font.render('Game Over!', True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, text_rect)

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] or event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()

        if random.randint(0, 100) < 2:
            self.spawn_obstacle()

        self.all_sprites.draw(self.screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render('Score: {}'.format(pygame.time.get_ticks() // 10), True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        return True


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the Pixelcopter
        self.image is the Pygame Surface representing the Pixelcopter
        self.rect is the Pygame Rect representing the Pixelcopter's position and size
        self.velocity is the Pixelcopter's vertical velocity
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.velocity = 0

    def update(self):
        """
        Update the Pixelcopter's position
        """
        self.rect.y += self.velocity
        self.velocity += 0.5  # Gravity

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.velocity = -10

    def jump(self):
        """
        Make the Pixelcopter jump
        """
        self.velocity = -10


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        """
        Initialize an obstacle
        top is the top y-coordinate of the obstacle's gap (if applicable)
        bottom is the bottom y-coordinate of the obstacle's gap (if applicable)
        self.image is the Pygame Surface representing the obstacle
        self.rect is the Pygame Rect representing the obstacle's position and size
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = WIDTH
        if top is not None:
            self.rect.bottom = top
        elif bottom is not None:
            self.rect.top = bottom

    def update(self):
        """
        Update the obstacle's position
        """
        self.rect.x -= 5


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

