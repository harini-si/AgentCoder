
import pygame
import sys

WIDTH, HEIGHT = 1000, 1000
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCORE_LIMIT = 5

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.speed = [5, -5]  # Initial speed of the ball

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        # Bounce the ball off walls
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]

    def reverse_speed(self):
        self.speed[0] = -self.speed[0]

class PaddleHuman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (30, HEIGHT // 2)  # Position the paddle on the left side
        self.speed = 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

class PaddleCPU(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - 30, HEIGHT // 2)  # Position the paddle on the right side
        self.speed = 5
        self.game = game

    def update(self):
        if self.game.ball.rect.top < self.rect.y:
            self.rect.y -= self.speed
        if self.game.ball.rect.bottom > self.rect.y:
            self.rect.y += self.speed

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.all_sprites = pygame.sprite.Group()
        self.ball = Ball()
        self.paddle_human = PaddleHuman()
        self.paddle_cpu = PaddleCPU(self)
        self.all_sprites.add(self.ball, self.paddle_human, self.paddle_cpu)
        self.score_human = 0
        self.score_cpu = 0
        self.font = pygame.font.Font(None, 36)
        
    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        self.all_sprites.update()

        # Check collision with paddles
        if pygame.sprite.spritecollide(self.ball, [self.paddle_human, self.paddle_cpu], False):
            self.ball.reverse_speed()

        # Check if the ball is missed by the paddles
        if self.ball.rect.right > WIDTH:
            self.score_human += 1
            self.ball.rect.x = WIDTH // 2
            self.ball.rect.y = HEIGHT // 2
            self.ball.speed = [5, -5]

        if self.ball.rect.left < 0:
            self.score_cpu += 1
            self.ball.rect.x = WIDTH // 2
            self.ball.rect.y = HEIGHT // 2
            self.ball.speed = [5, -5]

        self.screen.fill(BLACK)
        pygame.draw.line(self.screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)
        self.all_sprites.draw(self.screen)

        # Display scores
        text = self.font.render(f"Human: {self.score_human} CPU: {self.score_cpu}", True, WHITE)
        self.screen.blit(text, (10, 10))

        if self.score_human >= SCORE_LIMIT or self.score_cpu >= SCORE_LIMIT:
            self.game_over = True
            self.score_human = 0
            self.score_cpu = 0

        if self.game_over:
            font = pygame.font.SysFont(None, 100)
            text = font.render("Game Over!", True, WHITE)
            self.screen.blit(text, (WIDTH//2 - text.get_rect().width//2, HEIGHT//2 - text.get_rect().height//2))

            pygame.display.flip()
            pygame.time.delay(2000)
            self.game_over = False

        pygame.display.flip()
        self.clock.tick(FPS)

        return True

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run(pygame.event.get())
    pygame.quit()
