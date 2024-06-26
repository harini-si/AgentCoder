
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
        self.clock = pygame.time.Clock()
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()
        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def run(self, event):
        """implement the game loop here, given the pygame event"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.agent.move(0, -1)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.agent.move(0, 1)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.agent.move(-1, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.agent.move(1, 0)

        self.screen.fill(WHITE)
        self.agent.update(self.green_dot, self.red_puck)
        self.screen.blit(self.agent.image, self.agent.rect)
        self.screen.blit(self.green_dot.image, self.green_dot.rect)
        self.screen.blit(self.red_puck.image, self.red_puck.rect)

        self.score += self.calculate_score()
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)
        return True

    def calculate_score(self):
        agent_pos = self.agent.rect.center
        green_dot_pos = self.green_dot.rect.center

        distance = math.hypot(green_dot_pos[0] - agent_pos[0], green_dot_pos[1] - agent_pos[1])

        if distance < 50:
            self.green_dot.reset()
            return 10
        else:
            return -1

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
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = 5

    def move(self, dx, dy):
        self.rect.x += dx * self.velocity
        self.rect.y += dy * self.velocity

    def update(self, green_dot, red_puck):
        """Implement agent behavior here"""
        pass

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
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))

    def update(self):
        """Implement red puck behavior here"""
        pass

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
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))

    def reset(self):
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))

    def update(self):
        """Implement green dot behavior here"""
        pass

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    sys.exit()
