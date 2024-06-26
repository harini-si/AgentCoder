
import pygame
import sys
import random

# Initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_RADIUS = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Catcher(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the catcher
        self.rect should be a pygame.Rect object with the initial position of the catcher
        """
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT

    def update(self, direction):
        if direction == "left":
            self.rect.x -= 5
        elif direction == "right":
            self.rect.x += 5
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the ball
        self.rect should be a pygame.Rect object with the initial position of the ball
        """
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - BALL_RADIUS * 2)
        self.rect.y = 0

    def update(self):
        self.rect.y += 5


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        """
        Initialize / reset the game
        self.game_over is a boolean representing whether the game is over
        self.lives represents the number of lives the player has
        self.score keeps track of the player's score
        self.catch is an instance of the Catcher class
        self.balls is a Sprite Group of all balls (of the class Ball), it should never be empty
        """
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher()
        self.balls = pygame.sprite.Group()

    def handle_events(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.catcher.update("left")
                elif event.key == pygame.K_RIGHT:
                    self.catcher.update("right")

    def check_collision(self):
        for ball in self.balls:
            if pygame.sprite.collide_rect(self.catcher, ball):
                self.score += 1
                ball.kill()

    def update_balls(self):
        for ball in self.balls:
            ball.update()
            if ball.rect.y >= SCREEN_HEIGHT:
                self.lives -= 1
                ball.kill()

    def display_text(self, text, size, color, x, y):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def run(self, event):
        while not self.game_over:
            self.handle_events(event)
            self.screen.fill(BLACK)
            
            if not self.balls:
                self.balls.add(Ball())

            self.check_collision()
            self.update_balls()

            self.balls.draw(self.screen)
            self.screen.blit(self.catcher.image, self.catcher.rect.topleft)
            
            self.display_text(f"Score: {self.score}", 30, WHITE, 100, 50)
            self.display_text(f"Lives: {self.lives}", 30, WHITE, SCREEN_WIDTH - 100, 50)
            pygame.display.flip()
            self.clock.tick(30)

            if self.lives <= 0:
                self.game_over = True
                self.display_text("Game Over!", 50, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                pygame.display.flip()
                
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                    self.reset_game()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run(pygame.event)
    pygame.quit()
