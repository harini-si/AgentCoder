
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
PIPE_WIDTH = 80
GRAVITY = 0.6

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        self.rect is the pygame.Rect rectangle representing the bird
        x and y are the initial x and y positions of the bird
        """
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill((255, 255, 0))  # Yellow
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = -10

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, gap_height):
        """
        x is the initial x position of this instance on screen
        rect is the pygame.Rect instance representing the pipe
        passed is a boolean representing whether the bird has passed this pipe
        """
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
        self.image.fill((0, 255, 0))  # Green
        self.rect = self.image.get_rect(topleft=(x, 0))
        
        self.top_pipe = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT // 2 - gap_height // 2))
        self.top_pipe.fill((0, 255, 0))  # Green
        
        self.bottom_pipe = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT // 2 - gap_height // 2))
        self.bottom_pipe.fill((0, 255, 0))  # Green
        

    def update(self, speed):
        self.rect.x -= speed
        
    def collides_with(self, bird):
        return self.rect.colliderect(bird.rect) or self.top_pipe.get_rect(topleft=(self.rect.x, 0)).colliderect(bird.rect) or self.bottom_pipe.get_rect(topleft=(self.rect.x, SCREEN_HEIGHT // 2 + self.rect.height // 2)).colliderect(bird.rect)


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
        self.pipe_frequency = 60  # Add pipes every 60 frames
        self.pipe_counter = 0
        self.speed = 5

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.bird.jump()

        if not self.game_over:
            self.screen.fill((0, 0, 0))  # Black background

            self.bird.update()
            self.screen.blit(self.bird.image, self.bird.rect)

            if self.pipe_counter % self.pipe_frequency == 0:
                gap_height = random.randint(100, 300)
                new_pipe = Pipe(SCREEN_WIDTH, gap_height)
                self.pipes.append(new_pipe)

            for pipe in self.pipes:
                pipe.update(self.speed)
                self.screen.blit(pipe.image, pipe.rect)
                self.screen.blit(pipe.top_pipe, (pipe.rect.x, 0))
                self.screen.blit(pipe.bottom_pipe, (pipe.rect.x, SCREEN_HEIGHT // 2 + pipe.rect.height // 2))

                if pipe.collides_with(self.bird):
                    self.game_over = True

                if pipe.rect.right < 0:
                    self.pipes.remove(pipe)
                    self.score += 1

            font = pygame.font.Font(None, 36)
            text = font.render(f'Score: {self.score}', True, (255, 255, 255))  # White text
            self.screen.blit(text, (10, 10))

            if self.bird.rect.top < 0 or self.bird.rect.bottom > SCREEN_HEIGHT:
                self.game_over = True

            pygame.display.flip()
            self.clock.tick(30)
            
            self.pipe_counter += 1

        return True

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        running = game.run(pygame.event)
    pygame.quit()

