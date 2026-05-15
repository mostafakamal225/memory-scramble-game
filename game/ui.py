import tkinter as tk
from tkinter import messagebox

from game.board import Board
from game.timer import GameTimer


CARD_BACK_COLOR = "#3498db"
CARD_FACE_COLOR = "#ecf0f1"
CARD_MATCHED_COLOR = "#2ecc71"
CARD_BACK_TEXT_COLOR = "#ffffff"
CARD_FACE_TEXT_COLOR = "#2c3e50"
BG_COLOR = "#34495e"
HEADER_COLOR = "#2c3e50"


class GameUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Memory Scramble")
        self.root.configure(bg=BG_COLOR)
        self.root.geometry("420x320")

        self.board = None
        self.timer = None
        self.card_buttons = []
        self.first_card = None
        self.second_card = None
        self.is_checking = False
        self.moves = 0

        self._show_config()

    def _clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def _show_config(self):
        self._clear_window()
        self.root.geometry("420x320")
        self.root.title("Memory Scramble - Configuration")

        # Title
        tk.Label(
            self.root, text="Memory Scramble",
            font=("Helvetica", 18, "bold"), bg=BG_COLOR, fg="white"
        ).pack(pady=(25, 5))

        tk.Label(
            self.root, text="Configure your game",
            font=("Helvetica", 10), bg=BG_COLOR, fg="#bdc3c7"
        ).pack(pady=(0, 20))

        # Settings frame
        settings_frame = tk.Frame(self.root, bg=BG_COLOR)
        settings_frame.pack(padx=40, fill="x")

        # Rows
        row_frame = tk.Frame(settings_frame, bg=BG_COLOR)
        row_frame.pack(fill="x", pady=5)
        tk.Label(row_frame, text="Number of Rows:", width=18, anchor="w",
                 bg=BG_COLOR, fg="white").pack(side="left")
        self.rows_var = tk.StringVar(value="4")
        tk.Entry(row_frame, textvariable=self.rows_var, width=10).pack(side="left", padx=(10, 0))

        # Columns
        col_frame = tk.Frame(settings_frame, bg=BG_COLOR)
        col_frame.pack(fill="x", pady=5)
        tk.Label(col_frame, text="Number of Columns:", width=18, anchor="w",
                 bg=BG_COLOR, fg="white").pack(side="left")
        self.cols_var = tk.StringVar(value="4")
        tk.Entry(col_frame, textvariable=self.cols_var, width=10).pack(side="left", padx=(10, 0))

        # Timeout
        time_frame = tk.Frame(settings_frame, bg=BG_COLOR)
        time_frame.pack(fill="x", pady=5)
        tk.Label(time_frame, text="Time Limit (seconds):", width=18, anchor="w",
                 bg=BG_COLOR, fg="white").pack(side="left")
        self.time_var = tk.StringVar(value="60")
        tk.Entry(time_frame, textvariable=self.time_var, width=10).pack(side="left", padx=(10, 0))

        # Note
        tk.Label(
            self.root, text="Note: Total cells (rows x columns) must be even.",
            font=("Helvetica", 9, "italic"), bg=BG_COLOR, fg="gray"
        ).pack(pady=(15, 5))

        # Start button
        tk.Button(
            self.root, text="Start Game",
            font=("Helvetica", 12, "bold"),
            command=self._on_start_click,
            bg="#4CAF50", fg="white", padx=20, pady=5
        ).pack(pady=15)

    def _on_start_click(self):
        """Validate config inputs and start the game."""
        try:
            n_rows = int(self.rows_var.get())
            n_cols = int(self.cols_var.get())
            timeout = int(self.time_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Please enter valid integer values for all fields.",
                                 parent=self.root)
            return

        if n_rows < 2 or n_cols < 2:
            messagebox.showerror("Invalid Size",
                                 "Rows and columns must be at least 2.",
                                 parent=self.root)
            return

        if (n_rows * n_cols) % 2 != 0:
            messagebox.showerror("Invalid Size",
                                 "Total number of cells (rows x columns) must be even.",
                                 parent=self.root)
            return

        if n_rows * n_cols > 104:
            messagebox.showerror("Size Too Large",
                                 "Maximum supported board size is 104 cells (52 pairs).",
                                 parent=self.root)
            return

        if timeout < 10:
            messagebox.showerror("Invalid Timeout",
                                 "Timeout must be at least 10 seconds.",
                                 parent=self.root)
            return

        self.n_rows = n_rows
        self.n_cols = n_cols
        self.timeout = timeout
        self._setup_game()

    def _setup_game(self):
        """Initialize board, timer, and UI elements."""
        self._clear_window()
        self.root.title("Memory Scramble")

        self.board = Board(self.n_rows, self.n_cols)
        self.first_card = None
        self.second_card = None
        self.is_checking = False
        self.moves = 0
        self.card_buttons = []

        self._create_header()
        self._create_board_ui()
        self._start_timer()

        self.root.geometry("")
        self.root.update_idletasks()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())

    def _create_header(self):
        header_frame = tk.Frame(self.root, bg=HEADER_COLOR, padx=10, pady=10)
        header_frame.pack(fill="x")

        # Title
        title_label = tk.Label(
            header_frame,
            text="Memory Scramble",
            font=("Helvetica", 16, "bold"),
            bg=HEADER_COLOR,
            fg="white"
        )
        title_label.pack(side="left")

        # Timer display
        self.timer_label = tk.Label(
            header_frame,
            text="⏱ --:--",
            font=("Helvetica", 14, "bold"),
            bg=HEADER_COLOR,
            fg="#e74c3c"
        )
        self.timer_label.pack(side="right", padx=(20, 0))

        # Moves counter
        self.moves_label = tk.Label(
            header_frame,
            text="Moves: 0",
            font=("Helvetica", 12),
            bg=HEADER_COLOR,
            fg="#bdc3c7"
        )
        self.moves_label.pack(side="right")

    def _create_board_ui(self):
        board_frame = tk.Frame(self.root, bg=BG_COLOR, padx=10, pady=10)
        board_frame.pack(expand=True, fill="both")

        card_width = max(4, 10 - self.n_cols)
        card_height = max(2, 5 - self.n_rows // 2)
        font_size = max(12, 28 - max(self.n_rows, self.n_cols) * 2)

        self.card_buttons = []
        for row in range(self.n_rows):
            row_buttons = []
            for col in range(self.n_cols):
                btn = tk.Button(
                    board_frame,
                    text="?",
                    font=("Helvetica", font_size, "bold"),
                    width=card_width,
                    height=card_height,
                    bg=CARD_BACK_COLOR,
                    fg=CARD_BACK_TEXT_COLOR,
                    relief="raised",
                    borderwidth=3,
                    command=lambda r=row, c=col: self._on_card_click(r, c)
                )
                btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
                row_buttons.append(btn)
            self.card_buttons.append(row_buttons)

        for i in range(self.n_cols):
            board_frame.columnconfigure(i, weight=1)
        for i in range(self.n_rows):
            board_frame.rowconfigure(i, weight=1)

    def _start_timer(self):
        self.timer = GameTimer(
            self.timeout,
            on_tick=self._on_timer_tick,
            on_timeout=self._on_timeout
        )
        self.timer.start(self.root)

    def _on_timer_tick(self, remaining):
        minutes = remaining // 60
        seconds = remaining % 60
        time_str = f"⏱ {minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=time_str)

        if remaining <= 10:
            self.timer_label.config(fg="#e74c3c")
        elif remaining <= 30:
            self.timer_label.config(fg="#f39c12")

    def _on_card_click(self, row, col):
        if self.is_checking:
            return

        card = self.board.get_card(row, col)

        if card.is_matched or card.is_face_up:
            return

        card.flip_up()
        self._update_card_display(row, col)

        if self.first_card is None:
            self.first_card = card
        else:
            self.second_card = card
            self.moves += 1
            self.moves_label.config(text=f"Moves: {self.moves}")
            self.is_checking = True

            self.root.after(800, self._check_match)

    def _check_match(self):
        if self.board.check_match(self.first_card, self.second_card):
            self._update_card_display(self.first_card.row, self.first_card.col)
            self._update_card_display(self.second_card.row, self.second_card.col)

            # Check if game is complete
            if self.board.is_complete():
                self.timer.stop()
                self._show_victory()
        else:
            # Cards don't match so flip them back
            self.first_card.flip_down()
            self.second_card.flip_down()
            self._update_card_display(self.first_card.row, self.first_card.col)
            self._update_card_display(self.second_card.row, self.second_card.col)

        # Reset selection
        self.first_card = None
        self.second_card = None
        self.is_checking = False

    def _update_card_display(self, row, col):
        card = self.board.get_card(row, col)
        btn = self.card_buttons[row][col]

        if card.is_matched:
            btn.config(
                text=card.symbol,
                bg=CARD_MATCHED_COLOR,
                fg=CARD_FACE_TEXT_COLOR,
                relief="sunken",
                state="disabled"
            )
        elif card.is_face_up:
            btn.config(
                text=card.symbol,
                bg=CARD_FACE_COLOR,
                fg=CARD_FACE_TEXT_COLOR,
                relief="flat"
            )
        else:
            btn.config(
                text="?",
                bg=CARD_BACK_COLOR,
                fg=CARD_BACK_TEXT_COLOR,
                relief="raised"
            )

    def _on_timeout(self):
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                card = self.board.get_card(row, col)
                if not card.is_matched:
                    card.flip_up()
                    self._update_card_display(row, col)

        messagebox.showinfo(
            f"⏰ Time's up!\n\n"
            f"You matched {self.board.matched_pairs} out of {self.board.total_pairs} pairs.\n"
            f"Total moves: {self.moves}\n\n"
            f"Better luck next time!",
            parent=self.root
        )
        self._ask_play_again()

    def _show_victory(self):
        time_used = self.timeout - self.timer.remaining_seconds
        messagebox.showinfo(
            "Congratulations!",
            f"🎉 You Won!\n\n"
            f"All {self.board.total_pairs} pairs matched!\n"
            f"Time used: {time_used} seconds\n"
            f"Total moves: {self.moves}",
            parent=self.root
        )
        self._ask_play_again()

    def _ask_play_again(self):
        play_again = messagebox.askyesno(
            "Play Again?",
            "Would you like to play another round?",
            parent=self.root
        )
        if play_again:
            self._show_config()
        else:
            self.root.destroy()

    def run(self):
        self.root.mainloop()
