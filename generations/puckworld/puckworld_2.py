
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
        if keys[pygame.K_LEFT]:
            self.agent.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.agent.move(1, 0)
        if keys[pygame.K_UP]:
            self.agent.move(0, -1)
        if keys[pygame.K_DOWN]:
            self.agent.move(0, 1)
            
        self.all_sprites.update()

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        
        distance_to_green_dot = math.hypot(self.agent.rect.centerx - self.green_dot.rect.centerx,
                                           self.agent.rect.centery - self.green_dot.rect.centery)
        distance_to_red_puck = math.hypot(self.agent.rect.centerx - self.red_puck.rect.centerx,
                                          self.agent.rect.centery - self.red_puck.rect.centery)
        
        reward = (100 - distance_to_green_dot) - 2 * distance_to_red_puck
        
        if reward > 0:
            self.score += reward
        
        score_display = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_display, (10, 10))

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
        
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        

class RedPuck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        
    def update(self):
        pass


class GreenDot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        
    def update(self):
        pass


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run(pygame.event.poll())
    pygame.quit()
    sys.exit()

