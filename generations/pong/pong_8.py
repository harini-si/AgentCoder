
import pygame
import sys

WIDTH, HEIGHT = 1000, 1000
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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

        # Bounce off the top and bottom walls
        if self.rect.y <= 0 or self.rect.y >= HEIGHT - self.rect.height:
            self.speed[1] = -self.speed[1]

class PaddleHuman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.centery = HEIGHT // 2  # Position the paddle vertically at the center of the screen
        self.speed = 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

class PaddleCPU(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.right = WIDTH
        self.rect.centery = HEIGHT // 2
        self.speed = 7
        self.game = game

    def update(self):
        if self.game.ball.rect.centery < self.rect.centery and self.rect.top > 0:
            self.rect.y -= self.speed
        if self.game.ball.rect.centery > self.rect.centery and self.rect.bottom < HEIGHT:
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
        self.font = pygame.font.SysFont(None, 36)

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.all_sprites.update()

        if pygame.sprite.collide_rect(self.ball, self.paddle_human) or pygame.sprite.collide_rect(self.ball, self.paddle_cpu):
            self.ball.speed[0] = -self.ball.speed[0]

        if self.ball.rect.left < 0:
            self.score_cpu += 1
            self.ball.rect.center = (WIDTH // 2, HEIGHT // 2)
            self.ball.speed = [5, -5]
        elif self.ball.rect.right > WIDTH:
            self.score_human += 1
            self.ball.rect.center = (WIDTH // 2, HEIGHT // 2)
            self.ball.speed = [5, -5]

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        score_text = self.font.render(f"Human: {self.score_human}  CPU: {self.score_cpu}", True, WHITE)
        self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

        if self.score_human == 5 or self.score_cpu == 5:
            self.game_over = True

        if self.game_over:
            game_over_text = self.font.render("Game Over! Press R to Restart", True, WHITE)
            self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()
        self.clock.tick(FPS)

        if self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.game_over = False
                self.score_human = 0
                self.score_cpu = 0

        return True

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
