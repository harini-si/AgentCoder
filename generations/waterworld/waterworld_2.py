
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
        self.player = Agent()
        self.circles = pygame.sprite.Group()
        self.red_circles = pygame.sprite.Group()
        self.green_circles = pygame.sprite.Group()
        self.spawn_initial_circles()
        
    def spawn_initial_circles(self):
        for _ in range(GRID_WIDTH):
            self.spawn_circle(RED)
            self.spawn_circle(GREEN)
        
    def spawn_circle(self, color):
        circle = Circle(color)
        circle.rect.topleft = random.randint(0, GRID_WIDTH) * GRID_SIZE, random.randint(0, GRID_HEIGHT) * GRID_SIZE
        self.circles.add(circle)
        if color == RED:
            self.red_circles.add(circle)
        else:
            self.green_circles.add(circle)
    
    def update_circles(self):
        for circle in self.circles:
            if pygame.sprite.collide_rect(self.player, circle):
                if circle.color == GREEN:
                    self.score += 1
                else:
                    self.score -= 1
                self.circles.remove(circle)
                self.spawn_circle(random.choice([RED, GREEN]))
                break
        
        if len(self.green_circles) == 0:
            self.game_over = True
            
        
    def reset_game(self):
        self.score = 0
        self.spawn_initial_circles()
        self.player.reset()
        self.game_over = False
        
    def handle_events(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
    
    def render_game(self):
        self.screen.fill(WHITE)
        self.circles.draw(self.screen)
        
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, BLUE)
        self.screen.blit(text, (10, 10))
        
        if self.game_over:
            self.show_message("Game Over!")
        
        pygame.display.flip()
        
    def show_message(self, message, size=36):
        font = pygame.font.Font(None, size)
        text = font.render(message, True, BLUE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        
    def run(self, event):
        self.handle_events(event)
        
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move("left")
            if keys[pygame.K_RIGHT]:
                self.player.move("right")
            if keys[pygame.K_UP]:
                self.player.move("up")
            if keys[pygame.K_DOWN]:
                self.player.move("down")
                
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

    def move(self, direction):
        if direction == "left":
            self.rect.x -= GRID_SIZE
        elif direction == "right":
            self.rect.x += GRID_SIZE
        elif direction == "up":
            self.rect.y -= GRID_SIZE
        elif direction == "down":
            self.rect.y += GRID_SIZE

    def update(self):
        pass


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()

    def reset(self):
        self.rect.topleft = random.randint(0, GRID_WIDTH) * GRID_SIZE, random.randint(0, GRID_HEIGHT) * GRID_SIZE

    def update(self):
        pass

    def move_smoothly(self):
        self.rect.x += random.randint(-1, 1) * GRID_SIZE
        self.rect.y += random.randint(-1, 1) * GRID_SIZE


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        running = game.run(event)
    pygame.quit()
