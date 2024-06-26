
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
        self.spawn_circle(GREEN, "green")
        self.spawn_circle(RED, "red")

    def spawn_circle(self, color, circle_type):
        """
        Spawn a circle with the given color on the game grid.
        Ensure no collision with existing sprites.
        """
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if not any(circle.rect.topleft == (x, y) for circle in self.circles):
                circle = Circle(color, circle_type)
                circle.rect.topleft = (x, y)
                self.circles.add(circle)
                break

    def update_circles(self):
        """
        Update circles based on collisions with the agent.
        Update score accordingly.
        """
        for circle in pygame.sprite.spritecollide(self.agent, self.circles, True):
            if circle.color == GREEN:
                self.score += 1
            else:
                self.score -= 1

            self.spawn_circle(GREEN if circle.color == GREEN else RED, "respawn")

    def reset_game(self):
        """
        Reset the game state.
        """
        self.game_over = False
        self.score = 0
        self.spawn_initial_circles()

    def handle_events(self, event):
        """
        Handle game events, including quitting and restarting the game.
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if self.game_over:
                self.reset_game()

    def render_game(self):
        """
        Render the game screen, including sprites and score.
        Display game over or win messages as needed.
        """
        self.screen.fill(WHITE)
        self.agent.update()
        self.circles.update()

        self.circles.draw(self.screen)
        self.screen.blit(self.agent.image, self.agent.rect.topleft)

        score_text = self.font.render("Score: " + str(self.score), True, BLUE)
        self.screen.blit(score_text, (10, 10))

        if len([circle for circle in self.circles if circle.color == GREEN]) == 0:
            self.show_message("Game Over!", 72)
            self.game_over = True

    def show_message(self, message, size=36):
        """
        Display a message on the screen.
        """
        text = self.font.render(message, True, BLUE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def run(self, event):
        """
        Main game loop.
        """
        self.handle_events(event)
        self.update_circles()
        self.render_game()

        pygame.display.flip()
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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= GRID_SIZE
        if keys[pygame.K_DOWN]:
            self.rect.y += GRID_SIZE
        if keys[pygame.K_LEFT]:
            self.rect.x -= GRID_SIZE
        if keys[pygame.K_RIGHT]:
            self.rect.x += GRID_SIZE

    def update(self):
        """
        Update method for the agent (unused in this example).
        """
        self.move(pygame.key.get_pressed())


class Circle(pygame.sprite.Sprite):
    def __init__(self, color, circle_type):
        """
        Initialize a circle sprite with a specified color and type.
        """
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        if circle_type == "green":
            pygame.draw.circle(self.image, GREEN, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        elif circle_type == "red":
            pygame.draw.circle(self.image, RED, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)

    def reset(self):
        """
        Reset the circle's position and direction.
        """
        pass

    def update(self):
        """
        Update the circle's position.
        """
        self.move_smoothly()

    def move_smoothly(self):
        """
        Move the circle smoothly across the screen.
        """
        self.rect.x += random.choice([-GRID_SIZE, 0, GRID_SIZE])
        self.rect.y += random.choice([-GRID_SIZE, 0, GRID_SIZE])


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            running = game.run(event)

    pygame.quit()
