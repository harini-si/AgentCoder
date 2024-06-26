
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
        self.all_sprites = pygame.sprite.Group(self.agent, self.green_dot, self.red_puck)
        
        self.score = 0
        self.font = pygame.font.SysFont None, 25)
        
    def run(self, event):
        """Game loop"""
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

        self.agent.update()

        self.red_puck.follow(self.agent.rect)

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        
        distance_to_dot = math.hypot(self.green_dot.rect.x - self.agent.rect.x, self.green_dot.rect.y - self.agent.rect.y)
        distance_to_puck = math.hypot(self.red_puck.rect.x - self.agent.rect.x, self.red_puck.rect.y - self.agent.rect.y)
        
        self.score += 1 / distance_to_dot ** 2 if distance_to_dot != 0 else 0  # Positive reward
        self.score -= 1 / distance_to_puck ** 2 if distance_to_puck != 0 else 0  # Penalty
        
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        self.clock.tick(FPS)
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

    def move(self, dx, dy):
        self.rect.x += dx * self.velocity
        self.rect.y += dy * self.velocity

    def update(self):
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


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

    def follow(self, target_rect):
        target_x, target_y = target_rect.center
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        dist = math.hypot(dx, dy)
        
        if dist != 0:
            dx = dx / dist
            dy = dy / dist
        
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
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    sys.exit()
