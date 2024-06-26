
import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
GRID_SIZE = 20


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.body = [(500, 500)]
        self.direction = "UP"

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == "UP":
            new_segment = (head_x, head_y - GRID_SIZE)
        elif self.direction == "DOWN":
            new_segment = (head_x, head_y + GRID_SIZE)
        elif self.direction == "LEFT":
            new_segment = (head_x - GRID_SIZE, head_y)
        elif self.direction == "RIGHT":
            new_segment = (head_x + GRID_SIZE, head_y)

        self.body = [new_segment] + self.body[:-1]

    def change_direction(self, new_direction):
        if (new_direction == "UP" and self.direction != "DOWN") or \
           (new_direction == "DOWN" and self.direction != "UP") or \
           (new_direction == "LEFT" and self.direction != "RIGHT") or \
           (new_direction == "RIGHT" and self.direction != "LEFT"):
            self.direction = new_direction


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food(random.randint(0, SCREEN_WIDTH - GRID_SIZE), random.randint(0, SCREEN_HEIGHT - GRID_SIZE))
        self.score = 0

    def check_collision(self):
        if self.snake.body[0] in self.snake.body[1:] or \
           not (0 <= self.snake.body[0][0] < SCREEN_WIDTH and 0 <= self.snake.body[0][1] < SCREEN_HEIGHT):
            self.game_over = True

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.change_direction("UP")
            elif event.key == pygame.K_DOWN:
                self.snake.change_direction("DOWN")
            elif event.key == pygame.K_LEFT:
                self.snake.change_direction("LEFT")
            elif event.key == pygame.K_RIGHT:
                self.snake.change_direction("RIGHT")

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.handle_input(event)

        if not self.game_over:
            self.screen.fill((0, 0, 0))

            self.snake.move()
            self.check_collision()

            if self.snake.body[0] == (self.food.x, self.food.y):
                self.snake.body.append(self.snake.body[-1])
                self.food = Food(random.randint(0, SCREEN_WIDTH - GRID_SIZE), random.randint(0, SCREEN_HEIGHT - GRID_SIZE))
                self.score += 1

            pygame.draw.rect(self.screen, (255, 0, 0), self.food.rect)
            for segment in self.snake.body:
                pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))

            font = pygame.font.Font(None, 36)
            score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))

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

