
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

    def distance(self, obj1, obj2):
        return math.hypot(obj1.rect.centerx - obj2.rect.centerx, obj1.rect.centery - obj2.rect.centery)

    def relocate_green_dot(self):
        self.green_dot.rect.x = random.randint(0, WIDTH)
        self.green_dot.rect.y = random.randint(0, HEIGHT)

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.agent.rect.x -= self.agent.velocity
        if keys[pygame.K_RIGHT]:
            self.agent.rect.x += self.agent.velocity
        if keys[pygame.K_UP]:
            self.agent.rect.y -= self.agent.velocity
        if keys[pygame.K_DOWN]:
            self.agent.rect.y += self.agent.velocity

        self.screen.fill(WHITE)
        
        if self.distance(self.agent, self.green_dot) < self.distance(self.agent, self.red_puck):
            self.score += 1
        else:
            self.score -= 1

        self.agent.draw(self.screen)
        self.red_puck.draw(self.screen)
        self.green_dot.draw(self.screen)
        font = pygame.font.SysFont(None, 36)
        text = font.render('Score: ' + str(self.score), True, BLACK)
        self.screen.blit(text, (10, 10))

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
        self.velocity = 5

    def draw(self, screen):
        screen.blit(self.image, self.rect)


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
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


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
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    sys.exit()
