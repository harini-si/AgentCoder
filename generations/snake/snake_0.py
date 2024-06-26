
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

        self.length = 1
        self.rect = pygame.Rect(self.body[0][0], self.body[0][1], GRID_SIZE, GRID_SIZE)


class Food(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None):
        """
        Initialize the food's position and image.
        self.x and self.y should be the top-left coordinate of the food
        self.rect should be a pygame.Rect object with the initial position of the food
        """
        super().__init__()
        if x is None:
            self.x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE - 1)) * GRID_SIZE
        else:
            self.x = x

        if y is None:
            self.y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE - 1)) * GRID_SIZE
        else:
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
        pygame.display.set_caption("Snake Game")
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
        self.food = Food()

        self.score = 0

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (200, 200, 200), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (200, 200, 200), (0, y), (SCREEN_WIDTH, y))

    def check_collision(self):
        if self.snake.rect.collidelistall([pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE) for segment in self.snake.body[1:]]):
            self.game_over = True

        if self.snake.rect.left < 0 or self.snake.rect.right > SCREEN_WIDTH or self.snake.rect.top < 0 or self.snake.rect.bottom > SCREEN_HEIGHT:
            self.game_over = True

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.snake.direction != "DOWN":
            self.snake.direction = "UP"
        if keys[pygame.K_DOWN] and self.snake.direction != "UP":
            self.snake.direction = "DOWN"
        if keys[pygame.K_LEFT] and self.snake.direction != "RIGHT":
            self.snake.direction = "LEFT"
        if keys[pygame.K_RIGHT] and self.snake.direction != "LEFT":
            self.snake.direction = "RIGHT"

        if not self.game_over:
            self.snake.body.insert(0, tuple(sum(e) for e in zip(self.snake.body[0], (-1 if self.snake.direction == "LEFT" else 1 if self.snake.direction == "RIGHT" else 0) * GRID_SIZE, (-1 if self.snake.direction == "UP" else  1 if self.snake.direction == "DOWN" else 0) * GRID_SIZE)))

            if self.snake.body[0][0] == self.food.x and self.snake.body[0][1] == self.food.y:
                self.score += 1
                self.food = Food()
            else:
                self.snake.body.pop()

            self.snake.rect = pygame.Rect(self.snake.body[0][0], self.snake.body[0][1], GRID_SIZE, GRID_SIZE)

            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.screen.fill((255, 255, 255), self.snake.rect)
            self.screen.fill((255, 0, 0), self.food.rect)

            self.check_collision()

            pygame.display.flip()
            self.clock.tick(15)

        return not self.game_over


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            running = game.run(event)
    pygame.quit()
