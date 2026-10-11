import random
import pygame
from minigames.base import Minigame

TILE = 44
MOVE_DELAY = 0.12

DIRECTIONS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0)
}

MAZES = [
    [
        "###############",
        "#S..#.....#...#",
        "#.#.#.###.#.#.#",
        "#.#...#...#.#.#",
        "#.#####.###.#.#",
        "#.....#.....#.#",
        "#####.#######.#",
        "#.....#.....#.#",
        "#.#####.###.#.#",
        "#.......#...#E#",
        "###############",
    ],
    [
        "###############",
        "#S....#.......#",
        "#.###.#.#####.#",
        "#.#...#.#...#.#",
        "#.#.###.#.#.#.#",
        "#.#.....#.#...#",
        "#.#######.#####",
        "#.........#...#",
        "#.#######.#.#.#",
        "#.......#...#E#",
        "###############",
    ],
    [
        "###############",
        "#S#...#.......#",
        "#.#.#.#.#####.#",
        "#.#.#...#...#.#",
        "#.#.#####.#.#.#",
        "#.#.......#.#.#",
        "#.#########.#.#",
        "#...........#.#",
        "#.###########.#",
        "#............E#",
        "###############",
    ],
]

class MazeRush(Minigame):
    instruction = "ESCAPE!"

    def __init__(self, width, height):
        super().__init__(width, height, duration=10.0)
        self.grid = random.choice(MAZES)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.offset_x = (width - self.cols * TILE) // 2
        self.offset_y = 50
        self.player = (1, 1)
        self.exit = (1, 1)
        for row, line in enumerate(self.grid):
            for col, char in enumerate(line):
                if char == "S":
                    self.player = (col, row)
                elif char == "E":
                    self.exit = (col, row)
        self.move_timer = 0.0

    def tile_rect(self, col, row):
        return pygame.Rect(
            self.offset_x + col * TILE,
            self.offset_y + row * TILE,
            TILE,
            TILE
        )

    def try_move(self, dx, dy):
        col = self.player[0] + dx
        row = self.player[1] + dy

        if self.grid[row][col] == "#":
            return False

        self.player = (col, row)
        if self.player == self.exit:
            self.win()
        return True

    def handle_event(self, event):
        pass

    def update_game(self, dt):
        self.move_timer -= dt
        if self.move_timer > 0:
            return

        keys = pygame.key.get_pressed()
        for key, (dx, dy) in DIRECTIONS.items():
            if keys[key] and self.try_move(dx, dy):
                self.move_timer = MOVE_DELAY
                break

    def on_timeout(self):
        self.lose()

    def draw(self, screen):
        screen.fill((25, 25, 45))

        for row, line in enumerate(self.grid):
            for col, char in enumerate(line):
                rect = self.tile_rect(col, row)
                if char == "#":
                    pygame.draw.rect(screen, (90, 90, 150), rect)
                else:
                    pygame.draw.rect(screen, (50, 50, 80), rect)
                    pygame.draw.rect(screen, (35, 35, 60), rect, 1)

        exit_rect = self.tile_rect(*self.exit).inflate(-10, -10)
        pygame.draw.rect(screen, (80, 255, 120), exit_rect, border_radius=8)

        player_rect = self.tile_rect(*self.player)
        pygame.draw.circle(screen, (255, 215, 0), player_rect.center, TILE//2 - 6)