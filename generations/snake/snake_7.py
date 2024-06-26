
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

    def run(self, event):
        """
        Implement the main game loop here.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.snake.direction != "RIGHT":
            self.snake.direction = "LEFT"
        elif keys[pygame.K_RIGHT] and self.snake.direction != "LEFT":
            self.snake.direction = "RIGHT"
        elif keys[pygame.K_UP] and self.snake.direction != "DOWN":
            self.snake.direction = "UP"
        elif keys[pygame.K_DOWN] and self.snake.direction != "UP":
            self.snake.direction = "DOWN"

        self.move_snake()
        self.check_collision()
        self.draw()

        return not self.game_over

    def move_snake(self):
        """
        Move the snake in the current direction by one grid unit.
        """
        head_x, head_y = self.snake.body[0]
        if self.snake.direction == "LEFT":
            new_head = (head_x - GRID_SIZE, head_y)
        elif self.snake.direction == "RIGHT":
            new_head = (head_x + GRID_SIZE, head_y)
        elif self.snake.direction == "UP":
            new_head = (head_x, head_y - GRID_SIZE)
        elif self.snake.direction == "DOWN":
            new_head = (head_x, head_y + GRID_SIZE)

        self.snake.body.insert(0, new_head)

    def draw(self):
        """
        Draw the snake, food, and update the display.
        """
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 0, 0), (*self.food.rect.topleft, GRID_SIZE, GRID_SIZE))

        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), (*segment, GRID_SIZE, GRID_SIZE))

        pygame.display.flip()
        self.clock.tick(10)  # Adjust snake speed here

    def check_collision(self):
        """
        Check for collisions with walls, self, and food.
        """
        head = pygame.Rect(*self.snake.body[0], GRID_SIZE, GRID_SIZE)

        # Check if snake collides with itself or hits the wall
        if head.collidelist(self.snake.body[1:]) != -1 or not (0 <= head.x < SCREEN_WIDTH and 0 <= head.y < SCREEN_HEIGHT):
            self.game_over = True
            print("Game Over!")
            self.reset_game()

        # Check if snake eats the food
        if head.colliderect(self.food.rect):
            self.snake.body.append(self.snake.body[-1])  # Increase the snake length
            self.reset_food()
            
    def reset_food(self):
        """
        Reset the location of the food when the snake eats it.
        """
        self.food = Food(random.randint(0, SCREEN_WIDTH - GRID_SIZE), random.randint(0, SCREEN_HEIGHT - GRID_SIZE))

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
