
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
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()
        self.score = 0

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        keys = pygame.key.get_pressed()
        self.agent.update(keys)
        
        self.screen.fill(WHITE)
        self.screen.blit(self.agent.image, self.agent.rect)
        self.screen.blit(self.green_dot.image, self.green_dot.rect)
        self.screen.blit(self.red_puck.image, self.red_puck.rect)

        self.calculate_score()
        self.display_score()

        pygame.display.flip()
        return True

    def calculate_score(self):
        agent_pos = self.agent.rect.center
        green_dot_pos = self.green_dot.rect.center
        red_puck_pos = self.red_puck.rect.center

        agent_green_dist = math.hypot(green_dot_pos[0] - agent_pos[0], green_dot_pos[1] - agent_pos[1])
        agent_red_dist = math.hypot(red_puck_pos[0] - agent_pos[0], red_puck_pos[1] - agent_pos[1])

        if agent_green_dist < 20:  # Agent reached green dot
            self.green_dot.reset_position()
            self.score += 10
        elif agent_red_dist < 20:  # Agent too close to red puck
            self.score -= 5

    def display_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(self.score), True, BLACK)
        self.screen.blit(score_text, (10, 10))

class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(WIDTH/2, HEIGHT/2))
        self.velocity = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.velocity, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.velocity, 0)
        if keys[pygame.K_UP]:
            self.rect.move_ip(0, -self.velocity)
        if keys[pygame.K_DOWN]:
            self.rect.move_ip(0, self.velocity)


class RedPuck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))

    def update(self):
        pass


class GreenDot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))

    def reset_position(self):
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    sys.exit()

