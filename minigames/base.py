from abc import ABC, abstractmethod


class Minigame(ABC):
    """Blueprint that every minigame must follow.

    The GameManager only ever talks to this interface, so it can run
    any minigame without knowing what it is (polymorphism).
    """

    instruction = "GO!"  # short word shown before the game starts

    def __init__(self, width, height, duration=5.0):
        self.width = width
        self.height = height
        self.duration = duration
        self.time_left = duration
        self.finished = False
        self.won = False

    # ---- shared behaviour (same for every minigame) ----
    def update(self, dt):
        """Called once per frame by the manager. dt = seconds since last frame."""
        if self.finished:
            return

        self.update_game(dt)  # the minigame's own logic
        if self.finished:
            return

        self.time_left -= dt
        if self.time_left <= 0:
            self.time_left = 0
            self.on_timeout()  # each game decides: is running out of time a win or a loss?

    def win(self):
        self.finished = True
        self.won = True

    def lose(self):
        self.finished = True
        self.won = False

    # ---- behaviour each minigame MUST provide ----
    @abstractmethod
    def handle_event(self, event):
        """React to a single input event (mouse click, key press...)."""

    @abstractmethod
    def update_game(self, dt):
        """Move things, check collisions, etc."""

    @abstractmethod
    def on_timeout(self):
        """Called when the timer hits zero. Call self.win() or self.lose()."""

    @abstractmethod
    def draw(self, screen):
        """Draw this minigame onto the screen."""