
import pygame
import sys

WIDTH, HEIGHT = 1000, 1000
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initializes the Ball instance.
        image: Surface representing the ball
        rect: Rect object representing the ball's position and size
        speed: A list containing the speed of the ball in x and y directions (e.g. [5, -5])
        """
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.speed = [5, -5]

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]

class PaddleHuman(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initializes the human-controlled paddle.
        image: Surface representing the paddle
        rect: Rect object representing the paddle's position and size
        speed: Integer representing the paddle's movement speed
        """
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centery = HEIGHT // 2
        self.rect.left = 10
        self.speed = 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

class PaddleCPU(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initializes the CPU-controlled paddle.
        image: Surface representing the paddle
        rect: Rect object representing the paddle's position and size
        speed: An integer representing the paddle's movement speed
        """
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centery = HEIGHT // 2
        self.rect.right = WIDTH - 10
        self.speed = 5

    def update(self, ball):
        if ball.rect.centery < self.rect.centery:
            self.rect.y -= self.speed
        elif ball.rect.centery > self.rect.centery:
            self.rect.y += self.speed
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

class Game:
    def __init__(self):
        """
        Initializes the game.
        screen: Pygame display surface
        clock: Pygame Clock object for controlling frame rate
        game_over: Boolean representing whether the game is over
        all_sprites: Pygame group containing all sprites in the game
        ball: Ball object
        paddle_human: Human-controlled paddle object
        paddle_cpu: CPU-controlled paddle object
        score_human: An integer representing the human player's score
        score_cpu: An integer representing the CPU player's score
        font: Pygame font object for rendering text
        """

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.all_sprites = pygame.sprite.Group()
        self.ball = Ball()
        self.paddle_human = PaddleHuman()
        self.paddle_cpu = PaddleCPU()
        self.all_sprites.add(self.ball, self.paddle_human, self.paddle_cpu)
        self.score_human = 0
        self.score_cpu = 0
        self.font = pygame.font.SysFont(None, 50)

    def run(self, event):
        """
        Runs the game loop.
        event: Pygame event object
        Returns: Boolean indicating whether to continue running the game
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        self.all_sprites.update()

        if pygame.sprite.collide_rect(self.ball, self.paddle_human):
            self.ball.speed[0] = -self.ball.speed[0]
        if pygame.sprite.collide_rect(self.ball, self.paddle_cpu):
            self.ball.speed[0] = -self.ball.speed[0]

        if self.ball.rect.left <= 0:
            self.score_cpu += 1
            self.ball.rect.center = (WIDTH//2, HEIGHT//2)

        if self.ball.rect.right >= WIDTH:
            self.score_human += 1
            self.ball.rect.center = (WIDTH//2, HEIGHT//2)

        if self.score_human == 5 or self.score_cpu == 5:
            self.game_over = True

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        score_text = self.font.render(f"Human: {self.score_human}   CPU: {self.score_cpu}", True, WHITE)
        self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 10))

        if self.game_over:
            game_over_text = self.font.render("Game Over!", True, WHITE)
            self.screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2))
            restart_text = self.font.render("Press R to restart", True, WHITE)
            self.screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.__init__()

        pygame.display.flip()
        self.clock.tick(FPS)
        return True

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
