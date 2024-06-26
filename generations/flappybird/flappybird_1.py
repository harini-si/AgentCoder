
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
GRAVITY = 0.8
JUMP_AMOUNT = -15
PIPE_SPEED = 5
PIPE_SPAWN_FREQ = 120
GAP_HEIGHT = 200

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = JUMP_AMOUNT

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, height):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, 0)
        self.passed = False
        self.height = height

    def update(self):
        self.rect.x -= PIPE_SPEED

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(100, SCREEN_HEIGHT // 2)
        self.pipes = []

    def run(self, event):
        if self.game_over:
            game_over_text = pygame.font.SysFont(None, 70).render('Game Over!', True, BLACK)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, game_over_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        if not self.game_over:
            self.screen.fill(BLACK)

            for pipe in self.pipes:
                pipe.update()
                if pipe.rect.right < 0:
                    self.pipes.remove(pipe)
                    self.score += 1

                if pipe.rect.colliderect(self.bird.rect) or self.bird.rect.top <= 0 or self.bird.rect.bottom >= SCREEN_HEIGHT:
                    self.game_over = True

                if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    pipe.passed = True

            if len(self.pipes) == 0 or self.pipes[-1].rect.x < SCREEN_WIDTH - PIPE_SPAWN_FREQ:
                pipe_height = random.randint(100, SCREEN_HEIGHT - GAP_HEIGHT)
                self.pipes.append(Pipe(SCREEN_WIDTH, pipe_height))
                self.pipes.append(Pipe(SCREEN_WIDTH, SCREEN_HEIGHT - pipe_height - GAP_HEIGHT))

            self.bird.update()
            self.screen.blit(self.bird.image, self.bird.rect)

            for pipe in self.pipes:
                self.screen.blit(pipe.image, pipe.rect)

            score_text = pygame.font.SysFont(None, 40).render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.bird.jump()

        return not self.game_over

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
