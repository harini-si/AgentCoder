
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
        top_height = random.randint(50, HEIGHT - 50 - CAVERN_WIDTH)
        obstacle = Obstacle(top_height)
        self.obstacles.add(obstacle)
        self.all_sprites.add(obstacle)

    def reset_game(self):
        """
        Reset the game to its initial state
        """
        self.obstacles.empty()
        self.all_sprites.empty()
        self.player = Pixelcopter()
        self.all_sprites.add(self.player)
        self.game_over = False

    def run(self, event):
        """
        Run the game loop
        event is the current Pygame event
        Returns False if the game should exit, True otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if not self.game_over:
            self.all_sprites.update()

            if random.randint(0, 100) < 2:
                self.spawn_obstacle()

            hits = pygame.sprite.spritecollide(self.player, self.obstacles, False)
            if hits or self.player.rect.top < 0 or self.player.rect.bottom > HEIGHT:
                self.game_over = True

            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)

            font = pygame.font.Font(None, 36)
            text = font.render(f"Score: {self.player.score}", True, WHITE)
            self.screen.blit(text, (10, 10))

        else:
            self.screen.fill(BLACK)
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over!", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, text_rect)
            font2 = pygame.font.Font(None, 36)
            text2 = font2.render("Press Space to restart", True, WHITE)
            text_rect2 = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            self.screen.blit(text2, text_rect2)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.reset_game()

        pygame.display.flip()
        self.clock.tick(FPS)
        return True

class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0
        self.score = 0

    def update(self):
        self.velocity += 0.5
        self.rect.y += self.velocity
        self.score += 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
            self.jump()

    def jump(self):
        self.velocity = -10

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top_height):
        super().__init__()
        self.image = pygame.Surface((50, HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft=(WIDTH, 0))
        self.rect.top = top_height
        self.velocity = 5

    def update(self):
        self.rect.x -= self.velocity
        if self.rect.right < 0:
            self.kill()

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
