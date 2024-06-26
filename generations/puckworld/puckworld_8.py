
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
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Agent Navigation Game")
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()
        self.all_sprites.add(self.agent, self.green_dot, self.red_puck)

        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()
        self.agent.update(keys)

        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)

        # Calculate distance between agent and green dot
        distance = math.hypot(self.agent.rect.centerx - self.green_dot.rect.centerx,
                              self.agent.rect.centery - self.green_dot.rect.centery)

        # Update score based on proximity to green dot and red puck
        if distance < 40:
            self.score += 10
            self.green_dot.move_random()
        
        red_puck_distance = math.hypot(self.agent.rect.centerx - self.red_puck.rect.centerx,
                                       self.agent.rect.centery - self.red_puck.rect.centery)
        if red_puck_distance < 50:
            self.score -= 5

        # Display score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)

        return True

class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.velocity = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocity

class RedPuck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 60))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

    def update(self):
        # Red puck moves towards the agent slowly
        if self.rect.x < WIDTH // 2:
            self.rect.x += 1
        if self.rect.x > WIDTH // 2:
            self.rect.x -= 1
        if self.rect.y < HEIGHT // 2:
            self.rect.y += 1
        if self.rect.y > HEIGHT // 2:
            self.rect.y -= 1

class GreenDot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

    def move_random(self):
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    
    pygame.quit()
    sys.exit()
