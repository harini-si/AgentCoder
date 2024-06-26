
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
        """Implement the game loop here, given the pygame event"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.agent.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.agent.move(1, 0)
        if keys[pygame.K_UP]:
            self.agent.move(0, -1)
        if keys[pygame.K_DOWN]:
            self.agent.move(0, 1)

        self.screen.fill(BLACK)
        self.screen.blit(self.agent.image, self.agent.rect)
        self.screen.blit(self.green_dot.image, self.green_dot.rect)
        self.screen.blit(self.red_puck.image, self.red_puck.rect)

        is_collision = pygame.sprite.collide_rect(self.agent, self.red_puck)
        if is_collision:
            self.score -= 1

        distance = math.sqrt((self.green_dot.rect.x - self.agent.rect.x) ** 2 + (self.green_dot.rect.y - self.agent.rect.y) ** 2)
        if distance < 20:
            self.score += 1
            self.green_dot.reset()

        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
        return True


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        """Initialize the agent
        velocity: the agent's speed
        self.image is the Pygame Surface object representing the Agent
        self.rect is the Pygame Rect object representing the agent's position
        """
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - 15
        self.rect.y = HEIGHT // 2 - 15
        self.velocity = 5

    def move(self, dx, dy):
        self.rect.x += dx * self.velocity
        self.rect.y += dy * self.velocity

class RedPuck(pygame.sprite.Sprite):
    """Class representing the red puck obstacle"""

    def __init__(self):
        """
        Initialize the red puck
        self.image is the Pygame Surface object representing the RedPuck
        self.rect is the Pygame Rect object representing the RedPuck's position
        """
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 50)
        self.rect.y = random.randint(0, HEIGHT - 50)

    def update(self, agent):
        dx = 0
        dy = 0
        if self.rect.x < agent.rect.x:
            dx = 1
        elif self.rect.x > agent.rect.x:
            dx = -1
        if self.rect.y < agent.rect.y:
            dy = 1
        elif self.rect.y > agent.rect.y:
            dy = -1
        self.rect.x += dx
        self.rect.y += dy

class GreenDot(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the green dot
        self.image is the Pygame Surface object representing the GreenDot
        self.rect is the Pygame Rect object representing the GreenDot's position
        """
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.x = random.randint(0, WIDTH - 20)
        self.rect.y = random.randint(0, HEIGHT - 20)

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    sys.exit()
