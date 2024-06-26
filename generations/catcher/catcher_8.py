
import pygame
import sys
import random

# Initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_RADIUS = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Catcher(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - CATCHER_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - CATCHER_HEIGHT

    def move(self, direction):
        if direction == "LEFT":
            self.rect.x -= 10
        elif direction == "RIGHT":
            self.rect.x += 10
        self.rect.x = max(0, min(SCREEN_WIDTH - CATCHER_WIDTH, self.rect.x))

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - BALL_RADIUS * 2)
        self.rect.y = -BALL_RADIUS * 2

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Catch The Ball")
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
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                self.reset_game()

        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.catcher.move("LEFT")
            if keys[pygame.K_RIGHT]:
                self.catcher.move("RIGHT")

            self.screen.fill(BLACK)

            for ball in self.balls:
                ball.rect.y += 5
                if ball.rect.colliderect(self.catcher.rect):
                    self.score += 1
                    self.balls.remove(ball)
                    self.balls.add(Ball())

                if ball.rect.y > SCREEN_HEIGHT:
                    self.balls.remove(ball)
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over = True

            self.balls.draw(self.screen)
            self.screen.blit(self.catcher.image, self.catcher.rect)

            font = pygame.font.Font(None, 36)
            score_text = font.render("Score: " + str(self.score), True, WHITE)
            self.screen.blit(score_text, (10, 10))

            lives_text = font.render("Lives: " + str(self.lives), True, WHITE)
            self.screen.blit(lives_text, (10, 40))

        if self.game_over:
            font = pygame.font.Font(None, 60)
            game_over_text = font.render("Game Over!", True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 30))
            restart_text = font.render("Click to Restart", True, WHITE)
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 30))

        pygame.display.flip()
        self.clock.tick(30)
        return True


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run(pygame.event.get())
    pygame.quit()
