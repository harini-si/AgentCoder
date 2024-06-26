
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
        for _ in range((WIDTH // GRID_SIZE) // 2):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)
        
    def spawn_circle(self, color):
        """
        Spawn a circle with the given color on the game grid.
        Ensure no collision with existing sprites.
        """
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if not any(circle.rect.topleft == (x, y) for circle in self.circles):
                new_circle = Circle(color)
                new_circle.rect.topleft = x, y
                self.circles.add(new_circle)
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
            else:
                self.score -= 1
            self.spawn_circle(random.choice([GREEN, RED]))

        if all(circle.color == RED for circle in self.circles):
            self.game_over = True

    def reset_game(self):
        """
        Reset the game state.
        """
        self.score = 0
        self.game_over = False
        self.agent.reset()
        self.circles.empty()
        self.spawn_initial_circles()

    def handle_events(self, event):
        """
        Handle game events, including quitting and restarting the game.
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if self.game_over:
                self.reset_game()
            if event.key == pygame.K_UP:
                self.agent.move("up")
            elif event.key == pygame.K_DOWN:
                self.agent.move("down")
            elif event.key == pygame.K_LEFT:
                self.agent.move("left")
            elif event.key == pygame.K_RIGHT:
                self.agent.move("right")

    def render_game(self):
        """
        Render the game screen, including sprites and score.
        Display game over or win messages as needed.
        """
        self.screen.fill(WHITE)
        self.circles.update()
        self.agent.update()
        self.circles.draw(self.screen)
        self.screen.blit(self.agent.image, self.agent.rect)
        score_text = self.font.render(f"Score: {self.score}", True, BLUE)
        self.screen.blit(score_text, (10, 10))
        if self.game_over:
            self.show_message("Game Over!")
        

    def show_message(self, message, size=36):
        """
        Display a message on the screen.
        """
        text = pygame.font.Font(None, size).render(message, True, BLUE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

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

    def move(self, direction):
        """
        Move the agent in the specified direction.
        """
        if direction == "up":
            self.rect.y -= GRID_SIZE
        elif direction == "down":
            self.rect.y += GRID_SIZE
        elif direction == "left":
            self.rect.x -= GRID_SIZE
        elif direction == "right":
            self.rect.x += GRID_SIZE
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def update(self):
        """
        Update method for the agent (unused in this example).
        """
        pass


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        """
        Initialize a circle sprite with a specified color and direction.
        """
        super().__init__()
        self.color = color
        self.image = pygame.Surface(
            (CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(self.image, color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()

    def move_smoothly(self):
        """
        Move the circle smoothly across the screen.
        """
        self.rect.x += random.randint(-GRID_SIZE, GRID_SIZE)
        self.rect.y += random.randint(-GRID_SIZE, GRID_SIZE)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


if __name__ == "__main__":
    game = Game()
    while True:
        event = pygame.event.poll()
        if game.run(event) == False:
            break
    pygame.quit()
