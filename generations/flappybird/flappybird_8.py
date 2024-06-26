
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
GRAVITY = 0.6
JUMP_HEIGHT = -10

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 0))  # Yellow rectangle representing the bird
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_y = 0

    def update(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

    def jump(self):
        self.vel_y = JUMP_HEIGHT

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, gap_height):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
        self.image.fill((0, 255, 0))  # Green rectangle representing the pipe
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, 0)
        self.gap_height = gap_height

    def update(self):
        self.rect.x -= 5

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.jump()

        if not self.game_over:
            self.screen.fill((0, 0, 0))
            self.bird.update()
            self.screen.blit(self.bird.image, self.bird.rect)

            for pipe in self.pipes:
                pipe.update()
                self.screen.blit(pipe.image, pipe.rect)
                if pipe.rect.colliderect(self.bird.rect):
                    self.game_over = True

                if pipe.rect.right < 0:
                    self.pipes.remove(pipe)
                    self.score += 1

            self.spawn_pipes()
            pygame.display.update()
            self.clock.tick(30)

        return True

    def spawn_pipes(self):
        if len(self.pipes) == 0 or self.pipes[-1].rect.right < SCREEN_WIDTH - 300:
            gap_height = random.randint(150, 300)
            new_pipe = Pipe(SCREEN_WIDTH, gap_height)
            self.pipes.append(new_pipe)

if __name__ == "__main__":
    pygame.init()
    game = Game()
    
    while True:
        game.run(pygame.event.poll())

pygame.quit()

