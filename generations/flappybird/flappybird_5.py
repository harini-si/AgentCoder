
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_SPEED = 5
GRAVITY = 0.5
JUMP_HEIGHT = 10
GAP_SIZE = 200
SCORE_FONT = pygame.font.SysFont('Arial', 36)
GAME_OVER_FONT = pygame.font.SysFont('Arial', 72)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 30, 30)
        self.vel_y = 0

    def update(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

    def jump(self):
        self.vel_y = -JUMP_HEIGHT

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, gap_top):
        super().__init__()
        self.rect = pygame.Rect(x, 0, PIPE_WIDTH, gap_top)
        self.rect_bottom = pygame.Rect(x, gap_top + GAP_SIZE, PIPE_WIDTH, SCREEN_HEIGHT - gap_top - GAP_SIZE)
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED
        self.rect_bottom.x -= PIPE_SPEED


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()
        
    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(50, SCREEN_HEIGHT // 2)
        self.pipes = []
        self.spawn_pipe()

    def spawn_pipe(self):
        gap_top = random.randint(150, SCREEN_HEIGHT - GAP_SIZE - 150)
        self.pipes.append(Pipe(SCREEN_WIDTH, gap_top))

    def check_collision(self):
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.rect) or self.bird.rect.colliderect(pipe.rect_bottom) or self.bird.rect.y < 0 or self.bird.rect.y + self.bird.rect.height > SCREEN_HEIGHT:
                self.game_over = True

    def display_score(self):
        score_text = SCORE_FONT.render("Score: " + str(self.score), True, WHITE)
        self.screen.blit(score_text, (20, 20))

    def display_game_over(self):
        game_over_text = GAME_OVER_FONT.render("Game Over!", True, WHITE)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.bird.jump()

            if not self.game_over:
                self.screen.fill(BLACK)

                self.bird.update()
                for pipe in self.pipes:
                    pipe.update()

                    if pipe.rect.x + PIPE_WIDTH < self.bird.rect.x and not pipe.passed:
                        pipe.passed = True
                        self.score += 1

                    if pipe.rect.x < -PIPE_WIDTH:
                        self.pipes.remove(pipe)

                    if pipe.rect.x < self.bird.rect.x < pipe.rect.x + PIPE_WIDTH:
                        if not pipe.passed:
                            self.check_collision()

                    pygame.draw.rect(self.screen, WHITE, pipe.rect)
                    pygame.draw.rect(self.screen, WHITE, pipe.rect_bottom)

                if len(self.pipes) < 2:
                    self.spawn_pipe()

                self.display_score()
                pygame.draw.rect(self.screen, WHITE, self.bird.rect)

                if self.game_over:
                    self.display_game_over()
                    pygame.display.update()
                    return

                pygame.display.update()
                self.clock.tick(30)

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
