
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_RADIUS = 15
CATCHER_SPEED = 10
BALL_SPEED = 5

WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Catcher(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= CATCHER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += CATCHER_SPEED
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)

class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.center = (x, 0)

    def update(self):
        self.rect.y += BALL_SPEED


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
        x = random.randint(0, SCREEN_WIDTH)
        ball = Ball(x)
        self.balls.add(ball)

    def run(self, event):
        if not self.game_over:
            for ball in self.balls:
                ball.update()
                if ball.rect.colliderect(self.catcher.rect):
                    self.score += 1
                    self.balls.remove(ball)
                    self.spawn_ball()
                if ball.rect.bottom >= SCREEN_HEIGHT:
                    self.balls.remove(ball)
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over = True

            self.catcher.update()

            self.screen.fill((0, 0, 0))
            self.balls.draw(self.screen)
            self.screen.blit(self.catcher.image, self.catcher.rect)

            score_font = pygame.font.Font(None, 36)
            score_text = score_font.render("Score: " + str(self.score), True, WHITE)
            self.screen.blit(score_text, (20, 20))

            pygame.display.flip()
            self.clock.tick(60)

            if self.game_over:
                game_over_font = pygame.font.Font(None, 70)
                game_over_text = game_over_font.render("Game Over!", True, WHITE)
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 50))
                pygame.display.flip()
        else:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_game()
                    self.game_over = False

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        return True

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
