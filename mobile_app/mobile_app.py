import customtkinter as ctk
import database
from functions_clients import new_entry, show_photo
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Инициализация БДшки
database.create_tables()
database.seed_data()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x720")
app.title("PhotoStudio Mobile (Клиент)")
app.resizable(False, False)

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

# Основная область
main_frame = ctk.CTkFrame(app, corner_radius=0, fg_color="#18181b")
main_frame.grid(row=0, column=0, sticky="nsew")

# Навигация
nav_bar = ctk.CTkFrame(app, height=60, corner_radius=0, fg_color="#27272a")
nav_bar.grid(row=1, column=0, sticky="ew")
nav_bar.grid_columnconfigure((0, 1), weight=1)

def switch_to_portfolio():
    btn_nav_photo.configure(fg_color="#3b82f6")
    btn_nav_entry.configure(fg_color="transparent")
    show_photo(main_frame)

def switch_to_entry():
    btn_nav_entry.configure(fg_color="#3b82f6")
    btn_nav_photo.configure(fg_color="transparent")
    new_entry(main_frame)

btn_nav_photo = ctk.CTkButton(
    nav_bar, text="Галерея", font=("Arial", 13, "bold"),
    fg_color="#3b82f6", hover_color="#2563eb",
    command=switch_to_portfolio
)
btn_nav_photo.grid(row=0, column=0, padx=8, pady=10, sticky="ew")

btn_nav_entry = ctk.CTkButton(
    nav_bar, text="Онлайн-запись", font=("Arial", 13, "bold"),
    fg_color="transparent", hover_color="#3f3f46",
    command=switch_to_entry
)
btn_nav_entry.grid(row=0, column=1, padx=8, pady=10, sticky="ew")

# Стартовый экран
switch_to_portfolio()

if __name__ == "__main__":
    app.mainloop()