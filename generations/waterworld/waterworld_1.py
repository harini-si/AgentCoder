
import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 60
CIRCLE_RADIUS = 10

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("WaterWorld Game")
        
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0

        self.agent = Agent()
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        self.spawn_circle(GREEN)
        self.spawn_circle(RED)

    def spawn_circle(self, color):
        circle = Circle(color)
        while pygame.sprite.spritecollide(circle, self.circles, False):
            circle.reset()
        self.circles.add(circle)

    def update_circles(self):
        collisions = pygame.sprite.spritecollide(self.agent, self.circles, True)
        for circle in collisions:
            if circle.color == GREEN:
                self.score += 1
                self.spawn_circle(random.choice([GREEN, RED]))
            else:
                self.score -= 1

    def reset_game(self):
        self.score = 0
        self.game_over = False
        self.circles.empty()
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.reset_game()

    def render_game(self):
        self.screen.fill(WHITE)
        self.agent.update()
        self.circles.update()
        self.circles.draw(self.screen)
        self.agent.draw(self.screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLUE)
        self.screen.blit(score_text, (10, 10))

        if len(self.circles) == 1 and list(self.circles)[0].color == RED:
            self.show_message("Game Over! Press 'R' to restart", 48)

        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.Font(None, size)
        text = font.render(message, True, BLUE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def run(self, event):
        if not self.game_over:
            self.handle_events(event)

            keys = pygame.key.get_pressed()
            direction = [keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], 
                         keys[pygame.K_DOWN] - keys[pygame.K_UP]]
            self.agent.move(direction)

            if len(self.circles) == 1 and list(self.circles)[0].color == GREEN:
                self.show_message("Game Over!")
                self.game_over = True

            self.update_circles()
            self.render_game()
            
        self.clock.tick(FPS)
        return not self.game_over

class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def reset(self):
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def move(self, direction):
        self.rect.move_ip(direction[0] * GRID_SIZE, direction[1] * GRID_SIZE)
        self.rect.left = max(0, min(self.rect.left, WIDTH - CIRCLE_RADIUS * 2))
        self.rect.top = max(0, min(self.rect.top, HEIGHT - CIRCLE_RADIUS * 2))

    def update(self):
        pass

class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, 
                             random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        self.rect.move_ip(random.randint(-1, 1) * GRID_SIZE, random.randint(-1, 1) * GRID_SIZE)
        self.rect.left = max(0, min(self.rect.left, WIDTH - CIRCLE_RADIUS * 2))
        self.rect.top = max(0, min(self.rect.top, HEIGHT - CIRCLE_RADIUS * 2))

if __name__ == "__main__":
    game = Game()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.run(event)

    pygame.quit()
