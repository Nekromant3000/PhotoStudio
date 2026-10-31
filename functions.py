import customtkinter as ctk
from database import add_client

def show_clients(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    title = ctk.CTkLabel(main_frame, text="Управление клиентами", font=("Comic Sans MS", 24, "bold"))
    title.pack(pady=20)

    name_entry = ctk.CTkEntry(main_frame, placeholder_text="Имя клиента", width=250)
    name_entry.pack(pady=10)

    phone_entry = ctk.CTkEntry(main_frame, placeholder_text="Телефон клиента", width=250)
    phone_entry.pack(pady=10)

    def save_btn_clicked():
        client_name = name_entry.get()
        client_phone = phone_entry.get()

        if client_name != "":
            add_client(client_name, client_phone)

            name_entry.delete(0, 'end')
            phone_entry.delete(0, 'end')

            print("[UI] Форма очищена, ожидание нового ввода.")
        else:
            print("[UI] Ошибка: Имя не может быть пустым!")

    add_btn = ctk.CTkButton(main_frame, text="Добавить клиента", font=("Comic Sans MS", 14), command=save_btn_clicked)
    add_btn.pack(pady=20)