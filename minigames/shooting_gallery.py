import random
import pygame
from minigames.base import Minigame

class Target:
    def __init__(self, x, y, speed, is_decoy):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = 30
        self.is_decoy = is_decoy

    def update(self, dt, screen_width):
        self.x += self.speed * dt
        if self.x > screen_width + self.radius:
            self.x = -self.radius
        elif self.x < -self.radius:
            self.x = screen_width + self.radius

    def draw(self, screen):
        center = (int(self.x), int(self.y))
        if self.is_decoy:
            pygame.draw.circle(screen, (60, 60, 70), center, self.radius)
            cx, cy = center
            pygame.draw.line(screen, (255, 255, 255), (cx - 12, cy - 12), (cx + 12, cy + 12), 5)
            pygame.draw.line(screen, (255, 255, 255), (cx - 12, cy + 12), (cx + 12, cy - 12), 5)
        else:
            pygame.draw.circle(screen, (230, 50, 50), center, self.radius)
            pygame.draw.circle(screen, (255, 255, 255), center, self.radius * 2//3)
            pygame.draw.circle(screen, (230, 50, 50), center, self.radius//3)

    def contains(self, point):
        dx = point[0] - self.x
        dy = point[1] - self.y
        return dx*dx + dy*dy <= self.radius*self.radius


class ShootingGallery(Minigame):
    instruction  = "SHOOT!"

    def __init__(self, width, height):
        super().__init__(height, width, duration = 6.0)
        self.hits = 0
        self.hits_needed = 3
        self.targets = []
        lanes = [180, 300, 420]
        flags = [True, True, True, False, False, False]
        random.shuffle(flags)

        i = 0
        for lane_number, y in enumerate(lanes):
            direction = 1 if lane_number%2 == 0 else -1
            for _ in range(2):
                speed = random.randint(140, 260) * direction
                x = random.randint(0, width)
                self.targets.append(Target(x, y, speed, flags[i]))
                i += 1
    def handle_event(self, event):
        if self.finished:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for target in self.targets:
                if target.contains(event.pos):
                    if target.is_decoy:
                        self.lose()
                    else:
                        self.hits += 1
                        self.targets.remove(target)
                        if self.hits >= self.hits_needed:
                            self.win()
                    break

    def update_game(self, dt):
        for target in self.targets:
            target.update(dt, self.width)

    def on_timeout(self):
        self.lose()

    def draw(self, screen):
        screen.fill((70, 40, 90))
        for target in self.targets:
            target.draw(screen)
        font = pygame.font.Font(None, 48)
        text = font.render(f"Hits: {self.hits}/{self.hits_needed}", True, (255, 255, 255))
        screen.blit(text, (15, 40))