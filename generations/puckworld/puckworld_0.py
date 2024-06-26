
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
        self.clock = pygame.time.Clock()
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()
        self.all_sprites = pygame.sprite.Group(self.agent, self.green_dot, self.red_puck)
        self.score = 0
        
    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
        keys = pygame.key.get_pressed()
        self.agent.update(keys)
        
        # Calculate distance between agent and green dot
        distance = math.hypot(self.agent.rect.centerx - self.green_dot.rect.centerx,
                              self.agent.rect.centery - self.green_dot.rect.centery)
        
        # Reward or penalize the player based on distance to green dot
        if distance < 50:
            self.score += 10
            self.green_dot.reset_position()
            
        # Update the sprites
        self.all_sprites.update()
        self.draw()
        
        return True
        
    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        
        # Display score in top-left corner
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(self.score), True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5
        
    def update(self, keys):
        dx, dy = 0, 0
        
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed
            
        self.rect.x += dx
        self.rect.y += dy
        

class RedPuck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = pygame.Surface((60, 60))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.speed = 1
        
    def update(self):
        # Red puck slowly follows the agent
        if self.rect.x < self.agent.rect.x:
            self.rect.x += self.speed
        if self.rect.x > self.agent.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < self.agent.rect.y:
            self.rect.y += self.speed
        if self.rect.y > self.agent.rect.y:
            self.rect.y -= self.speed


class GreenDot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.reset_position()
        
    def reset_position(self):
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
        game.clock.tick(FPS)
    pygame.quit()
    sys.exit()
