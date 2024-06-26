
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

        self.score = 0
        self.font = pygame.font.Font(None, 36)

        self.obstacle_timer = 0

    def spawn_obstacle(self):
        """
        Spawn obstacles in the game world
        """
        top = random.randint(0, HEIGHT - CAVERN_WIDTH)
        bottom = top + CAVERN_WIDTH
        obstacle = Obstacle(top, bottom)
        self.obstacles.add(obstacle)
        self.all_sprites.add(obstacle)

    def reset_game(self):
        """
        Reset the game to its initial state
        """
        self.score = 0
        self.game_over = False
        self.player.rect.centery = HEIGHT // 2
        self.obstacles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.obstacle_timer = 0

    def run(self, event):
        """
        Run the game loop
        event is the current Pygame event
        Returns False if the game should exit, True otherwise
        """
        if self.game_over:
            self.screen.fill(WHITE)
            self.draw_text("Game Over!", self.screen.get_rect().center, (255, 0, 0))
            self.draw_text("Press R to restart", (WIDTH // 2, HEIGHT // 2 + 50), (0, 0, 255))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()

            return True

        self.screen.fill(BLACK)

        for obstacle in self.obstacles:
            obstacle.update()
            if obstacle.rect.right < 0:
                self.obstacles.remove(obstacle)
                self.all_sprites.remove(obstacle)
                self.score += 1

        if not self.obstacles:
            self.spawn_obstacle()

        self.player.update(event)
        
        self.draw_text(f"Score: {self.score}", (10, 10))
        
        self.clock.tick(FPS)
        pygame.display.flip()
        
        return True

    def draw_text(self, text, pos, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = pos
        self.screen.blit(text_surface, text_rect)

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

    def update(self, event):
        """
        Update the Pixelcopter's position
        """
        self.velocity += 0.5  # Gravity
        self.rect.y += self.velocity

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or event.type == pygame.MOUSEBUTTONDOWN:
            self.velocity = -10

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            game.game_over = True

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top, bottom):
        """
        Initialize an obstacle
        top is the top y-coordinate of the obstacle's gap (if applicable)
        bottom is the bottom y-coordinate of the obstacle's gap (if applicable)
        """
        super().__init__()
        self.image = pygame.Surface((50, HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (WIDTH, 0)
        self.top = top
        self.bottom = bottom

    def update(self):
        """
        Update the obstacle's position
        """
        self.rect.x -= 5

if __name__ == "__main__":
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        running = game.run(event)

    pygame.quit()
