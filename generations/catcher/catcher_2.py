
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_SPEED = 5
INITIAL_BALL_SPAWN = 1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Catcher(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speed = 10

    def update(self, direction):
        self.rect.x += direction * self.speed
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
        self.speed = BALL_SPEED

    def update(self):
        self.rect.y += self.speed


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
        for _ in range(INITIAL_BALL_SPAWN):
            self.spawn_ball()

    def spawn_ball(self):
        ball = Ball(random.randint(0, SCREEN_WIDTH - BALL_SIZE))
        self.balls.add(ball)

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        direction = 0
        if keys[pygame.K_LEFT]:
            direction = -1
        elif keys[pygame.K_RIGHT]:
            direction = 1

        self.catcher.update(direction)

        for ball in self.balls:
            ball.update()
            if ball.rect.colliderect(self.catcher.rect):
                self.score += 1
                self.balls.remove(ball)
                self.spawn_ball()
            elif ball.rect.bottom >= SCREEN_HEIGHT:
                self.lives -= 1
                self.balls.remove(ball)
                if self.lives == 0:
                    self.game_over = True

        self.screen.fill(BLACK)
        self.screen.blit(self.catcher.image, self.catcher.rect)
        self.balls.draw(self.screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = font.render("Game Over! Click to restart", True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
            if pygame.mouse.get_pressed()[0]:
                self.reset_game()

        pygame.display.flip()
        self.clock.tick(30)
