"""
GRAVITAS - Week 1: window, ball, drag-to-shoot and friction

How to play:
    Press the mouse on the ball, pull back (the arrow shows the shot),
    then release to shoot. The ball slows down because of friction and
    bounces off the screen edges.
    Press ESC or close the window to quit.
"""
import pygame

pygame.init()

# ---------- Settings ----------
WIDTH, HEIGHT = 1000, 650
FPS = 60
BG_COLOR = (8, 8, 20)

BALL_RADIUS = 10
FRICTION = 0.99        # speed is multiplied by this every frame
MAX_DRAG = 150         # longest pull (limits the shot power)
POWER = 0.12           # pull length -> ball speed


class Ball:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)     # position
        self.vel = pygame.Vector2(0, 0)     # velocity (pixels per frame)

    def is_moving(self):
        return self.vel.length() > 0

    def update(self):
        self.pos += self.vel
        self.vel *= FRICTION
        if self.vel.length() < 0.05:        # stop when very slow
            self.vel = pygame.Vector2(0, 0)

        # bounce off the screen edges
        if self.pos.x < BALL_RADIUS or self.pos.x > WIDTH - BALL_RADIUS:
            self.vel.x *= -1
            self.pos.x = max(BALL_RADIUS, min(WIDTH - BALL_RADIUS, self.pos.x))
        if self.pos.y < BALL_RADIUS or self.pos.y > HEIGHT - BALL_RADIUS:
            self.vel.y *= -1
            self.pos.y = max(BALL_RADIUS, min(HEIGHT - BALL_RADIUS, self.pos.y))

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), self.pos, BALL_RADIUS)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Gravitas")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.ball = Ball(200, 325)
        self.dragging = False
        self.running = True

    def pull_vector(self, mouse):
        """Direction and length of the shot: from the mouse to the ball."""
        pull = self.ball.pos - pygame.Vector2(mouse)
        if pull.length() > MAX_DRAG:
            pull.scale_to_length(MAX_DRAG)
        return pull

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False

        # click near the ball: start dragging
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self.ball.is_moving():
                if pygame.Vector2(event.pos).distance_to(self.ball.pos) < 30:
                    self.dragging = True

        # release: shoot
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging:
            self.dragging = False
            self.ball.vel = self.pull_vector(event.pos) * POWER

    def draw(self):
        self.screen.fill(BG_COLOR)

        if self.dragging:
            pull = self.pull_vector(pygame.mouse.get_pos())
            end = self.ball.pos + pull
            pygame.draw.line(self.screen, (255, 200, 0), self.ball.pos, end, 3)
            pygame.draw.circle(self.screen, (255, 200, 0), end, 5)

        self.ball.draw(self.screen)

        hint = self.font.render("Drag back from the ball and release to shoot   |   ESC = quit",
                                True, (90, 105, 150))
        self.screen.blit(hint, (20, HEIGHT - 35))
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.ball.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    Game().run()
