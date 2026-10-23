import customtkinter as ctk
from functions import show_clients

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("900x600")
app.title("Управление Фотостудией")

app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)


sidebar_frame = ctk.CTkFrame(app, width=200, corner_radius=0)
sidebar_frame.grid(row=0, column=0, sticky="nsew")

logo_label = ctk.CTkLabel(sidebar_frame, text="PhotoStudio Pro", font=("Papyrus", 20, "bold"))
logo_label.pack(pady=20, padx=20)

btn_clients = ctk.CTkButton(sidebar_frame, text="Клиенты", font=("Comic Sans MS", 14), command=lambda: show_clients(main_frame))
btn_clients.pack(pady=10, padx=20)

btn_schedule = ctk.CTkButton(sidebar_frame, text="Расписание", font=("Comic Sans MS", 14))
btn_schedule.pack(pady=10, padx=20)

btn_photo = ctk.CTkButton(sidebar_frame, text="Обработка фото", font=("Comic Sans MS", 14))
btn_photo.pack(pady=10, padx=20)


main_frame = ctk.CTkFrame(app, corner_radius=0, fg_color="transparent")
main_frame.grid(row=0, column=1, sticky="nsew")

welcome_lable = ctk.CTkLabel(main_frame, text="Добро пожаловать!\nВыберите раздел слева.", font=("Comic Sans MS", 24))
welcome_lable.pack(expand=True)

app.mainloop()