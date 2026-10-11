import asyncio

import pygame

from game_manager import GameManager

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WarioWare Clone")
clock = pygame.time.Clock()

manager = GameManager(screen)


async def main():
    running = True
    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                manager.handle_event(event)

        manager.update(dt)
        manager.draw()
        pygame.display.flip()

        await asyncio.sleep(0)   # give control back to the browser every frame

    pygame.quit()


asyncio.run(main())

