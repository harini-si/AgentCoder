
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Catcher(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT)

class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, 0)
        self.speed = 5

    def update(self):
        self.rect.y += self.speed


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Catch the Ball')
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher()
        self.balls = pygame.sprite.Group()
        self.spawn_ball()

    def spawn_ball(self):
        x = random.randint(0, SCREEN_WIDTH - 30)
        ball = Ball(x)
        self.balls.add(ball)

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.catcher.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.catcher.rect.x += 5

        self.screen.fill(WHITE)
        self.balls.update()

        for ball in self.balls:
            if ball.rect.colliderect(self.catcher.rect):
                self.score += 1
                self.balls.remove(ball)
                self.spawn_ball()
            elif ball.rect.bottom >= SCREEN_HEIGHT:
                self.lives -= 1
                self.balls.remove(ball)
                self.spawn_ball()

        if self.lives <= 0:
            self.game_over = True

        if self.game_over:
            font = pygame.font.Font(None, 36)
            text = font.render('Game Over! Click to Restart', True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()

        self.balls.draw(self.screen)
        self.screen.blit(self.catcher.image, self.catcher.rect)
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render('Score: ' + str(self.score), True, BLACK)
        self.screen.blit(score_text, (10, 10))
        lives_text = score_font.render('Lives: ' + str(self.lives), True, BLACK)
        self.screen.blit(lives_text, (10, 40))

        pygame.display.flip()
        self.clock.tick(30)
        return True


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
