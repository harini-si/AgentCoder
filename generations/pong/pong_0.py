
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
        self.speed = [5, 5]  # Initial speed in x and y directions

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]

    def collide_paddle(self):
        self.speed[0] = -self.speed[0]

class PaddleHuman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centery = HEIGHT // 2
        self.rect.left = 10
        self.speed = 10

    def update(self, keys):
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
        self.rect.centery = HEIGHT // 2
        self.rect.right = WIDTH - 10
        self.speed = 5
        self.game = game

    def update(self):
        if self.game.ball.rect.centery < self.rect.centery:
            self.rect.y -= self.speed
        if self.game.ball.rect.centery > self.rect.centery:
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
        self.score_human = 0
        self.score_cpu = 0
        self.font = pygame.font.Font(None, 36)
        self.all_sprites.add(self.ball, self.paddle_human, self.paddle_cpu)

    def run(self, event):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        self.all_sprites.update()

        if pygame.sprite.collide_rect(self.ball, self.paddle_human):
            self.ball.collide_paddle()
        if pygame.sprite.collide_rect(self.ball, self.paddle_cpu):
            self.ball.collide_paddle()

        if self.ball.rect.right >= WIDTH:
            self.score_human += 1
            self.ball.rect.center = (WIDTH // 2, HEIGHT // 2)

        if self.ball.rect.left <= 0:
            self.score_cpu += 1
            self.ball.rect.center = (WIDTH // 2, HEIGHT // 2)

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        score_display = self.font.render(f"Human: {self.score_human} CPU: {self.score_cpu}", True, WHITE)
        self.screen.blit(score_display, (WIDTH // 2 - 100, 10))

        if self.score_human >= 5 or self.score_cpu >= 5:
            self.game_over = True

        if self.game_over:
            game_over_text = self.font.render("Game Over!", True, WHITE)
            self.screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
            restart_text = self.font.render("Press R to restart", True, WHITE)
            self.screen.blit(restart_text, (WIDTH // 2 - 100, HEIGHT // 2 + 20))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.__init__()  # Restart the game

        pygame.display.flip()
        self.clock.tick(FPS)

        return True

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
