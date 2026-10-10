import pygame

from game_manager import GameManager

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WarioWare Clone")
clock = pygame.time.Clock()

manager = GameManager(screen)

running = True
while running:
    # dt = seconds since the last frame (tick returns milliseconds)
    dt = clock.tick(60) / 1000

    # 1. Handle input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            manager.handle_event(event)

    # 2. Update game state
    manager.update(dt)

    # 3. Draw
    manager.draw()
    pygame.display.flip()

pygame.quit()

