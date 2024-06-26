
import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
# Define the size of each grid unit / snake's body segment
# every time the snake moves, it should move by this amount
GRID_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

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
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        """
        Reset the game to its initial state.
        self.game_over is a boolean representing whether the game is over
        self.snake is a Snake object representing the snake character
        self.food is a Food object representing the active food item (randomize the food location)
        """
        self.game_over = False
        self.snake = Snake()
        self.food = Food(random.randint(0, SCREEN_WIDTH - GRID_SIZE), random.randint(0, SCREEN_HEIGHT - GRID_SIZE))

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, WHITE, (0, y), (SCREEN_WIDTH, y))

    def draw_score(self, score):
        font = pygame.font.SysFont(None, 36)
        score_text = font.render("Score: " + str(score), True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def check_collision(self):
        if self.snake.body[0] in self.snake.body[1:] or not (0 <= self.snake.body[0][0] < SCREEN_WIDTH and 0 <= self.snake.body[0][1] < SCREEN_HEIGHT):
            self.game_over = True

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if self.game_over:
            self.screen.fill(RED)
            font = pygame.font.SysFont(None, 72)
            game_over_text = font.render("Game Over!", True, WHITE)
            restart_text = font.render("Press R to restart", True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.reset_game()
                self.game_over = False

        else:
            self.screen.fill((0, 0, 0))
            self.draw_grid()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.snake.direction != "DOWN":
                self.snake.direction = "UP"
            elif keys[pygame.K_DOWN] and self.snake.direction != "UP":
                self.snake.direction = "DOWN"
            elif keys[pygame.K_LEFT] and self.snake.direction != "RIGHT":
                self.snake.direction = "LEFT"
            elif keys[pygame.K_RIGHT] and self.snake.direction != "LEFT":
                self.snake.direction = "RIGHT"

            x, y = self.snake.body[0]
            if self.snake.direction == "UP":
                y -= GRID_SIZE
            elif self.snake.direction == "DOWN":
                y += GRID_SIZE
            elif self.snake.direction == "LEFT":
                x -= GRID_SIZE
            elif self.snake.direction == "RIGHT":
                x += GRID_SIZE

            new_head = (x, y)
            self.snake.body.insert(0, new_head)

            if self.snake.body[0] == (self.food.x, self.food.y):
                self.food = Food(random.randint(0, SCREEN_WIDTH - GRID_SIZE), random.randint(0, SCREEN_HEIGHT - GRID_SIZE))
            else:
                self.snake.body.pop()

            self.screen.fill(GREEN, rect=self.food.rect)
            for segment in self.snake.body:
                pygame.draw.rect(self.screen, WHITE, pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))

            self.draw_score(len(self.snake.body) - 1)
            self.check_collision()

        pygame.display.flip()
        self.clock.tick(10)
        return True

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
