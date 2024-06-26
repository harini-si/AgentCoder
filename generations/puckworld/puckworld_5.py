
import pygame
import sys
import random
import math

WIDTH, HEIGHT = 1000, 1000
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Game:
    def __init__(self):
        """Initialize the game
        self.screen is the Pygame display surface
        self.agent: the player's character
        self.green_dot: the target for the agent
        self.red_puck: the obstacle for the agent
        self.score: the player's score
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()
        self.score = 0

    def run(self, event):
        """Game loop"""
        self.screen.fill(WHITE)

        for entity in [self.green_dot, self.red_puck, self.agent]:
            self.screen.blit(entity.image, entity.rect)

        distance_to_green_dot = math.hypot(
            self.agent.rect.center[0] - self.green_dot.rect.center[0],
            self.agent.rect.center[1] - self.green_dot.rect.center[1]
        )

        distance_to_red_puck = math.hypot(
            self.agent.rect.center[0] - self.red_puck.rect.center[0],
            self.agent.rect.center[1] - self.red_puck.rect.center[1]
        )

        self.score += 1 / distance_to_green_dot if distance_to_green_dot != 0 else 0
        self.score -= 1 / distance_to_red_puck if distance_to_red_puck != 0 else 0

        font = pygame.font.Font(None, 36)
        score_text = font.render('Score: {:.2f}'.format(self.score), True, BLACK)
        self.screen.blit(score_text, (10, 10))

        for entity in [self.green_dot, self.red_puck]:
            entity.move()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.agent.rect.x -= 3
        if keys[pygame.K_RIGHT]:
            self.agent.rect.x += 3
        if keys[pygame.K_UP]:
            self.agent.rect.y -= 3
        if keys[pygame.K_DOWN]:
            self.agent.rect.y += 3

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        pygame.display.flip()
        return True


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        """Initialize the agent
        velocity: the agent's speed
        self.image is the Pygame Surface object representing the Agent
        self.rect is the Pygame Rect object representing the agent's position
        """
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)


class RedPuck(pygame.sprite.Sprite):
    """Class representing the red puck obstacle"""

    def __init__(self):
        """
        Initialize the red puck
        self.image is the Pygame Surface object representing the RedPuck
        self.rect is the Pygame Rect object representing the RedPuck's position
        """
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

    def move(self):
        self.rect.center = (self.rect.center[0] + random.randint(-1, 1), self.rect.center[1] + random.randint(-1, 1))


class GreenDot(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the green dot
        self.image is the Pygame Surface object representing the GreenDot
        self.rect is the Pygame Rect object representing the GreenDot's position
        """
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

    def move(self):
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    sys.exit()
