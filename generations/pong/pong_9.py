
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
        if self.rect.y <= 0 or self.rect.y >= HEIGHT - 20:
            self.speed[1] = -self.speed[1]

class PaddleHuman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (20, HEIGHT // 2)
        self.speed = 10

    def update(self, keys):
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < HEIGHT - 100:
            self.rect.y += self.speed

class PaddleCPU(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - 20, HEIGHT // 2)
        self.speed = 5
        self.game = game

    def update(self):
        # CPU AI to track the ball
        if self.rect.centery < self.game.ball.rect.centery:
            self.rect.y += self.speed
        if self.rect.centery > self.game.ball.rect.centery:
            self.rect.y -= self.speed

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score_human = 0
        self.score_cpu = 0
        self.font = pygame.font.Font(None, 36)

        self.all_sprites = pygame.sprite.Group()
        self.ball = Ball()
        self.paddle_human = PaddleHuman()
        self.paddle_cpu = PaddleCPU(self)

        self.all_sprites.add(self.ball, self.paddle_human, self.paddle_cpu)

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        self.paddle_human.update(keys)
        self.paddle_cpu.update()
        self.ball.update()

        # Check collision between ball and paddles
        if pygame.sprite.collide_rect(self.ball, self.paddle_human) or pygame.sprite.collide_rect(self.ball, self.paddle_cpu):
            self.ball.speed[0] = -self.ball.speed[0]

        # Check if ball misses the paddles
        if self.ball.rect.x <= 0:
            self.score_cpu += 1
            self.ball.rect.x = WIDTH // 2
            self.ball.rect.y = HEIGHT // 2
        elif self.ball.rect.x >= WIDTH - 20:
            self.score_human += 1
            self.ball.rect.x = WIDTH // 2
            self.ball.rect.y = HEIGHT // 2

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        score_text = self.font.render(f'Human: {self.score_human} CPU: {self.score_cpu}', True, WHITE)
        self.screen.blit(score_text, (WIDTH // 2 - 100, 20))

        if self.score_human >= 5 or self.score_cpu >= 5:
            game_over_text = self.font.render('Game Over!', True, WHITE)
            self.screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2))
            restart_text = self.font.render('Press R to restart', True, WHITE)
            self.screen.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 40))
            self.game_over = True

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
