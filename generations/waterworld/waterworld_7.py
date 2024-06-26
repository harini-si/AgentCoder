
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
        self.agent = Agent()
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        """
        Spawn initial circles on the game grid.
        """
        for _ in range(GRID_WIDTH * GRID_HEIGHT // 2):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        """
        Spawn a circle with the given color on the game grid.
        Ensure no collision with existing sprites.
        """
        is_colliding = True
        while is_colliding:
            x = random.randrange(GRID_WIDTH) * GRID_SIZE
            y = random.randrange(GRID_HEIGHT) * GRID_SIZE
            circle = Circle(color)
            circle.rect.topleft = (x, y)
            is_colliding = pygame.sprite.spritecollide(circle, self.circles, False)
        self.circles.add(circle)
    
    def update_circles(self):
        """
        Update circles based on collisions with the agent.
        Update score accordingly.
        """
        captured_circles = pygame.sprite.spritecollide(self.agent, self.circles, True)
        for circle in captured_circles:
            if circle.color == GREEN:
                self.score += 1
                self.spawn_circle(random.choice([GREEN, RED]))
            elif circle.color == RED:
                self.score -= 1
    
    def reset_game(self):
        """
        Reset the game state.
        """
        self.game_over = False
        self.score = 0
        self.circles.empty()
        self.spawn_initial_circles()

    def handle_events(self, event):
        """
        Handle game events, including quitting and restarting the game.
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if self.game_over and event.type == pygame.KEYDOWN:
            self.reset_game()

    def render_game(self):
        """
        Render the game screen, including sprites and score.
        Display game over or win messages as needed.
        """
        self.screen.fill(WHITE)
        self.circles.draw(self.screen)
        self.agent.draw(self.screen)
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score}', True, BLUE)
        self.screen.blit(text, (10, 10))
        if len(self.circles) == 0 or self.score == len(pygame.sprite.Group([c for c in self.circles if c.color == GREEN])):
            self.game_over = True
            self.show_message('Game Over!', size=72)

        pygame.display.flip()

    def show_message(self, message, size=36):
        """
        Display a message on the screen.
        """
        font = pygame.font.Font(None, size)
        text = font.render(message, True, BLUE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def run(self, event):
        """
        Main game loop.
        """
        self.handle_events(event)
        if not self.game_over:
            self.agent.update()
            for circle in self.circles:
                circle.update()
                circle.move_smoothly()
            self.update_circles()
            self.render_game()
            self.clock.tick(FPS)
        return not self.game_over

class Agent(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the agent sprite.
        """
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def reset(self):
        """
        Reset the agent's position.
        """
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def move(self, direction):
        """
        Move the agent in the specified direction.
        """
        key_map = {pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1), pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)}
        if direction in key_map:
            dx, dy = key_map[direction]
            new_x = self.rect.x + dx * GRID_SIZE
            new_y = self.rect.y + dy * GRID_SIZE
            self.rect.topleft = (new_x, new_y)
            self.rect.move_ip(dx * GRID_SIZE, dy * GRID_SIZE)

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
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()

    def reset(self):
        """
        Reset the circle's position and direction.
        """
        self.rect.topleft = (random.randrange(GRID_WIDTH) * GRID_SIZE, random.randrange(GRID_HEIGHT) * GRID_SIZE)

    def update(self):
        """
        Update the circle's position.
        """
        self.move_smoothly()

    def move_smoothly(self):
        """
        Move the circle smoothly across the screen.
        """
        direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        new_x = self.rect.x + direction[0] * GRID_SIZE
        new_y = self.rect.y + direction[1] * GRID_SIZE
        if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT:
            self.rect.topleft = (new_x, new_y)


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        for event in pygame.event.get():
            running = game.run(event)
    pygame.quit()
