import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.history_file = "password_history.json"
        
        self.length_var = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)

        self.setup_ui()
        self.load_history()
    
    def setup_ui(self):
        ttk.Label(self.root, text="Длина пароля:").pack(pady=5)
        self.slider = ttk.Scale(self.root, from_=4, to=32, variable=self.length_var, orient='horizontal', command=self.update_label)
        self.slider.pack(fill="x", padx=20)
        self.len_label = ttk.Label(self.root, text='12')
        self.len_label.pack()

        ttk.Checkbutton(self.root, text='Цифры', variable=self.use_digits).pack(anchor='w', padx=20)
        ttk.Checkbutton(self.root, text='Буквы', variable=self.use_letters).pack(anchor='w', padx=20)
        ttk.Checkbutton(self.root, text='Специальные символы', variable=self.use_special).pack(anchor='w', padx=20)

        ttk.Button(self.root, text='Генерация пароля', command=self.generate_password).pack(pady=10)

        self.password_out = ttk.Entry(self.root, font=("Times New Roman", 12))
        self.password_out.pack(pady=5, padx=20, fill="x")

        ttk.Label(self.root, text="История:").pack(pady=5)
        self.tree = ttk.Treeview(self.root, columns=('Password'), show='headings')
        self.tree.heading("Password", text='Сгенерированные пароли')
        self.tree.pack(padx=20, pady=10, fill="both", expand=True)
    
    def update_label(self, event):
        self.len_label.config(text=str(int(self.length_var.get())))

    def generate_password(self):
        length = int(self.length_var.get())
        chars = ""
        if self.use_digits.get(): chars += string.digits
        if self.use_letters.get(): chars += string.ascii_letters
        if self.use_special.get(): chars += string.punctuation

        if not chars:
            messagebox.showwarning( "Выбери хотя бы один тип символов")
            return

        password = "".join(random.choice(chars) for _ in range(length))
        self.password_out.delete(0, tk.END)
        self.password_out.insert(0, password)
        self.save_to_history(password)

    def save_to_history(self, password):
        self.tree.insert("", 0, values=(password,))
        history = []
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                try: 
                    history = json.load(f)
                except: 
                    history = []
        history.append(password)
        with open(self.history_file, "w") as f:
            json.dump(history, f)

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                try:
                    history = json.load(f)
                    for p in history:
                        self.tree.insert("", 0, values=(p,))
                except: 
                    pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()


