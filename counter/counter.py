import tkinter as tk
from tkinter import messagebox
import os

class CounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Счётчик")
        self.root.geometry("340x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f0f0f")

        self.count = 0
        self.save_file = "counter_save.txt"
        self.load_value()

        tk.Label(
            root,
            text="Счётчик",
            font=("Arial", 26, "bold"),
            bg="#0f0f0f",
            fg="#00e5ff"
        ).pack(pady=(20, 10))

        display_frame = tk.Frame(root, bg="#1a1a1a", padx=10, pady=10)
        display_frame.pack(padx=40, fill="x")

        self.display = tk.Label(
            display_frame,
            text=str(self.count),
            font=("Arial", 64, "bold"),
            bg="#1a1a1a",
            fg="#00e5ff",
            width=6
        )
        self.display.pack(pady=10)

        btn_frame = tk.Frame(root, bg="#0f0f0f")
        btn_frame.pack(pady=20)

        self.create_button(btn_frame, "−", "#ff3b30", self.decrease).grid(row=0, column=0, padx=10)
        self.create_button(btn_frame, "Сброс", "#333333", self.reset, width=8).grid(row=0, column=1, padx=10)
        self.create_button(btn_frame, "+", "#30d158", self.increase).grid(row=0, column=2, padx=10)

        extra_frame = tk.Frame(root, bg="#0f0f0f")
        extra_frame.pack(pady=15)

        self.create_button(extra_frame, "+10", "#30d158", lambda: self.change(10), width=8).pack(side="left", padx=12)
        self.create_button(extra_frame, "−10", "#ff3b30", lambda: self.change(-10), width=8).pack(side="left", padx=12)

        save_btn = self.create_button(root, "Сохранить", "#2c2c2e", self.save_value, width=12, height=1)
        save_btn.pack(pady=25)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_button(self, parent, text, color, command, width=5, height=2):
        # На macOS стандартные tk.Button плохо красятся, поэтому используем Label
        btn = tk.Label(
            parent,
            text=text,
            font=("Arial", 16, "bold"),
            bg=color,
            fg="white",
            width=width,
            height=height,
            cursor="hand2"
        )
        
        def on_enter(e):
            btn.config(bg=self.darken(color))
        
        def on_leave(e):
            btn.config(bg=color)
            
        def on_click(e):
            command()
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", on_click)
        
        return btn

    def darken(self, hex_color):
        hex_color = hex_color.lstrip('#')
        r = max(0, int(hex_color[0:2], 16) - 30)
        g = max(0, int(hex_color[2:4], 16) - 30)
        b = max(0, int(hex_color[4:6], 16) - 30)
        return f"#{r:02x}{g:02x}{b:02x}"

    def play_sound(self):
        self.root.bell()

    def update_display(self):
        self.display.config(text=str(self.count))

    def increase(self):
        self.count += 1
        self.play_sound()
        self.update_display()

    def decrease(self):
        if self.count > 0:
            self.count -= 1
            self.play_sound()
            self.update_display()
        else:
            self.play_sound()
            messagebox.showinfo("Ограничение", "Нельзя уходить в минус")

    def change(self, value):
        new_value = self.count + value
        if new_value < 0:
            self.count = 0
            messagebox.showinfo("Ограничение", "Нельзя уходить в минус")
        else:
            self.count = new_value
        self.play_sound()
        self.update_display()

    def reset(self):
        self.count = 0
        self.play_sound()
        self.update_display()

    def save_value(self):
        try:
            with open(self.save_file, "w", encoding="utf-8") as f:
                f.write(str(self.count))
            messagebox.showinfo("Сохранено", "Значение успешно сохранено")
        except:
            messagebox.showerror("Ошибка", "Не удалось сохранить значение")

    def load_value(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r", encoding="utf-8") as f:
                    self.count = int(f.read().strip())
            except:
                self.count = 0

    def on_closing(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CounterApp(root)
    root.mainloop()