
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
GRAVITY = 0.6
JUMP_SPEED = -10
PIPE_SPEED = 5


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 255, 0))  # Yellow rectangle representing the bird
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Keep bird within screen bounds
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0

    def jump(self):
        self.velocity = JUMP_SPEED


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, gap_height):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
        self.image.fill((0, 255, 0))  # Green rectangle representing the pipe
        self.rect = self.image.get_rect(topleft=(x, 0))
        self.bottom_pipe = self.image.get_rect(topleft=(x, gap_height + 200))
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED
        self.bottom_pipe.x -= PIPE_SPEED


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(100, 500)
        self.pipes = []
        self.pipe_timer = 0

    def run(self, event):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.bird.jump()

            self.screen.fill((0, 0, 0))

            if not self.pipe_timer:
                pipe_gap = random.randint(200, 400)
                new_pipe = Pipe(SCREEN_WIDTH, pipe_gap)
                self.pipes.append(new_pipe)
                self.pipe_timer = 150

            for pipe in self.pipes:
                pipe.update()
                self.screen.blit(pipe.image, pipe.rect)
                self.screen.blit(pipe.image, pipe.bottom_pipe)

                if pipe.rect.right < 0:
                    self.pipes.remove(pipe)

                if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    pipe.passed = True
                    self.score += 1

            self.pipe_timer -= 1

            self.bird.update()
            self.screen.blit(self.bird.image, self.bird.rect)

            # Collision Detection
            for pipe in self.pipes:
                if self.bird.rect.colliderect(pipe.rect) or self.bird.rect.colliderect(pipe.bottom_pipe):
                    self.game_over = True

            # Display Score
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(30)

        elif self.game_over:
            game_over_text = self.font.render("Game Over!", True, (255, 0, 0))
            self.screen.blit(game_over_text, (400, 500))
            pygame.display.flip()
            self.reset_game()
            pygame.time.wait(2000)

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
