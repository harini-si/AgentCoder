
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
GRAVITY = 0.5
JUMP_HEIGHT = -10
GAP_SIZE = 200
PIPE_SPEED = 5


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 50, 50)
        self.vel_y = 0

    def update(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

    def jump(self):
        self.vel_y = JUMP_HEIGHT


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, gap_y):
        super().__init__()
        self.x = x
        self.gap_y = gap_y
        self.top_pipe = pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_y)
        self.bottom_pipe = pygame.Rect(self.x, self.gap_y + GAP_SIZE, PIPE_WIDTH, SCREEN_HEIGHT - (self.gap_y + GAP_SIZE))

    def update(self):
        self.x -= PIPE_SPEED
        self.top_pipe.x = self.x
        self.bottom_pipe.x = self.x


class Game(pygame.sprite.Sprite):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(100, SCREEN_HEIGHT // 2)
        self.pipes = []
        self.spawn_pipe()

    def spawn_pipe(self):
        gap_y = random.randint(100, SCREEN_HEIGHT - GAP_SIZE - 100)
        new_pipe = Pipe(SCREEN_WIDTH, gap_y)
        self.pipes.append(new_pipe)

    def check_collision(self):
        for pipe in self.pipes:
            if pipe.top_pipe.colliderect(self.bird.rect) or pipe.bottom_pipe.colliderect(self.bird.rect):
                self.game_over = True

    def run(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not self.game_over:
            self.screen.fill((0, 0, 0))

            self.bird.update()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.bird.jump()

            for pipe in self.pipes:
                pipe.update()
                pygame.draw.rect(self.screen, (0, 255, 0), pipe.top_pipe)
                pygame.draw.rect(self.screen, (0, 255, 0), pipe.bottom_pipe)
                if pipe.x + PIPE_WIDTH < 0:
                    self.pipes.remove(pipe)
                    self.score += 1
                    self.spawn_pipe()

            pygame.draw.rect(self.screen, (255, 0, 0), self.bird.rect)
            pygame.font.init()
            font = pygame.font.SysFont("Arial", 30)
            text = font.render("Score: " + str(self.score), True, (255, 255, 255))
            self.screen.blit(text, (10, 10))

            if self.bird.rect.y > SCREEN_HEIGHT or self.bird.rect.y < 0:
                self.game_over = True

            self.check_collision()

            if self.game_over:
                font = pygame.font.SysFont("Arial", 50)
                text = font.render("Game Over!", True, (255, 255, 255))
                self.screen.blit(text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))

            pygame.display.flip()
            self.clock.tick(30)

        return True


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            running = game.run(event)
    pygame.quit()
