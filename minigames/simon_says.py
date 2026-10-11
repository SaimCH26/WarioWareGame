import random
import pygame
from minigames.base import Minigame

STEP_TIME = 0.9
LIT_TIME = 0.6

Arrows = {
    pygame.K_UP: {
        "color": (80, 200, 120),
        "offset": (0, -110),
        "shape": [(0, -30), (-25, 20), (25, 20)]
    },
    pygame.K_DOWN: {
        "color": (240, 200, 60),
        "offset": (0, 110),
        "shape": [(0, 30), (-25, -20), (25, -20)]
    },
    pygame.K_LEFT: {
        "color": (80, 140, 240),
        "offset": (-110, 0),
        "shape": [(-30, 0), (20, -25), (20, 25)]
    },
    pygame.K_RIGHT: {
        "color": (230, 80, 100),
        "offset": (110, 0),
        "shape": [(30, 0), (-20, -25), (-20, 25)]
    }
}

class SimonSays(Minigame):
    instruction = "MEMORIZE!"

    def __init__(self, width, height):
        super().__init__(width, height, duration = 9.0)
        self.font = pygame.font.Font(None, 56)
        self.center = (width//2, height//2 + 20)

        self.sequence = [random.choice(list(Arrows)) for _ in range(3)]

        self.phase = "show"
        self.phase_timer = 0.0
        self.flash_key = None

        self.input_index = 0
        self.press_timer = 0.0

    def update_game(self, dt):
        if self.phase == "show":
            self.phase_timer += dt
            step = int(self.phase_timer/STEP_TIME)

            if step >= len(self.sequence):
                self.phase = "input"
                self.flash_key = None
            else:
                time_in_step = self.phase_timer % STEP_TIME
                if time_in_step < LIT_TIME:
                    self.flash_key = self.sequence[step]
                else:
                    self.flash_key = None
        elif self.phase == "input":
            if self.press_timer > 0:
                self.press_timer -= dt
                if self.press_timer <= 0:
                    self.flash_key = None

    def handle_event(self, event):
        if self.finished or self.phase != "input":
            return

        if event.type == pygame.KEYDOWN and event.key in Arrows:
            self.flash_key = event.key
            self.press_timer = 0.15

            if event.key == self.sequence[self.input_index]:
                self.input_index += 1
                if self.input_index >= len(self.sequence):
                    self.win()
            else:
                self.lose()

    def on_timeout(self):
        self.lose()

    def draw_arrow(self, screen, key, lit):
        info = Arrows[key]
        color = info["color"]
        if not lit:
            color = tuple(c // 3 for c in color)

        cx = self.center[0] + info["offset"][0]
        cy = self.center[1] + info["offset"][1]

        button = pygame.Rect(0, 0, 90, 90)
        button.center = (cx, cy)
        pygame.draw.rect(screen, color, button, border_radius = 14)

        points = [(cx + px, cy + py) for px, py in info["shape"]]
        pygame.draw.polygon(screen, (255, 255, 255), points)

    def draw(self, screen):
        screen.fill((35, 35, 70))

        for key in Arrows:
            self.draw_arrow(screen, key, key==self.flash_key)

        label = "WATCH..." if self.phase == "show" else "YOUR TURN!"
        text = self.font.render(label, True, (255, 255, 255))
        rect = text.get_rect(center = (self.width//2, 80))
        screen.blit(text, rect)

        count = len(self.sequence)
        start_x = self.width//2 - (count-1)*20
        for i in range(count):
            filled = i < self.input_index
            color = (80, 255, 120) if filled else (90, 90, 120)
            pygame.draw.circle(screen, color, (start_x + i * 40, self.height - 90), 12)