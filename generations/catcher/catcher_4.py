
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_RADIUS = 15
CATCHER_COLOR = (0, 255, 0)
BALL_COLOR = (255, 0, 0)

class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill(CATCHER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = SCREEN_HEIGHT

    def update(self, direction):
        if direction == "right":
            self.rect.x += 5
        elif direction == "left":
            self.rect.x -= 5
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, BALL_COLOR, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0

    def update(self):
        self.rect.y += 5


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = pygame.sprite.Group()
        self.spawn_ball()

    def spawn_ball(self):
        x = random.randint(0, SCREEN_WIDTH - BALL_RADIUS * 2)
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
                if ball.rect.top > SCREEN_HEIGHT:
                    self.lives -= 1
                    self.balls.remove(ball)
                    self.spawn_ball()
            self.screen.fill((0, 0, 0))

            for ball in self.balls:
                self.screen.blit(ball.image, ball.rect)
            self.screen.blit(self.catcher.image, self.catcher.rect)
            font = pygame.font.Font(None, 36)
            score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            lives_text = font.render("Lives: " + str(self.lives), True, (255, 255, 255))
            self.screen.blit(lives_text, (10, 40))

            if self.lives <= 0:
                self.game_over = True
                font = pygame.font.Font(None, 72)
                game_over_text = font.render("Game Over!", True, (255, 0, 0))
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                    self.reset_game()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.catcher.update("left")
            if keys[pygame.K_RIGHT]:
                self.catcher.update("right")

            self.clock.tick(30)
        return True


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
