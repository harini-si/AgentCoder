
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
GRAVITY = 0.5
JUMP_VELOCITY = -10

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 50, 50)
        self.vel_y = 0

    def update(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, gap_y):
        super().__init__()
        self.x = x
        self.gap_y = gap_y
        self.rect_top = pygame.Rect(x, 0, PIPE_WIDTH, gap_y)
        self.rect_bottom = pygame.Rect(x, gap_y + 200, PIPE_WIDTH, SCREEN_HEIGHT - gap_y - 200)

    def update(self):
        self.x -= 5
        self.rect_top.x = self.x
        self.rect_bottom.x = self.x

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(200, 500)
        self.pipes = []

    def run(self, event):
        if self.game_over:
            self.display_game_over()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        else:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN or (e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE):
                    self.bird.vel_y = JUMP_VELOCITY

            self.screen.fill((0, 0, 0))

            self.bird.update()
            if self.bird.rect.bottom > SCREEN_HEIGHT or self.bird.rect.top < 0:
                self.game_over = True

            if pygame.sprite.spritecollide(self.bird, self.pipes, False):
                self.game_over = True

            for pipe in self.pipes:
                pipe.update()
                pygame.draw.rect(self.screen, (124, 252, 0), pipe.rect_top)
                pygame.draw.rect(self.screen, (124, 252, 0), pipe.rect_bottom)

                if pipe.x + PIPE_WIDTH <= 0:
                    self.pipes.remove(pipe)
                    self.score += 1

            if len(self.pipes) == 0 or self.pipes[-1].x < SCREEN_WIDTH - 300:
                self.generate_pipes()

            pygame.draw.rect(self.screen, (255, 255, 255), self.bird.rect)
            self.display_score()
            
            pygame.display.update()
            self.clock.tick(30)

    def generate_pipes(self):
        gap_y = random.randint(200, SCREEN_HEIGHT - 400)
        self.pipes.append(Pipe(SCREEN_WIDTH, gap_y))

    def display_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def display_game_over(self):
        font = pygame.font.Font(None, 72)
        text = font.render("Game Over!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
