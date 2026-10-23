import customtkinter as ctk

def show_clients(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()
    title = ctk.CTkLabel(main_frame, text="Управление клиентами", font=("Comic Sans MS", 24, "bold"))
    title.pack(pady=20)

    add_btn = ctk.CTkButton(main_frame, text="Добавить клиента", font=("Comic Sans MS", 14))
    add_btn.pack(pady=10)