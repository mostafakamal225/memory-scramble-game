import tkinter as tk
from tkinter import messagebox


class ConfigDialog:
    

    def __init__(self, parent):
        self.result = None
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Memory Scramble - Configuration")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_close)

        
        self.dialog.geometry("400x300")
        self.dialog.lift()
        self.dialog.attributes('-topmost', True)
        self.dialog.after(100, lambda: self.dialog.attributes('-topmost', False))
        self.dialog.focus_force()

        self._create_widgets()

    def _create_widgets(self):
        
        
        title_label = tk.Label(
            self.dialog,
            text="Memory Scramble",
            font=("Helvetica", 18, "bold")
        )
        title_label.pack(pady=(20, 5))

        subtitle_label = tk.Label(
            self.dialog,
            text="Configure your game",
            font=("Helvetica", 10)
        )
        subtitle_label.pack(pady=(0, 20))
        
        settings_frame = tk.Frame(self.dialog)
        settings_frame.pack(padx=40, fill="x")

        row_frame = tk.Frame(settings_frame)
        row_frame.pack(fill="x", pady=5)
        tk.Label(row_frame, text="Number of Rows:", width=18, anchor="w").pack(side="left")
        self.rows_var = tk.StringVar(value="4")
        rows_entry = tk.Entry(row_frame, textvariable=self.rows_var, width=10)
        rows_entry.pack(side="left", padx=(10, 0))

        col_frame = tk.Frame(settings_frame)
        col_frame.pack(fill="x", pady=5)
        tk.Label(col_frame, text="Number of Columns:", width=18, anchor="w").pack(side="left")
        self.cols_var = tk.StringVar(value="4")
        cols_entry = tk.Entry(col_frame, textvariable=self.cols_var, width=10)
        cols_entry.pack(side="left", padx=(10, 0))

        time_frame = tk.Frame(settings_frame)
        time_frame.pack(fill="x", pady=5)
        tk.Label(time_frame, text="Time Limit (seconds):", width=18, anchor="w").pack(side="left")
        self.time_var = tk.StringVar(value="60")
        time_entry = tk.Entry(time_frame, textvariable=self.time_var, width=10)
        time_entry.pack(side="left", padx=(10, 0))

        note_label = tk.Label(
            self.dialog,
            text="Note: Total cells (rows × columns) must be even.",
            font=("Helvetica", 9, "italic"),
            fg="gray"
        )
        note_label.pack(pady=(15, 5))

        start_btn = tk.Button(
            self.dialog,
            text="Start Game",
            font=("Helvetica", 12, "bold"),
            command=self._on_start,
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5
        )
        start_btn.pack(pady=15)

    def _on_start(self):
        """Validate inputs and start the game."""
        try:
            n_rows = int(self.rows_var.get())
            n_cols = int(self.cols_var.get())
            timeout = int(self.time_var.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter valid integer values for all fields.",
                parent=self.dialog
            )
            return

        if n_rows < 2 or n_cols < 2:
            messagebox.showerror(
                "Invalid Size",
                "Rows and columns must be at least 2.",
                parent=self.dialog
            )
            return

        if (n_rows * n_cols) % 2 != 0:
            messagebox.showerror(
                "Invalid Size",
                "Total number of cells (rows × columns) must be even.",
                parent=self.dialog
            )
            return

        if n_rows * n_cols > 104:
            messagebox.showerror(
                "Size Too Large",
                "Maximum supported board size is 104 cells (52 pairs).",
                parent=self.dialog
            )
            return

        if timeout < 10:
            messagebox.showerror(
                "Invalid Timeout",
                "Timeout must be at least 10 seconds.",
                parent=self.dialog
            )
            return

        self.result = {
            "n_rows": n_rows,
            "n_cols": n_cols,
            "timeout": timeout
        }
        self.dialog.destroy()

    def _on_close(self):
        """Handle dialog close via window manager."""
        self.result = None
        self.dialog.destroy()

    def show(self):
        """Show the dialog and wait for it to close."""
        self.dialog.wait_window()
        return self.result
