
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

        # Load snake image
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill((0, 255, 0))  # Green color for the snake
        self.rect = self.image.get_rect(topleft=self.body[0])

    def update(self):
        """
        Update the position of the snake's body segments
        """
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = self.body[i - 1]
        self.body[0] = self.rect.topleft

    def grow(self):
        """
        Increase the length of the snake when it eats food
        """
        self.body.append((-20, -20))  # Temporary position


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

        # Load food image
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill((255, 0, 0))  # Red color for the food
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


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
        self.food = Food(random.randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                         random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE)
        self.score = 0

    def run(self, event):
        """
        Implement the main game loop here.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if not self.game_over:
            if keys[pygame.K_UP] and self.snake.direction != "DOWN":
                self.snake.direction = "UP"
            elif keys[pygame.K_DOWN] and self.snake.direction != "UP":
                self.snake.direction = "DOWN"
            elif keys[pygame.K_LEFT] and self.snake.direction != "RIGHT":
                self.snake.direction = "LEFT"
            elif keys[pygame.K_RIGHT] and self.snake.direction != "LEFT":
                self.snake.direction = "RIGHT"

            # Update snake position
            self.snake.update()
        
            # Check for collision with walls and itself
            if (self.snake.rect.left < 0 or self.snake.rect.right > SCREEN_WIDTH or
                    self.snake.rect.top < 0 or self.snake.rect.bottom > SCREEN_HEIGHT or
                    any(segment == self.snake.rect.topleft for segment in self.snake.body[1:])):
                self.game_over = True

            # Check if snake eats food
            if self.snake.rect.colliderect(self.food.rect):
                self.snake.grow()
                self.food = Food(random.randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                                 random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE)
                self.score += 1

        # Draw everything on the screen
        self.screen.fill((0, 0, 0))  # Black background
        self.screen.blit(self.food.image, self.food.rect)
        for segment in self.snake.body:
            self.screen.blit(self.snake.image, pygame.Rect(segment, (GRID_SIZE, GRID_SIZE)))

        # Display score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))  # White color for score
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(10)  # Adjust snake speed by changing the tick value

        return self.game_over


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run(pygame.event.poll())
    pygame.quit()

