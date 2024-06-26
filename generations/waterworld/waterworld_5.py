
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
        """
        Initialize the game window, clock, game_over status, and score.
        Create sprite groups for all game objects.
        agent: The player-controlled sprite.
        circles: A group of all circles in the game.
        """
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
        """
        Spawn initial circles on the game grid.
        """
        for _ in range(GRID_WIDTH // 2 - 1):
            self.spawn_circle(RED)
        for _ in range(GRID_WIDTH // 2 - 1):
            self.spawn_circle(GREEN)

    def spawn_circle(self, color):
        """
        Spawn a circle with the given color on the game grid.
        Ensure no collision with existing sprites.
        """
        circle = Circle(color)
        circle.rect.topleft = (random.randint(0, GRID_WIDTH) * GRID_SIZE, random.randint(0, GRID_HEIGHT) * GRID_SIZE)
        self.circles.add(circle)

    def update_circles(self):
        """
        Update circles based on collisions with the agent.
        Update score accordingly.
        """
        collisions = pygame.sprite.spritecollide(self.agent, self.circles, True)
        for circle in collisions:
            if circle.color == GREEN:
                self.score += 1
                self.spawn_circle(random.choice([RED, GREEN]))

        if len([circle for circle in self.circles if circle.color == GREEN]) == 0:
            self.game_over = True

    def reset_game(self):
        """
        Reset the game state.
        """
        self.score = 0
        for circle in self.circles:
            circle.kill()
        self.spawn_initial_circles()
        self.agent.reset()

    def handle_events(self, event):
        """
        Handle game events, including quitting and restarting the game.
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

    def render_game(self):
        """
        Render the game screen, including sprites and score.
        Display game over or win messages as needed.
        """
        self.screen.fill(WHITE)
        self.agent.update()
        self.agent.move(pygame.key.get_pressed())

        for circle in self.circles:
            circle.update()
            circle.move_smoothly()

        self.circles.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, BLUE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            self.show_message("Game Over!", 72)

        pygame.display.flip()

    def show_message(self, message, size=36):
        """
        Display a message on the screen.
        """
        text = pygame.font.Font(None, size).render(message, True, BLUE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def run(self, event):
        """
        Main game loop.
        """
        self.handle_events(event)
        self.update_circles()
        self.render_game()

        self.clock.tick(FPS)
        return True

class Agent(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the agent sprite.
        
        """
        super().__init__()
        self.image = pygame.Surface(
            (CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def reset(self):
        """
        Reset the agent's position.
        """
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def move(self, keys):
        """
        Move the agent based on keyboard input.
        """
        if keys[pygame.K_LEFT]:
            self.rect.x -= GRID_SIZE
        if keys[pygame.K_RIGHT]:
            self.rect.x += GRID_SIZE
        if keys[pygame.K_UP]:
            self.rect.y -= GRID_SIZE
        if keys[pygame.K_DOWN]:
            self.rect.y += GRID_SIZE

        self.rect.left = min(max(self.rect.left, 0), WIDTH - GRID_SIZE)
        self.rect.top = min(max(self.rect.top, 0), HEIGHT - GRID_SIZE)

    def update(self):
        """
        Update method for the agent (unused in this example).
        """
        pass

class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        """
        Initialize a circle sprite with a specified color and direction
        """
        super().__init__()
        self.color = color
        self.image = pygame.Surface(
            (CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image,
            color,
            (CIRCLE_RADIUS, CIRCLE_RADIUS),
            CIRCLE_RADIUS
        )
        self.rect = self.image.get_rect()

    def reset(self):
        """
        Reset the circle's position and direction.
        """
        self.rect.topleft = (random.randint(0, GRID_WIDTH) * GRID_SIZE, random.randint(0, GRID_HEIGHT) * GRID_SIZE)

    def update(self):
        """
        Update the circle's position.
        """
    
    def move_smoothly(self):
        """
        Move the circle smoothly across the screen.
        """
        self.rect = self.rect.move(random.randint(-GRID_SIZE, GRID_SIZE), random.randint(-GRID_SIZE, GRID_SIZE))


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            game.run(event)
    pygame.quit()

