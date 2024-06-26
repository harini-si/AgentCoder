
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
GRAVITY = 0.6
JUMP_FORCE = -10
PIPE_SPEED = 5
PIPE_SPAWN_INTERVAL = 120
GAP_HEIGHT = 200

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 0))  # Yellow color
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = JUMP_FORCE

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, height):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))  # Green color
        self.rect = self.image.get_rect(topleft=(x, 0))
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED

class Game(pygame.sprite.Sprite):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.score = 0
        self.font = pygame.font.SysFont(None, 48)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(100, SCREEN_HEIGHT // 2)
        self.pipes = []

    def run(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:  # Space key to jump
                self.bird.jump()

            if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse click to jump
                self.bird.jump()

            self.screen.fill((0, 0, 0))  # Black background

            self.bird.update()
            self.screen.blit(self.bird.image, self.bird.rect)

            if random.randint(1, PIPE_SPAWN_INTERVAL) == 1:
                pipe_height = random.randint(100, SCREEN_HEIGHT - 100 - GAP_HEIGHT)
                self.pipes.append(Pipe(SCREEN_WIDTH, pipe_height))

            for pipe in self.pipes[:]:
                pipe.update()
                self.screen.blit(pipe.image, pipe.rect)

                if pipe.rect.colliderect(self.bird.rect):
                    self.game_over = True

                if pipe.rect.right < 0 and not pipe.passed:
                    pipe.passed = True
                    self.score += 1

                if pipe.rect.right < 0:
                    self.pipes.remove(pipe)

            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))  # White color
            self.screen.blit(score_text, (10, 10))

            if self.bird.rect.top < 0 or self.bird.rect.bottom > SCREEN_HEIGHT:
                self.game_over = True

            pygame.display.flip()
            self.clock.tick(30)

            if self.game_over:
                game_over_text = self.font.render("Game Over!", True, (255, 0, 0))  # Red color
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 - 24))
                pygame.display.flip()
                pygame.time.wait(2000)
                self.reset_game()

        return True

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            running = game.run(event)
    pygame.quit()
