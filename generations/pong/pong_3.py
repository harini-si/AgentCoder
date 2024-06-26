
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
        self.speed = [5, -5]

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]

class PaddleHuman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.speed = 10

    def update(self, keys):
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

class PaddleCPU(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.speed = 5
        self.game = game

    def update(self):
        if self.rect.centery < self.game.ball.rect.centery:
            self.rect.y += self.speed
        if self.rect.centery > self.game.ball.rect.centery:
            self.rect.y -= self.speed
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.all_sprites = pygame.sprite.Group()
        self.ball = Ball()
        self.paddle_human = PaddleHuman()
        self.paddle_human.rect.midleft = (0, HEIGHT // 2)
        self.paddle_cpu = PaddleCPU(self)
        self.paddle_cpu.rect.midright = (WIDTH, HEIGHT // 2)
        self.all_sprites.add(self.ball, self.paddle_human, self.paddle_cpu)
        self.score_human = 0
        self.score_cpu = 0
        self.font = pygame.font.SysFont(None, 48)

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()
        self.paddle_human.update(keys)
        self.paddle_cpu.update()
        self.ball.update()

        # Handle ball collisions with paddles
        if pygame.sprite.collide_rect(self.ball, self.paddle_human) or pygame.sprite.collide_rect(self.ball, self.paddle_cpu):
            self.ball.speed[0] = -self.ball.speed[0]

        # Detect scoring
        if self.ball.rect.right >= WIDTH:
            self.score_human += 1
            self.ball.rect.x = WIDTH // 2
            self.ball.rect.y = HEIGHT // 2
            self.ball.speed = [5, -5]
        elif self.ball.rect.left <= 0:
            self.score_cpu += 1
            self.ball.rect.x = WIDTH // 2
            self.ball.rect.y = HEIGHT // 2
            self.ball.speed = [-5, 5]

        self.screen.fill(BLACK)
        pygame.draw.line(self.screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
        self.all_sprites.draw(self.screen)

        score_text = self.font.render(f'Human: {self.score_human} / CPU: {self.score_cpu}', True, WHITE)
        self.screen.blit(score_text, (WIDTH // 2 + 10, 10))

        if self.score_human >= SCORE_LIMIT or self.score_cpu >= SCORE_LIMIT:
            self.game_over = True
            self.score_human = 0
            self.score_cpu = 0

        if self.game_over:
            game_over_text = self.font.render('Game Over!', True, WHITE)
            self.screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
            restart_text = self.font.render('Press any key to restart.', True, WHITE)
            self.screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))

            if any(keys):
                self.game_over = False

        pygame.display.flip()
        self.clock.tick(FPS)

        return not self.game_over

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
