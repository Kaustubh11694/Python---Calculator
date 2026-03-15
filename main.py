import tkinter as tk
from tkinter import font

class CircleButton(tk.Canvas):
    def __init__(self, master, text, command=None, outline_color="#00BFFF", fill_color="#FFFFFF", **kwargs):
        super().__init__(master, width=60, height=60, highlightthickness=0, bg=master['bg'])
        self.command = command
        self.text = text
        self.outline_color = outline_color
        self.fill_color = fill_color
        self.circle = self.create_oval(5, 5, 55, 55, outline=outline_color, width=3, fill=fill_color)
        self.label = self.create_text(30, 30, text=text, font=("Segoe UI", 18, "bold"), fill="#222")
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", lambda e: self.itemconfig(self.circle, outline="#FF4500"))
        self.bind("<Leave>", lambda e: self.itemconfig(self.circle, outline=outline_color))

    def _on_click(self, event):
        if self.command:
            self.command(self.text)

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Elegant Calculator")
        self.configure(bg="#F5F5F5")
        self.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        self.display_var = tk.StringVar()
        display_font = font.Font(family="Segoe UI", size=22, weight="bold")
        display = tk.Entry(self, textvariable=self.display_var, font=display_font, bd=0, bg="#FFFFFF", fg="#222", justify="right")
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=12, pady=(12, 6))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        btns = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('C', 4, 1), ('=', 4, 2), ('+', 4, 3),
        ]

        for (text, row, col) in btns:
            if text.isdigit():
                btn = CircleButton(self, text, command=self._on_button, outline_color="#00BFFF", fill_color="#E6F7FF")
            elif text == 'C':
                btn = CircleButton(self, text, command=self._on_clear, outline_color="#FF6347", fill_color="#FFF5F5")
            elif text == '=':
                btn = CircleButton(self, text, command=self._on_equal, outline_color="#32CD32", fill_color="#F5FFF5")
            else:
                btn = CircleButton(self, text, command=self._on_button, outline_color="#FFD700", fill_color="#FFFBE6")
            btn.grid(row=row, column=col, padx=10, pady=10)

        for i in range(1, 5):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def _on_button(self, value):
        current = self.display_var.get()
        self.display_var.set(current + value)

    def _on_clear(self, _):
        self.display_var.set("")

    def _on_equal(self, _):
        try:
            result = eval(self.display_var.get())
            self.display_var.set(str(result))
        except Exception:
            self.display_var.set("Error")

class CalculatorWithHistory(Calculator):
    def __init__(self):
        self.history = []
        super().__init__()

    def _on_equal(self, _):
        expr = self.display_var.get()
        try:
            result = eval(expr)
            self.display_var.set(str(result))
            self._add_to_history(expr, result)
        except Exception:
            self.display_var.set("Error")

    def _add_to_history(self, expr, result):
        entry = f"{expr} = {result}"
        self.history.append(entry)
        if len(self.history) > 3:
            self.history.pop(0)
        self._update_history_display()

    def _build_ui(self):
        super()._build_ui()
        self.history_var = tk.StringVar()
        history_label = tk.Label(self, textvariable=self.history_var, font=("Segoe UI", 12), bg="#F5F5F5", fg="#888", anchor="w", justify="left")
        history_label.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=12, pady=(0, 12))
        self.grid_rowconfigure(5, weight=0)
        self._update_history_display()

    def _update_history_display(self):
        if self.history:
            self.history_var.set("History:\n" + "\n".join(self.history))
        else:
            self.history_var.set("History:")

if __name__ == "__main__":
    CalculatorWithHistory().mainloop()