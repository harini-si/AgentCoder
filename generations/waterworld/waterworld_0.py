

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
        for _ in range(GRID_WIDTH * GRID_HEIGHT // 40):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        """
        Spawn a circle with the given color on the game grid.
        Ensure no collision with existing sprites.
        """
        while True:
            x = random.randrange(GRID_WIDTH) * GRID_SIZE
            y = random.randrange(GRID_HEIGHT) * GRID_SIZE
            circle = Circle(color)
            circle.rect.topleft = (x, y)
            if not pygame.sprite.spritecollide(circle, self.circles, False):
                self.circles.add(circle)
                break

    def update_circles(self):
        """
        Update circles based on collisions with the agent.
        Update score accordingly.
        """
        collisions = pygame.sprite.spritecollide(self.agent, self.circles, True)
        for circle in collisions:
            if circle.color == GREEN:
                self.score += 1
            elif circle.color == RED:
                self.score -= 1

            if circle.color == GREEN:  # Respawn if a green circle is captured
                self.spawn_circle(random.choice([GREEN, RED]))

    def reset_game(self):
        """
        Reset the game state.
        """
        self.score = 0
        self.agent.reset()
        self.circles.empty()
        self.spawn_initial_circles()
        self.game_over = False

    def handle_events(self, event):
        """
        Handle game events, including quitting and restarting the game.
        """
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()
        return True

    def render_game(self):
        """
        Render the game screen, including sprites and score.
        Display game over or win messages as needed.
        """
        self.screen.fill(WHITE)
        self.circles.update()
        self.circles.draw(self.screen)
        self.agent.update()
        self.agent.move()
        self.screen.blit(self.agent.image, self.agent.rect)

        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLUE)
        self.screen.blit(score_text, (10, 10))

        if not any(circle.color == GREEN for circle in self.circles):
            self.game_over = True
            self.show_message("Game Over! Press 'R' to restart.")

        if self.game_over:
            self.show_message("Game Over! Press 'R' to restart.")

        pygame.display.flip()

    def show_message(self, message, size=36):
        """
        Display a message on the screen.
        """
        font = pygame.font.SysFont(None, size)
        text = font.render(message, True, BLUE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def run(self, event):
        """
        Main game loop.
        """
        for event in pygame.event.get():
            if not self.handle_events(event):
                return False

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

    def move(self):
        """
        Move the agent based on arrow key input.
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

        self.rect.x = max(0, min(self.rect.x, WIDTH - GRID_SIZE))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - GRID_SIZE))

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
        pygame.draw.circle(self.image, color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()

    def reset(self):
        """
        Reset the circle's position and direction.
        """
        self.rect.topleft = (
            random.randrange(GRID_WIDTH) * GRID_SIZE,
            random.randrange(GRID_HEIGHT) * GRID_SIZE,
        )

    def update(self):
        """
        Update the circle's position.
        """
        self.move_smoothly()

    def move_smoothly(self):
        """
        Move the circle smoothly across the screen.
        """
        self.rect.x += random.randint(-1, 1) * GRID_SIZE
        self.rect.x = max(0, min(self.rect.x, WIDTH - GRID_SIZE))
        self.rect.y += random.randint(-1, 1) * GRID_SIZE
        self.rect.y = max(0, min(self.rect.y, HEIGHT - GRID_SIZE))


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run(pygame.event.poll())
    pygame.quit()

