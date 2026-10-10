import random

import pygame

from minigames.base import Minigame

GRAVITY = 2000      # pixels per second, per second (how fast we fall faster)
FLAP_SPEED = -500   # negative = upward (screen y grows downward)
SCROLL_SPEED = 400  # how fast the pillars move left, pixels per second
PILLAR_WIDTH = 80
GAP_HEIGHT = 190


class Pillar:
    """A top + bottom pillar pair with a gap between them."""

    def __init__(self, x, gap_center, screen_height):
        self.x = x
        self.screen_height = screen_height
        self.gap_top = gap_center - GAP_HEIGHT // 2
        self.gap_bottom = gap_center + GAP_HEIGHT // 2

    def update(self, dt):
        self.x -= SCROLL_SPEED * dt

    def rects(self):
        top = pygame.Rect(int(self.x), 0, PILLAR_WIDTH, self.gap_top)
        bottom = pygame.Rect(
            int(self.x), self.gap_bottom, PILLAR_WIDTH, self.screen_height - self.gap_bottom
        )
        return top, bottom

    def draw(self, screen):
        for rect in self.rects():
            pygame.draw.rect(screen, (60, 180, 75), rect)
            pygame.draw.rect(screen, (30, 110, 40), rect, 4)


class FlappyGap(Minigame):
    """Tap SPACE to flap. Survive until the timer ends."""

    instruction = "FLY!"

    def __init__(self, width, height):
        super().__init__(width, height, duration=15.0)

        # the bird
        self.bird_x = 150
        self.bird_y = height / 2
        self.bird_vy = 0
        self.bird_radius = 18

        # the pillars: the first gap is near the bird, each later gap stays
        # within reach of the one before so the level is always beatable
        self.pillars = []
        gap_center = height / 2 + random.randint(-100, 100)
        x = width + 50
        for _ in range(15):
            self.pillars.append(Pillar(x, gap_center, height))
            x += 320
            gap_center += random.randint(-130, 130)
            gap_center = max(150, min(height - 150, gap_center))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.bird_vy = FLAP_SPEED  # instant upward kick

    def update_game(self, dt):
        # gravity changes the speed, the speed changes the position
        self.bird_vy += GRAVITY * dt
        self.bird_y += self.bird_vy * dt

        for pillar in self.pillars:
            pillar.update(dt)

        # lose if we touch the floor or the ceiling
        if self.bird_y - self.bird_radius < 0 or self.bird_y + self.bird_radius > self.height:
            self.lose()
            return

        # lose if the bird's box overlaps any pillar
        bird_rect = pygame.Rect(
            self.bird_x - self.bird_radius,
            self.bird_y - self.bird_radius,
            self.bird_radius * 2,
            self.bird_radius * 2,
        )
        for pillar in self.pillars:
            for rect in pillar.rects():
                if bird_rect.colliderect(rect):
                    self.lose()
                    return

    def on_timeout(self):
        self.win()  # surviving the whole time IS the win condition

    def draw(self, screen):
        screen.fill((110, 200, 240))
        for pillar in self.pillars:
            pillar.draw(screen)

        center = (int(self.bird_x), int(self.bird_y))
        pygame.draw.circle(screen, (255, 215, 0), center, self.bird_radius)
        pygame.draw.circle(screen, (0, 0, 0), center, self.bird_radius, 3)
        pygame.draw.circle(screen, (0, 0, 0), (center[0] + 7, center[1] - 5), 4)  # eye