
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
        Initialize the snake's body, direction and image.
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
        # Move the rest of the body segments to follow the head
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = self.body[i - 1]

        # Move the head in the current direction
        x, y = self.body[0]
        if self.direction == "UP":
            y -= GRID_SIZE
        elif self.direction == "DOWN":
            y += GRID_SIZE
        elif self.direction == "LEFT":
            x -= GRID_SIZE
        elif self.direction == "RIGHT":
            x += GRID_SIZE

        self.body[0] = (x, y)


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        Initialize the food's position and image.
        self.x and self.y should be the top-left coordinate of the food
        self.rect should be a pygame.Rect object with the initial position of the food
        """
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)


class Game:
    """
    The main class for the Snake game.
    """
    def __init__(self):
        """
        Initialize the game and its components.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        """
        Reset the game to its initial state.
        self.game_over is a boolean representing whether the game is over
        self.snake is a Snake object representing the snake character
        self.food is a Food object representing the active food item (randomize the food location)
        self.score is an integer representing the player's score
        """
        self.game_over = False
        self.snake = Snake()
        self.food = Food(
            random.randint(0, (SCREEN_WIDTH // GRID_SIZE - 1)) * GRID_SIZE,
            random.randint(0, (SCREEN_HEIGHT // GRID_SIZE - 1)) * GRID_SIZE
        )
        self.score = 0

    def check_collision(self):
        """
        Check for collisions between the snake and food, snake itself, or window boundaries.
        """
        # Check if snake has collided with the food
        if self.snake.body[0] == (self.food.x, self.food.y):
            self.snake.body.append(self.snake.body[-1])
            self.score += 1
            self.food = Food(
                random.randint(0, (SCREEN_WIDTH // GRID_SIZE - 1)) * GRID_SIZE,
                random.randint(0, (SCREEN_HEIGHT // GRID_SIZE - 1)) * GRID_SIZE
            )

        # Check if snake has collided with itself
        if len(self.snake.body) != len(set(self.snake.body)):
            self.game_over = True

        # Check if snake has collided with window boundaries
        if (
            self.snake.body[0][0] < 0 or
            self.snake.body[0][0] >= SCREEN_WIDTH or
            self.snake.body[0][1] < 0 or
            self.snake.body[0][1] >= SCREEN_HEIGHT
        ):
            self.game_over = True

    def draw_elements(self):
        """
        Draw the snake, food, and score on the screen.
        """
        # Clear the screen
        self.screen.fill((0, 0, 0))

        # Draw the snake
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))

        # Draw the food
        pygame.draw.rect(self.screen, (255, 0, 0), self.food.rect)

        # Draw the score
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

    def run(self, event):
        """
        Main game loop.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != "DOWN":
                    self.snake.direction = "UP"
                elif event.key == pygame.K_DOWN and self.snake.direction != "UP":
                    self.snake.direction = "DOWN"
                elif event.key == pygame.K_LEFT and self.snake.direction != "RIGHT":
                    self.snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and self.snake.direction != "LEFT":
                    self.snake.direction = "RIGHT"

        if not self.game_over:
            self.snake.move()
            self.check_collision()
            self.draw_elements()
            self.clock.tick(15)

        return not self.game_over


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run(pygame.event.poll())
    pygame.quit()
