
import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
# Define the size of each grid unit / snake's body segment
# every time the snake moves, it should move by this amount
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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
        self.food = self.generate_food()
        self.score = 0

    def generate_food(self):
        """
        Generate a new food item at a random location on the grid.
        """
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return Food(x, y)

    def draw_grid(self):
        """
        Draw grid lines on the game screen for better visualization.
        """
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (255, 255, 255), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (255, 255, 255), (0, y), (SCREEN_WIDTH, y))

    def check_collision(self):
        """
        Check for collision - with itself or boundaries of the game window.
        """
        head = self.snake.body[0]
        
        if head in self.snake.body[1:] or head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
            self.game_over = True

    def update_score(self):
        """
        Update the score when the snake consumes food.
        """
        self.score += 10

    def draw_score(self):
        """
        Display the current score on the game screen.
        """
        font = pygame.font.SysFont(None, 36)
        score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def run(self, event):
        """
        Implement the main game loop here.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.snake.direction != "RIGHT":
            self.snake.direction = "LEFT"
        if keys[pygame.K_RIGHT] and self.snake.direction != "LEFT":
            self.snake.direction = "RIGHT"
        if keys[pygame.K_UP] and self.snake.direction != "DOWN":
            self.snake.direction = "UP"
        if keys[pygame.K_DOWN] and self.snake.direction != "UP":
            self.snake.direction = "DOWN"

        head = self.snake.body[0]
        if self.snake.direction == "LEFT":
            new_head = (head[0] - GRID_SIZE, head[1])
        elif self.snake.direction == "RIGHT":
            new_head = (head[0] + GRID_SIZE, head[1])
        elif self.snake.direction == "UP":
            new_head = (head[0], head[1] - GRID_SIZE)
        else:
            new_head = (head[0], head[1] + GRID_SIZE)

        self.snake.body.insert(0, new_head)

        if new_head[0] == self.food.x and new_head[1] == self.food.y:
            self.snake.body.append((self.food.x, self.food.y))
            self.food = self.generate_food()
            self.update_score()
        else:
            self.snake.body.pop()

        self.check_collision()

        self.screen.fill((0, 0, 0))
        self.draw_grid()

        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))

        pygame.draw.rect(self.screen, (255, 0, 0), self.food.rect)

        self.draw_score()
        
        pygame.display.flip()
        
        self.clock.tick(10)

        if self.game_over:
            self.reset_game()

        return True

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run(pygame.event.poll())
