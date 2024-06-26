
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
        for _ in range(GRID_WIDTH):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        valid_position = False
        while not valid_position:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            valid_position = True
            for circle in self.circles:
                if circle.rect.collidepoint(x, y):
                    valid_position = False
                    break
        circle = Circle(color)
        circle.rect.topleft = (x, y)
        self.circles.add(circle)

    def update_circles(self):
        collisions = pygame.sprite.spritecollide(self.agent, self.circles, True)
        for circle in collisions:
            if circle.color == GREEN:
                self.score += 1
            elif circle.color == RED:
                self.score -= 1
            self.spawn_circle(random.choice([GREEN, RED]))

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.agent.reset()
        self.circles.empty()
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()

    def render_game(self):
        self.screen.fill(WHITE)
        self.circles.update()
        self.agent.update()
        self.circles.draw(self.screen)
        self.screen.blit(self.agent.image, self.agent.rect.topleft)

        score_text = self.font.render(f"Score: {self.score}", True, BLUE)
        self.screen.blit(score_text, (10, 10))

        if self.score >= len([circle for circle in self.circles if circle.color == GREEN]):
            self.show_message("Game Over!")

        pygame.display.flip()

    def show_message(self, message, size=36):
        text = self.font.render(message, True, BLUE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        
        self.game_over = True

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
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

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= GRID_SIZE
        if keys[pygame.K_DOWN]:
            self.rect.y += GRID_SIZE
        if keys[pygame.K_LEFT]:
            self.rect.x -= GRID_SIZE
        if keys[pygame.K_RIGHT]:
            self.rect.x += GRID_SIZE

        self.rect.left = max(0, min(self.rect.left, WIDTH - GRID_SIZE))
        self.rect.top = max(0, min(self.rect.top, HEIGHT - GRID_SIZE))

class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()

    def reset(self):
        self.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        self.rect.x += random.choice([-GRID_SIZE, 0, GRID_SIZE])
        self.rect.y += random.choice([-GRID_SIZE, 0, GRID_SIZE])
        self.rect.left = max(0, min(self.rect.left, WIDTH - GRID_SIZE))
        self.rect.top = max(0, min(self.rect.top, HEIGHT - GRID_SIZE))

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
