
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
        self.all_sprites = pygame.sprite.Group(self.agent, self.green_dot, self.red_puck)
        self.score = 0
        self.font = pygame.font.Font(None, 36)

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
        
        self.all_sprites.update()

        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.update_score()
        pygame.display.flip()
        return True

    def update_score(self):
        self.score += self.calculate_score()
        text = self.font.render("Score: " + str(self.score), True, BLACK)
        self.screen.blit(text, (10, 10))

    def calculate_score(self):
        agent_pos = self.agent.rect.center
        green_dot_pos = self.green_dot.rect.center
        red_puck_pos = self.red_puck.rect.center
        agent_green_dot_dist = math.hypot(green_dot_pos[0] - agent_pos[0], green_dot_pos[1] - agent_pos[1])
        agent_red_puck_dist = math.hypot(red_puck_pos[0] - agent_pos[0], red_puck_pos[1] - agent_pos[1])
        if agent_red_puck_dist < 100:
            return -1
        return 1 / agent_green_dot_dist

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
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

class GreenDot(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the green dot
        self.image is the Pygame Surface object representing the GreenDot
        self.rect is the Pygame Rect object representing the GreenDot's position
        """
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run(pygame.event.poll())
    pygame.quit()
    sys.exit()
