class GameTimer:
    """Manages the countdown timer for the game."""

    def __init__(self, timeout_seconds: int, on_tick=None, on_timeout=None):
        self.total_seconds = timeout_seconds
        self.remaining_seconds = timeout_seconds
        self.on_tick = on_tick
        self.on_timeout = on_timeout
        self._timer_id = None
        self._root = None
        self._running = False

    def start(self, root):
        self._root = root
        self._running = True
        self._tick()

    def stop(self):
        self._running = False
        if self._timer_id and self._root:
            self._root.after_cancel(self._timer_id)
            self._timer_id = None

    def _tick(self):
        if not self._running:
            return

        if self.on_tick:
            self.on_tick(self.remaining_seconds)

        if self.remaining_seconds <= 0:
            self._running = False
            if self.on_timeout:
                self.on_timeout()
            return

        self.remaining_seconds -= 1
        self._timer_id = self._root.after(1000, self._tick)

    def get_formatted_time(self) -> str:
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    @property
    def is_running(self) -> bool:
        return self._running
