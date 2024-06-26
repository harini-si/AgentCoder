
import pygame
import sys
import random

# Initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_SPEED = 5

class Catcher(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - CATCHER_WIDTH) // 2
        self.rect.y = SCREEN_HEIGHT - CATCHER_HEIGHT

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 10
        if keys[pygame.K_RIGHT]:
            self.rect.x += 10
        self.rect.x = max(0, min(SCREEN_WIDTH - CATCHER_WIDTH, self.rect.x))


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - BALL_SIZE)
        self.rect.y = 0

    def update(self):
        self.rect.y += BALL_SPEED


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
        self.all_sprites = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.catcher = Catcher()
        self.all_sprites.add(self.catcher)

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if self.game_over:
            return

        self.screen.fill((0, 0, 0))

        if len(self.balls) == 0:
            ball = Ball()
            self.balls.add(ball)
            self.all_sprites.add(ball)

        self.all_sprites.update()

        for ball in self.balls:
            if ball.rect.colliderect(self.catcher.rect):
                self.score += 1
                self.balls.remove(ball)
                self.all_sprites.remove(ball)
            elif ball.rect.y >= SCREEN_HEIGHT:
                self.lives -= 1
                self.balls.remove(ball)
                self.all_sprites.remove(ball)

        if self.lives <= 0:
            self.game_over = True

        if self.game_over:
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over! Click to restart", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)

        self.all_sprites.draw(self.screen)
        score_font = pygame.font.Font(None, 24)
        score_text = score_font.render(f"Score: {self.score} Lives: {self.lives}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(60)
        return True

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
        pygame.display.update()
