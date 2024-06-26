
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
BIRD_COLOR = (255, 0, 0)
PIPE_COLOR = (0, 255, 0)
FONT_COLOR = (255, 255, 255)
FONT_SIZE = 36
GRAVITY = 0.6
JUMP_SPEED = -14
PIPE_SPEED = 5
GAP_SIZE = 200
PIPE_SPAWN_TIME = 120

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill(BIRD_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = JUMP_SPEED

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, height):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill(PIPE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, 0)
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.score = 0
        self.font = pygame.font.Font(None, FONT_SIZE)

    def reset_game(self):
        self.game_over = False
        self.bird = Bird(100, SCREEN_HEIGHT // 2)
        self.pipes = []

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if not self.game_over:
                        self.bird.jump()

        if not self.game_over:
            self.screen.fill((0, 0, 0))
            self.bird.update()
            self.screen.blit(self.bird.image, self.bird.rect)

            if random.randint(1, PIPE_SPAWN_TIME) == 1:
                pipe_height = random.randint(100, SCREEN_HEIGHT - GAP_SIZE - 100)
                new_pipe = Pipe(SCREEN_WIDTH, pipe_height)
                self.pipes.append(new_pipe)
            
            for pipe in self.pipes:
                pipe.update()
                self.screen.blit(pipe.image, pipe.rect)

                if pipe.rect.right < 0:
                    self.pipes.remove(pipe)
                    self.score += 1

                if pipe.rect.colliderect(self.bird.rect):
                    self.game_over = True

            if self.bird.rect.top < 0 or self.bird.rect.bottom > SCREEN_HEIGHT:
                self.game_over = True

            score_text = self.font.render(f"Score: {self.score}", True, FONT_COLOR)
            self.screen.blit(score_text, (10, 10))

            if self.game_over:
                game_over_text = self.font.render("Game Over!", True, FONT_COLOR)
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        self.clock.tick(30)

        return True

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        running = game.run(pygame.event.poll())
    pygame.quit()
