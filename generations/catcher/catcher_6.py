
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((80, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = SCREEN_HEIGHT - 40

class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = pygame.sprite.Group()
        self.spawn_ball()

    def spawn_ball(self):
        new_ball = Ball(random.randint(0, SCREEN_WIDTH - 20))
        self.balls.add(new_ball)

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.catcher.rect.x -= 10
                elif event.key == pygame.K_RIGHT:
                    self.catcher.rect.x += 10

        self.screen.fill(WHITE)
        self.screen.blit(self.catcher.image, self.catcher.rect)

        self.balls.update()
        self.balls.draw(self.screen)

        collisions = pygame.sprite.spritecollide(self.catcher, self.balls, True)
        if collisions:
            self.score += 1

        for ball in self.balls:
            if ball.rect.y >= SCREEN_HEIGHT:
                self.lives -= 1
                self.balls.remove(ball)

        if self.lives <= 0:
            font = pygame.font.SysFont('Arial', 40)
            text = font.render('Game Over! Click to restart', True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(500)
            self.reset_game()

        font = pygame.font.SysFont('Arial', 20)
        score_text = font.render(f'Score: {self.score}', True, BLACK)
        lives_text = font.render(f'Lives: {self.lives}', True, BLACK)
      
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 30))

        pygame.display.flip()
        self.clock.tick(30)

        return True

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run(pygame.event.poll())
    pygame.quit()
