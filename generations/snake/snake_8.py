
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
        self.length = 1
        self.rect = pygame.Rect(self.body[0][0], self.body[0][1], GRID_SIZE, GRID_SIZE)

    def update(self):
        """
        Update the snake's position based on direction.
        """
        if self.direction == "UP":
            self.rect.y -= GRID_SIZE
        elif self.direction == "DOWN":
            self.rect.y += GRID_SIZE
        elif self.direction == "LEFT":
            self.rect.x -= GRID_SIZE
        elif self.direction == "RIGHT":
            self.rect.x += GRID_SIZE

        # Update the body positions
        self.body.insert(0, (self.rect.x, self.rect.y))
        if len(self.body) > self.length:
            self.body.pop()

    def turn(self, direction):
        """
        Change the snake's direction without going directly backward.
        """
        if direction == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        elif direction == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        elif direction == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif direction == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

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
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)

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
        self.food = Food(random.randint(0, SCREEN_WIDTH - GRID_SIZE), random.randint(0, SCREEN_HEIGHT - GRID_SIZE))
        self.score = 0

    def check_collision(self):
        """
        Check for collisions between the snake, food, and game boundaries.
        """
        if self.snake.rect.colliderect(self.food.rect): # Snake eats the food
            self.score += 1
            self.snake.length += 1
            self.food = Food(random.randint(0, SCREEN_WIDTH - GRID_SIZE), random.randint(0, SCREEN_HEIGHT - GRID_SIZE))

        if self.snake.rect.left < 0 or self.snake.rect.right > SCREEN_WIDTH or self.snake.rect.top < 0 or self.snake.rect.bottom > SCREEN_HEIGHT:
            self.game_over = True

        for segment in self.snake.body[1:]:
            if self.snake.rect.collidepoint(segment):
                self.game_over = True

    def run(self, event):
        """
        Implement the main game loop.
        """
        if not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.turn("UP")
                    elif event.key == pygame.K_DOWN:
                        self.snake.turn("DOWN")
                    elif event.key == pygame.K_LEFT:
                        self.snake.turn("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        self.snake.turn("RIGHT")

            self.snake.update()
            self.check_collision()            

            self.screen.fill((0, 0, 0))

            # Draw the snake
            for segment in self.snake.body:
                pygame.draw.rect(self.screen, (0, 255, 0), (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

            # Draw the food
            pygame.draw.rect(self.screen, (255, 0, 0), (self.food.rect.x, self.food.rect.y, GRID_SIZE, GRID_SIZE))

            # Display the score
            font = pygame.font.Font(None, 36)
            score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(10)  # Set the snake's speed

        else:
            self.screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 100)
            game_over_text = font.render("Game Over!", True, (255, 255, 255))
            restart_text = font.render("Press R to Restart", True, (255, 255, 255))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.game_over = False

        return True

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        running = game.run(event)

    pygame.quit()
