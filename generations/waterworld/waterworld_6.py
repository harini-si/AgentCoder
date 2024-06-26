
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
        self.font = pygame.font.Font(None, 36)
        self.agent = Agent()
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()
        
    def spawn_initial_circles(self):
        for _ in range(GRID_WIDTH // 2):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)
    
    def spawn_circle(self, color):
        while True:
            x = random.randint(0, GRID_WIDTH-1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT-1) * GRID_SIZE
            if not any(circle.rect.topleft == (x, y) for circle in self.circles):
                circle = Circle(color)
                circle.rect.topleft = (x, y)
                self.circles.add(circle)
                break

    def update_circles(self):
        collisions = pygame.sprite.spritecollide(self.agent, self.circles, True)
        for circle in collisions:
            if circle.color == GREEN:
                self.score += 1
            else:
                self.score -= 1
            self.spawn_circle(random.choice([GREEN, RED]))
        
        if all(circle.color == GREEN for circle in self.circles):
            self.game_over = True

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.agent.reset()
        self.circles.empty()
        self.spawn_initial_circles()
        
    def handle_events(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.game_over and event.type == pygame.KEYDOWN:
                self.reset_game()
        
    def render_game(self):
        self.screen.fill(WHITE)
        self.circles.update()
        self.circles.draw(self.screen)
        self.screen.blit(self.agent.image, self.agent.rect)
        score_text = self.font.render(f"Score: {self.score}", True, BLUE)
        self.screen.blit(score_text, (10, 10))
        if self.game_over:
            self.show_message("Game Over!")
        pygame.display.flip()
        
    def show_message(self, message, size=36):
        text = self.font.render(message, True, BLUE)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(text, text_rect)
        
    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.agent.move()
            self.update_circles()
            self.render_game()
        self.clock.tick(FPS)
        return True

class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def reset(self):
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def move(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -GRID_SIZE
        if keys[pygame.K_RIGHT]:
            dx = GRID_SIZE
        if keys[pygame.K_UP]:
            dy = -GRID_SIZE
        if keys[pygame.K_DOWN]:
            dy = GRID_SIZE
        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()

    def reset(self):
        self.rect.topleft = (random.randint(0, GRID_WIDTH-1) * GRID_SIZE, random.randint(0, GRID_HEIGHT-1) * GRID_SIZE)
        
    def update(self):
        self.move_smoothly()
        
    def move_smoothly(self):
        self.rect.x += random.randint(-GRID_SIZE, GRID_SIZE)
        self.rect.y += random.randint(-GRID_SIZE, GRID_SIZE)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

if __name__ == "__main__":
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        game.run(event)
