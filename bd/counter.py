import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

class CounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Счётчик")
        self.root.geometry("340x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f0f0f")

        self.db_name = "counter.db"
        self.setup_database()

        self.count = 0
        self.current_customer_id = 1 # ID текущего пользователя в БД
        self.load_from_db()

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

        save_btn = self.create_button(root, "Сохранить", "#2c2c2e", self.save_to_db, width=12, height=1)
        save_btn.pack(pady=25)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_database(self):
        """Создает таблицы и начальные данные, если их нет"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Таблица 1: Пользователи (Счетчики)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    current_value INTEGER DEFAULT 0
                )
            ''')
            
            # Таблица 2: История изменений (FK)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    action TEXT NOT NULL,
                    value_after INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(customer_id) REFERENCES customers(id)
                )
            ''')
            
            # Если пользователей нет, добавляем первого (id=1)
            cursor.execute("SELECT COUNT(*) FROM customers")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO customers (name, current_value) VALUES ('Мой счетчик', 0)")
            
            conn.commit()

    def load_from_db(self):
        """Загружает значение из БД при запуске"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT current_value FROM customers WHERE id = ?", (self.current_customer_id,))
                result = cursor.fetchone()
                if result:
                    self.count = result[0]
        except Exception as e:
            print(f"Ошибка загрузки: {e}")

    def log_history(self, action, value):
        """Записывает действие в таблицу истории"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO history (customer_id, action, value_after) VALUES (?, ?, ?)",
                    (self.current_customer_id, action, value)
                )
                conn.commit()
        except Exception as e:
            print(f"Ошибка записи истории: {e}")

    def save_to_db(self):
        """Сохраняет текущее значение в основную таблицу"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE customers SET current_value = ? WHERE id = ?",
                    (self.count, self.current_customer_id)
                )
                conn.commit()
            messagebox.showinfo("Сохранено", "Значение и история записаны в БД")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

    def create_button(self, parent, text, color, command, width=5, height=2):
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

    def update_display(self):
        self.display.config(text=str(self.count))

    def increase(self):
        self.count += 1
        self.root.bell()
        self.update_display()
        self.log_history("increase", self.count)

    def decrease(self):
        if self.count > 0:
            self.count -= 1
            self.root.bell()
            self.update_display()
            self.log_history("decrease", self.count)
        else:
            self.root.bell()
            messagebox.showinfo("Ограничение", "Нельзя уходить в минус")

    def change(self, value):
        new_value = self.count + value
        if new_value < 0:
            self.count = 0
            messagebox.showinfo("Ограничение", "Нельзя уходить в минус")
        else:
            self.count = new_value
        self.root.bell()
        self.update_display()
        self.log_history(f"change_{value}", self.count)

    def reset(self):
        self.count = 0
        self.root.bell()
        self.update_display()
        self.log_history("reset", self.count)

    def on_closing(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CounterApp(root)
    root.mainloop()