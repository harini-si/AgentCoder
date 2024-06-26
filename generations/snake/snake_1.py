

import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
# Define the size of each grid unit / snake's body segment
# every time the snake moves, it should move by this amount
GRID_SIZE = 20


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the snake's body, direction, and image.
        self.body should be a list of tuples representing the snake's body segments (top-left coordinates)
        self.direction should be one of {"UP", "DOWN", "LEFT", "RIGHT"}
        self.length should be an integer representing the length of the snake
        self.rect should be a pygame.Rect object with the head position of the snake
        """
        super().__init__()
        self.body = [(500, 500)]
        self.direction = "UP"

    def move(self):
        """
        Move the snake in the current direction by one grid unit.
        """
        head_x, head_y = self.body[0]
        if self.direction == "UP":
            new_head = (head_x, head_y - GRID_SIZE)
        elif self.direction == "DOWN":
            new_head = (head_x, head_y + GRID_SIZE)
        elif self.direction == "LEFT":
            new_head = (head_x - GRID_SIZE, head_y)
        elif self.direction == "RIGHT":
            new_head = (head_x + GRID_SIZE, head_y)
        self.body = [new_head] + self.body[:-1]

class Food(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the food's position and image.
        self.x and self.y should be the top-left coordinate of the food
        self.rect should be a pygame.Rect object with the initial position of the food
        """
        super().__init__()
        self.x = 0
        self.y = 0
        self.randomize_position()

    def randomize_position(self):
        """
        Update the food's position to a random location on the grid.
        """
        self.x = random.randrange(0, SCREEN_WIDTH, GRID_SIZE)
        self.y = random.randrange(0, SCREEN_HEIGHT, GRID_SIZE)
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)


class Game:
    """
    The main class for the Snake game.
    """
    def __init__(self):
        """
        Initialize the game and its components.
        """
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        """
        Reset the game to its initial state.
        self.game_over is a boolean representing whether the game is over
        self.score is an integer representing the player's current score
        self.snake is a Snake object representing the snake character
        self.food is a Food object representing the active food item (randomize the food location)
        """
        self.game_over = False
        self.score = 0
        self.snake = Snake()
        self.food = Food()

    def check_collision(self):
        """
        Check for collisions between the snake and the food or boundaries.
        """
        if self.snake.body[0] == (self.food.x, self.food.y):
            self.snake.body.append(self.snake.body[-1])
            self.food.randomize_position()
            self.score += 1

        if (
            self.snake.body[0][0] < 0
            or self.snake.body[0][0] >= SCREEN_WIDTH
            or self.snake.body[0][1] < 0
            or self.snake.body[0][1] >= SCREEN_HEIGHT
            or self.snake.body[0] in self.snake.body[1:]
        ):
            self.game_over = True

    def handle_input(self, event):
        """
        Handle user input to change the snake's direction.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.snake.direction != "DOWN":
                self.snake.direction = "UP"
            elif event.key == pygame.K_DOWN and self.snake.direction != "UP":
                self.snake.direction = "DOWN"
            elif event.key == pygame.K_LEFT and self.snake.direction != "RIGHT":
                self.snake.direction = "LEFT"
            elif event.key == pygame.K_RIGHT and self.snake.direction != "LEFT":
                self.snake.direction = "RIGHT"

    def draw_text(self, text, size, color, x, y):
        """
        Helper method to draw text on the screen.
        """
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def run(self, event):
        """
        Main game loop handling events, updates, and rendering.
        Returns False when the game should exit.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.reset_game()
                    self.game_over = False

            if not self.game_over:
                self.handle_input(event)

        if not self.game_over:
            self.snake.move()
            self.check_collision()

        self.screen.fill((0, 0, 0))

        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))

        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.food.x, self.food.y, GRID_SIZE, GRID_SIZE))

        self.draw_text(f"Score: {self.score}", 36, (255, 255, 255), 10, 10)

        if self.game_over:
            self.draw_text("Game Over!", 72, (255, 0, 0), SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2)
            self.draw_text("Press Enter to Restart", 36, (255, 255, 255), SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50)

        pygame.display.flip()
        self.clock.tick(10)

        return True


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        running = game.run(pygame.event.poll())
    pygame.quit()

