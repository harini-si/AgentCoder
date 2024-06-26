
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
        pygame.display.set_caption("PixelCopter Game")
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
        bottom_height = top_height + CAVERN_WIDTH
        new_obstacle = Obstacle(top=top_height, bottom=bottom_height)
        self.obstacles.add(new_obstacle)
        self.all_sprites.add(new_obstacle)

    def reset_game(self):
        """
        Reset the game to its initial state
        """
        self.game_over = False
        self.player.rect.center = (100, HEIGHT // 2)
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
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                self.player.jump()

        self.screen.fill(BLACK)

        if not self.game_over:
            self.player.update()
            self.spawn_obstacle()

            self.player_hit_obstacle = pygame.sprite.spritecollide(self.player, self.obstacles, False)

            if self.player.rect.top <= 0 or self.player.rect.bottom >= HEIGHT or self.player_hit_obstacle:
                self.game_over = True

            self.all_sprites.update()
            self.all_sprites.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)
            return True
        else:
            font = pygame.font.SysFont(None, 48)
            text = font.render('Game Over!', True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, text_rect)

            pygame.display.flip()
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.reset_game()

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
        self.image = pygame.Surface((50, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.velocity = 0

    def update(self):
        """
        Update the Pixelcopter's position
        """
        self.velocity += 1
        self.rect.y += self.velocity

    def jump(self):
        """
        Make the Pixelcopter jump
        """
        self.velocity = -12

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
        self.rect.top = 0
        if top is not None:
            self.rect.bottom = top
        elif bottom is not None:
            self.rect.top = bottom

    def update(self):
        """
        Update the obstacle's position
        """
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run(event)
