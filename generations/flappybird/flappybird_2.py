
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
GRAVITY = 0.6
JUMP_STRENGTH = -10
PIPE_SPEED = 3
PIPE_SPAWN_INTERVAL = 120

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill((255, 255, 0))  # Yellow rectangle representing the bird
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = 0
    
    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = JUMP_STRENGTH

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, gap_height):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
        self.image.fill((0, 255, 0))  # Green rectangle representing the pipe
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, gap_height - SCREEN_HEIGHT)  # Top of the upper pipe
        self.scored = False

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
        self.bird = Bird(200, SCREEN_HEIGHT // 2)
        self.pipes = []

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                self.bird.jump()

        if not self.game_over:
            self.screen.fill((0, 0, 0))

            # Update bird
            self.bird.update()

            # Check collisions
            if self.bird.rect.top > SCREEN_HEIGHT or pygame.sprite.spritecollideany(self.bird, self.pipes):
                self.game_over = True

            # Spawn pipes
            if self.clock.get_count() % PIPE_SPAWN_INTERVAL == 0:
                gap_height = random.randint(150, SCREEN_HEIGHT - 150)
                self.pipes.append(Pipe(SCREEN_WIDTH, gap_height))

            # Update pipes
            for pipe in self.pipes:
                pipe.update()
                self.screen.blit(pipe.image, pipe.rect)

                if pipe.rect.right < 0:
                    self.pipes.remove(pipe)

                if not pipe.scored and pipe.rect.right < self.bird.rect.left:
                    pipe.scored = True
                    self.score += 1

            # Display bird
            self.screen.blit(self.bird.image, self.bird.rect)

            # Display score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)

        else:
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Game Over!", True, (255, 255, 255))
            self.screen.blit(game_over_text, (250, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            self.clock.tick(1)  # Lower frame rate since the game is over

        return True


if __name__ == "__main__":
    pygame.init()
    game = Game()

    running = True
    while running:
        running = game.run(pygame.event.poll())

    pygame.quit()
