
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

    def move(self):
        """
        Move the snake in the current direction by one grid unit
        """
        x, y = self.body[0]
        if self.direction == "UP":
            y -= GRID_SIZE
        elif self.direction == "DOWN":
            y += GRID_SIZE
        elif self.direction == "LEFT":
            x -= GRID_SIZE
        elif self.direction == "RIGHT":
            x += GRID_SIZE

        self.body.insert(0, (x, y))
        self.rect = pygame.Rect(self.body[0][0], self.body[0][1], GRID_SIZE, GRID_SIZE)

    def check_collision(self):
        """
        Check if the snake collides with itself or hits the game window boundaries
        """
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH or self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            return True

        if len(self.body) != len(set(self.body)):  # Collision with itself
            return True

        return False


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

    def respawn(self):
        """
        Move the food to a random position within the game window
        """
        self.x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        self.rect.topleft = (self.x, self.y)


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
        self.score is an integer representing the player's score
        """
        self.game_over = False
        self.snake = Snake()
        self.food = Food(random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                         random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)
        self.score = 0

    def run(self, event):
        """
        Implement the main game loop here.
        """
        if event.type == pygame.QUIT:
            return False

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

            self.snake.move()

            if self.snake.rect.colliderect(self.food.rect):
                self.snake.length += 1
                self.score += 1
                self.food.respawn()

            if self.snake.check_collision():
                self.game_over = True

        self.screen.fill((0, 0, 0))

        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))

        pygame.draw.rect(self.screen, (255, 0, 0), self.food.rect)

        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            font = pygame.font.Font(None, 72)
            text = font.render("Game Over!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)

        pygame.display.flip()
        self.clock.tick(10)

        return True


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        for event in pygame.event.get():
            running = game.run(event)
    pygame.quit()
