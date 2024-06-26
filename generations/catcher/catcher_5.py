
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_SPEED = 5

class Catcher(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT

    def update(self, direction):
        self.rect.x += direction
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - BALL_SIZE)
        self.rect.y = 0

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
        self.balls.add(Ball())

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.catcher.update(-5)
                if event.key == pygame.K_RIGHT:
                    self.catcher.update(5)

        if not self.game_over:
            self.screen.fill(WHITE)

            self.balls.update()
            self.catcher.update(0)

            for ball in self.balls:
                if pygame.sprite.collide_rect(self.catcher, ball):
                    self.score += 1
                    self.balls.remove(ball)
                    self.balls.add(Ball())

                if ball.rect.top > SCREEN_HEIGHT:
                    self.lives -= 1
                    self.balls.remove(ball)
                    if self.lives <= 0:
                        self.game_over = True

            self.balls.draw(self.screen)
            self.screen.blit(self.catcher.image, self.catcher.rect)

            font = pygame.font.Font(None, 36)
            score_text = font.render("Score: " + str(self.score), True, BLACK)
            self.screen.blit(score_text, (10, 10))

            lives_text = font.render("Lives: " + str(self.lives), True, BLACK)
            self.screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))

            if self.game_over:
                game_over_text = font.render("Game Over! Click to restart.", True, BLACK)
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

                if pygame.mouse.get_pressed()[0]:
                    self.reset_game()

            pygame.display.flip()
            self.clock.tick(30)

        return True

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        running = game.run(pygame.event.poll())
    pygame.quit()
