import tkinter as tk
from game.board import Board
from game.timer import GameTimer



CARD_BACK_COLOR = "#571313"

CARD_FACE_COLOR = "#d8d8d8"

CARD_MATCHED_COLOR = "#8E8E8E"

CARD_BACK_TEXT_COLOR = "#ffffff"
CARD_FACE_TEXT_COLOR = "#111111"

BG_COLOR = "#565757"
HEADER_COLOR = "#313132"

ACCENT_COLOR = "#7A1C1C"
HOVER_COLOR = "#8E8E8E"


class GameUI:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Memory Scramble")

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        self.root.geometry(f"{screen_w}x{screen_h}+0+0")

        self.root.configure(bg=BG_COLOR)

        self.root.minsize(1100, 700)

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

    # CONFIG SCREEN
    def _show_config(self):

        self._clear_window()

        self.root.title("Memory Scramble - Configuration")

        main_container = tk.Frame(
            self.root,
            bg=BG_COLOR
        )

        main_container.pack(
            fill="both",
            expand=True
        )

        card = tk.Frame(
            main_container,
            bg=HEADER_COLOR
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=650,
            height=560
        )

        top_bar = tk.Frame(
            card,
            bg=ACCENT_COLOR,
            height=10
        )

        top_bar.pack(fill="x")

        title = tk.Label(
            card,
            text="MEMORY SCRAMBLE",
            font=("Helvetica", 30, "bold"),
            bg=HEADER_COLOR,
            fg="white"
        )

        title.pack(pady=(40, 10))

        subtitle = tk.Label(
            card,
            text="Configure your game and start matching",
            font=("Helvetica", 13),
            bg=HEADER_COLOR,
            fg="#d0d0d0"
        )

        subtitle.pack(pady=(0, 35))

        settings_frame = tk.Frame(
            card,
            bg=HEADER_COLOR
        )

        settings_frame.pack(
            padx=60,
            fill="x"
        )

        # ROWS
        self.rows_var = tk.StringVar(value="4")

        self._create_input_row(
            settings_frame,
            "Number of Rows",
            self.rows_var
        )

        # COLUMNS
        self.cols_var = tk.StringVar(value="4")

        self._create_input_row(
            settings_frame,
            "Number of Columns",
            self.cols_var
        )

        self.time_var = tk.StringVar(value="60")

        self._create_input_row(
            settings_frame,
            "Time Limit (seconds)",
            self.time_var
        )

        note = tk.Label(
            card,
            text="Rows × Columns must be EVEN",
            font=("Helvetica", 10, "italic"),
            bg=HEADER_COLOR,
            fg="#aaaaaa"
        )

        note.pack(pady=(35, 15))

        start_btn = tk.Button(
            card,
            text="START GAME",
            font=("Helvetica", 16, "bold"),
            bg=CARD_BACK_COLOR,
            fg="white",
            activebackground=HOVER_COLOR,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=25,
            cursor="hand2",
            command=self._on_start_click
        )

        start_btn.pack(ipadx=10, pady=(0, 0))

        start_btn.bind(
            "<Enter>",
            lambda e:
            start_btn.config(bg=HOVER_COLOR)
        )

        start_btn.bind(
            "<Leave>",
            lambda e:
            start_btn.config(bg=CARD_BACK_COLOR)
        )

    def _create_input_row(
            self,
            parent,
            label_text,
            variable
    ):

        container = tk.Frame(
            parent,
            bg=HEADER_COLOR
        )

        container.pack(
            fill="x",
            pady=12
        )

        label = tk.Label(
            container,
            text=label_text,
            font=("Helvetica", 13, "bold"),
            bg=HEADER_COLOR,
            fg="white",
            anchor="w"
        )

        label.pack(
            fill="x",
            pady=(0, 8)
        )

        entry = tk.Entry(
            container,
            textvariable=variable,
            font=("Helvetica", 13),
            bg="#404040",
            fg="white",
            insertbackground="white",
            relief="flat",
            bd=0
        )

        entry.pack(
            fill="x",
            ipady=10,
            padx=2
        )

    # START GAME
    def _on_start_click(self):

        try:

            n_rows = int(self.rows_var.get())
            n_cols = int(self.cols_var.get())
            timeout = int(self.time_var.get())

        except ValueError:

            self._show_custom_popup(
                "INVALID INPUT",
                "Please enter valid integer values."
            )

            return

        if n_rows < 2 or n_cols < 2:

            self._show_custom_popup(
                "INVALID SIZE",
                "Rows and columns must be at least 2."
            )

            return

        if (n_rows * n_cols) % 2 != 0:

            self._show_custom_popup(
                "INVALID SIZE",
                "Total cells must be EVEN."
            )

            return

        if n_rows * n_cols > 104:

            self._show_custom_popup(
                "BOARD TOO LARGE",
                "Maximum supported board size is 104 cells."
            )

            return

        if timeout < 10:

            self._show_custom_popup(
                "INVALID TIME",
                "Timeout must be at least 10 seconds."
            )

            return

        self.n_rows = n_rows
        self.n_cols = n_cols
        self.timeout = timeout

        self._setup_game()


    def _setup_game(self):

        self._clear_window()

        self.board = Board(
            self.n_rows,
            self.n_cols
        )

        self.first_card = None
        self.second_card = None

        self.is_checking = False

        self.moves = 0

        self.card_buttons = []

        self._create_header()

        self._create_board_ui()

        self._start_timer()


    def _create_header(self):

        header = tk.Frame(
            self.root,
            bg=HEADER_COLOR,
            height=90
        )

        header.pack(fill="x")

        left = tk.Frame(
            header,
            bg=HEADER_COLOR
        )

        left.pack(
            side="left",
            padx=30,
            pady=15
        )

        title = tk.Label(
            left,
            text="Memory Scramble",
            font=("Helvetica", 24, "bold"),
            bg=HEADER_COLOR,
            fg="white"
        )

        title.pack(anchor="w")

        subtitle = tk.Label(
            left,
            text="Find all matching pairs",
            font=("Helvetica", 11),
            bg=HEADER_COLOR,
            fg="#bdbdbd"
        )

        subtitle.pack(anchor="w")

        right = tk.Frame(
            header,
            bg=HEADER_COLOR
        )

        right.pack(
            side="right",
            padx=30
        )

        self.moves_label = tk.Label(
            right,
            text="Moves: 0",
            font=("Helvetica", 14, "bold"),
            bg=HEADER_COLOR,
            fg="white"
        )

        self.moves_label.pack(
            side="left",
            padx=20
        )

        self.timer_label = tk.Label(
            right,
            text="⏱ 00:00",
            font=("Helvetica", 16, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            padx=18,
            pady=8
        )

        self.timer_label.pack(side="left")


    def _create_board_ui(self):

        outer = tk.Frame(
            self.root,
            bg=BG_COLOR
        )

        outer.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        board_frame = tk.Frame(
            outer,
            bg=HEADER_COLOR
        )

        board_frame.pack(
            fill="both",
            expand=True
        )

        card_width = max(4, 14 - self.n_cols)

        card_height = max(2, 7 - self.n_rows // 2)

        font_size = max(
            16,
            34 - max(self.n_rows, self.n_cols) * 2
        )

        self.card_buttons = []

        for row in range(self.n_rows):

            row_buttons = []

            for col in range(self.n_cols):

                btn = tk.Button(
                    board_frame,

                    text="?",

                    font=("Helvetica", font_size, "bold"),

                    bg=CARD_BACK_COLOR,
                    fg="white",

                    activebackground=HOVER_COLOR,
                    activeforeground="white",

                    relief="flat",
                    bd=0,

                    width=card_width,
                    height=card_height,

                    cursor="hand2",

                    command=lambda r=row, c=col:
                    self._on_card_click(r, c)
                )

                btn.grid(
                    row=row,
                    column=col,
                    padx=8,
                    pady=8,
                    sticky="nsew"
                )

                # HOVER EFFECT
                btn.bind(
                    "<Enter>",
                    lambda e, b=btn:
                    b.config(bg=HOVER_COLOR)
                )

                btn.bind(
                    "<Leave>",
                    lambda e, b=btn:
                    self._restore_card_color(b)
                )

                row_buttons.append(btn)

            self.card_buttons.append(row_buttons)

        # GRID RESPONSIVE
        for i in range(self.n_cols):
            board_frame.columnconfigure(i, weight=1)

        for i in range(self.n_rows):
            board_frame.rowconfigure(i, weight=1)

    def _restore_card_color(self, btn):

        current_text = btn.cget("text")

        if current_text == "?":

            btn.config(
                bg=CARD_BACK_COLOR
            )


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

        self.timer_label.config(
            text=f"⏱ {minutes:02d}:{seconds:02d}"
        )

        if remaining <= 10:

            self.timer_label.config(
                bg="#a31616"
            )

        elif remaining <= 30:

            self.timer_label.config(
                bg="#8a4f13"
            )

        else:

            self.timer_label.config(
                bg=ACCENT_COLOR
            )


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

            self.moves_label.config(
                text=f"Moves: {self.moves}"
            )

            self.is_checking = True

            self.root.after(
                700,
                self._check_match
            )


    def _check_match(self):

        if self.board.check_match(
                self.first_card,
                self.second_card
        ):

            self._update_card_display(
                self.first_card.row,
                self.first_card.col
            )

            self._update_card_display(
                self.second_card.row,
                self.second_card.col
            )

            if self.board.is_complete():

                self.timer.stop()

                self._show_victory()

        else:

            self.first_card.flip_down()

            self.second_card.flip_down()

            self._update_card_display(
                self.first_card.row,
                self.first_card.col
            )

            self._update_card_display(
                self.second_card.row,
                self.second_card.col
            )

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
                fg="white",

                relief="flat",

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

                relief="flat"
            )


    def _show_custom_popup(
            self,
            title,
            message,
            is_win=False
    ):

        popup = tk.Toplevel(self.root)

        popup.title(title)

        popup.geometry("650x420")

        popup.configure(
            bg=HEADER_COLOR
        )

        popup.resizable(False, False)

        popup.transient(self.root)

        popup.grab_set()

        popup.update_idletasks()

        x = (
                popup.winfo_screenwidth() // 2
                - 650 // 2
        )

        y = (
                popup.winfo_screenheight() // 2
                - 420 // 2
        )

        popup.geometry(
            f"650x420+{x}+{y}"
        )

        top = tk.Frame(
            popup,
            bg=ACCENT_COLOR,
            height=10
        )

        top.pack(fill="x")

        icon = "🎉" if is_win else "⏰"

        icon_label = tk.Label(
            popup,
            text=icon,
            font=("Helvetica", 55),
            bg=HEADER_COLOR,
            fg="white"
        )

        icon_label.pack(
            pady=(35, 10)
        )

        title_label = tk.Label(
            popup,
            text=title,
            font=("Helvetica", 28, "bold"),
            bg=HEADER_COLOR,
            fg="white"
        )

        title_label.pack(
            pady=(0, 20)
        )

        message_label = tk.Label(
            popup,
            text=message,
            font=("Helvetica", 15),
            bg=HEADER_COLOR,
            fg="#d7d7d7",
            justify="center"
        )

        message_label.pack(
            pady=(0, 35)
        )

        btn_frame = tk.Frame(
            popup,
            bg=HEADER_COLOR
        )

        btn_frame.pack()

        # PLAY AGAIN
        play_btn = tk.Button(
            btn_frame,
            text="PLAY AGAIN",
            font=("Helvetica", 14, "bold"),
            bg=CARD_BACK_COLOR,
            fg="white",
            activebackground=HOVER_COLOR,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=28,
            pady=14,
            cursor="hand2",
            command=lambda: [
                popup.destroy(),
                self._show_config()
            ]
        )

        play_btn.pack(
            side="left",
            padx=15
        )

        exit_btn = tk.Button(
            btn_frame,
            text="EXIT",
            font=("Helvetica", 14, "bold"),
            bg="#404040",
            fg="white",
            activebackground="#555555",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=40,
            pady=14,
            cursor="hand2",
            command=self.root.destroy
        )

        exit_btn.pack(
            side="left",
            padx=15
        )

    def _on_timeout(self):

        for row in range(self.n_rows):

            for col in range(self.n_cols):

                card = self.board.get_card(row, col)

                if not card.is_matched:

                    card.flip_up()

                    self._update_card_display(row, col)

        self._show_custom_popup(
            "GAME OVER",
            f"Time's Up!\n\n"
            f"Matched Pairs: "
            f"{self.board.matched_pairs}/"
            f"{self.board.total_pairs}\n\n"
            f"Moves: {self.moves}",
            False
        )


    def _show_victory(self):

        time_used = (
                self.timeout -
                self.timer.remaining_seconds
        )

        self._show_custom_popup(
            "YOU WON!",
            f"All pairs matched successfully!\n\n"
            f"Time Used: {time_used} sec\n\n"
            f"Total Moves: {self.moves}",
            True
        )


    def run(self):

        self.root.mainloop()