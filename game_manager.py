import random

import pygame

from minigames.flappy_gap import FlappyGap

# The manager is always in exactly one of these states (a simple state machine)
READY = "ready"          # shows the instruction word
PLAYING = "playing"      # a minigame is running
RESULT = "result"        # shows WIN / MISS for a moment
GAME_OVER = "game_over"  # out of lives


class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.big_font = pygame.font.Font(None, 110)
        self.font = pygame.font.Font(None, 48)

        # Add new minigame classes to this list as you build them
        self.minigame_classes = [FlappyGap]

        self.reset()

    # ---------- setup ----------
    def reset(self):
        self.lives = 4
        self.score = 0
        self.start_ready()

    def start_ready(self):
        game_class = random.choice(self.minigame_classes)
        self.current = game_class(self.width, self.height)
        self.state = READY
        self.state_timer = 1.5

    # ---------- the three phases of the game loop ----------
    def handle_event(self, event):
        if self.state == PLAYING:
            self.current.handle_event(event)
        elif self.state == GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()

    def update(self, dt):
        if self.state == READY:
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = PLAYING

        elif self.state == PLAYING:
            self.current.update(dt)
            if self.current.finished:
                if self.current.won:
                    self.score += 1
                else:
                    self.lives -= 1
                self.state = RESULT
                self.state_timer = 1.0

        elif self.state == RESULT:
            self.state_timer -= dt
            if self.state_timer <= 0:
                if self.lives <= 0:
                    self.state = GAME_OVER
                else:
                    self.start_ready()

    def draw(self):
        if self.state == READY:
            self.screen.fill((20, 20, 40))
            self.draw_centered(self.current.instruction, self.big_font, (255, 220, 0), self.height // 2)

        elif self.state == PLAYING:
            self.current.draw(self.screen)
            self.draw_timer_bar()

        elif self.state == RESULT:
            self.current.draw(self.screen)
            if self.current.won:
                self.draw_centered("WIN!", self.big_font, (80, 255, 120), self.height // 2)
            else:
                self.draw_centered("MISS!", self.big_font, (255, 80, 80), self.height // 2)

        elif self.state == GAME_OVER:
            self.screen.fill((20, 20, 40))
            self.draw_centered("GAME OVER", self.big_font, (255, 80, 80), self.height // 2 - 40)
            self.draw_centered(f"Score: {self.score}", self.font, (255, 255, 255), self.height // 2 + 30)
            self.draw_centered("Press SPACE to play again", self.font, (200, 200, 200), self.height // 2 + 80)

        if self.state != GAME_OVER:
            self.draw_hud()

    # ---------- small drawing helpers ----------
    def draw_centered(self, text, font, color, y):
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(self.width // 2, y))
        self.screen.blit(surface, rect)

    def draw_timer_bar(self):
        fraction = self.current.time_left / self.current.duration
        pygame.draw.rect(self.screen, (60, 60, 60), (0, 0, self.width, 20))
        pygame.draw.rect(self.screen, (255, 220, 0), (0, 0, int(self.width * fraction), 20))

    def draw_hud(self):
        text = self.font.render(f"Score: {self.score}   Lives: {self.lives}", True, (255, 255, 255))
        self.screen.blit(text, (15, self.height - 45))