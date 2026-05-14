import random

# Symbols used as card faces
SYMBOLS = [
    "★", "♦", "♣", "♠", "♥", "●", "▲", "■",
    "◆", "○", "△", "□", "☀", "☁", "☂", "☃",
    "✿", "❀", "⚡", "⚙", "✈", "☎", "✉", "♬",
    "⚽", "⚾", "☯", "♛", "♞", "⚓", "✂", "⌛",
    "☮", "✦", "❖", "⬟", "⬡", "◎", "❂", "✪",
    "⧫", "⬣", "☘", "⚜", "♕", "♔", "♖", "♗",
    "♘", "♙", "⚔", "⛵"
]


class Card:

    def __init__(self, symbol: str, row: int, col: int):
        self.symbol = symbol
        self.row = row
        self.col = col
        self.is_face_up = False
        self.is_matched = False

    def flip_up(self):
        self.is_face_up = True

    def flip_down(self):
        if not self.is_matched:
            self.is_face_up = False

    def __repr__(self):
        return f"Card({self.symbol}, ({self.row},{self.col}), up={self.is_face_up}, matched={self.is_matched})"


class Board:

    def __init__(self, n_rows: int, n_cols: int):
        if (n_rows * n_cols) % 2 != 0:
            raise ValueError("Board size (nRows * nCols) must be even.")

        self.n_rows = n_rows
        self.n_cols = n_cols
        self.total_cards = n_rows * n_cols
        self.total_pairs = self.total_cards // 2
        self.matched_pairs = 0
        self.grid = self._create_board()

    def _create_board(self) -> list:
        if self.total_pairs > len(SYMBOLS):
            raise ValueError(
                f"Not enough symbols. Max board size supported: {len(SYMBOLS) * 2} cards."
            )

        selected_symbols = random.sample(SYMBOLS, self.total_pairs)

        card_symbols = selected_symbols * 2
        random.shuffle(card_symbols)

        grid = []
        idx = 0
        for row in range(self.n_rows):
            row_cards = []
            for col in range(self.n_cols):
                card = Card(card_symbols[idx], row, col)
                row_cards.append(card)
                idx += 1
            grid.append(row_cards)

        return grid

    def get_card(self, row: int, col: int) -> Card:
        return self.grid[row][col]

    def check_match(self, card1: Card, card2: Card) -> bool:
        if card1.symbol == card2.symbol:
            card1.is_matched = True
            card2.is_matched = True
            self.matched_pairs += 1
            return True
        return False

    def is_complete(self) -> bool:
        return self.matched_pairs == self.total_pairs

    def reset(self):
        self.matched_pairs = 0
        self.grid = self._create_board()
