
import pygame
import random
import sys

# Initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_RADIUS = 10

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Catcher(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)
    
    def update(self, direction):
        if direction == 'left':
            self.rect.x -= 5
        elif direction == 'right':
            self.rect.x += 5
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, BLACK, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - BALL_RADIUS * 2)
        self.rect.y = 0

    def update(self):
        self.rect.y += 3

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
        self.catcher = Catcher()
        self.balls = pygame.sprite.Group()
    
    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle catcher movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.catcher.update('left')
        if keys[pygame.K_RIGHT]:
            self.catcher.update('right')

        # Spawn new balls
        if len(self.balls) == 0:
            self.balls.add(Ball())

        # Update ball positions
        for ball in self.balls:
            ball.update()

        # Check for collisions
        collisions = pygame.sprite.spritecollide(self.catcher, self.balls, True)
        if collisions:
            self.score += 1

        # Check for missed balls
        for ball in self.balls:
            if ball.rect.y >= SCREEN_HEIGHT:
                self.lives -= 1
                self.balls.remove(ball)

        # Game over condition
        if self.lives == 0:
            self.game_over = True
        
        # Display elements
        self.screen.fill(BLACK)
        self.balls.draw(self.screen)
        self.screen.blit(self.catcher.image, self.catcher.rect)
        self.clock.tick(60)
        pygame.display.flip()

        return True if not self.game_over else False

# Test cases
game = Game()
assert game.score == 0, "Initial score should be 0"
assert game.lives == 3, "Initial lives should be 3"
assert not game.game_over, "Game should not be over initially"
assert isinstance(game.catcher, Catcher), "Catcher should be an instance of the Catcher class"
assert isinstance(game.balls, pygame.sprite.Group), "Balls should be a Sprite Group"
assert len(game.balls) > 0, "There should be at least one initial ball on the screen"
