import customtkinter as ctk
from database import add_client, get_all_clients, get_all_photographers,  get_all_services, add_booking
from tkinter import filedialog
from PIL import Image

def show_clients(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    title = ctk.CTkLabel(main_frame, text="Управление клиентами", font=("Comic Sans MS", 24, "bold"))
    title.pack(pady=10)

    name_entry = ctk.CTkEntry(main_frame, placeholder_text="Имя клиента", width=250)
    name_entry.pack(pady=5)

    phone_entry = ctk.CTkEntry(main_frame, placeholder_text="Телефон клиента (например: 89991234567)", width=250)
    phone_entry.pack(pady=5)

    def save_btn_clicked():
        client_name = name_entry.get()
        client_phone = phone_entry.get()

        if client_name != "":
            add_client(client_name, client_phone)
            print("[UI] Клиент сохранён.")
            show_clients(main_frame)
        else:
            print("[UI] Ошибка: Имя не может быть пустым!")

    add_btn = ctk.CTkButton(main_frame, text="Добавить клиента", font=("Comic Sans MS", 14), command=save_btn_clicked)
    add_btn.pack(pady=10)

    table_label = ctk.CTkLabel(main_frame, text="Список клиентов:", font=("Comic Sans MS", 16, "bold"))
    table_label.pack(pady=(20, 5))

    scroll_frame = ctk.CTkScrollableFrame(main_frame, width=400, height=200)
    scroll_frame.pack(pady=5, fill="both", expand=True)

    ctk.CTkLabel(scroll_frame, text="ID", font=("Comic Sans MS", 14, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(scroll_frame, text="Имя", font=("Comic Sans MS", 14, "bold")).grid(row=0, column=1, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(scroll_frame, text="Телефон", font=("Comic Sans MS", 14, "bold")).grid(row=0, column=2, padx=10, pady=5, sticky="w")

    clients = get_all_clients()

    for index, client in enumerate(clients):
        row_num = index + 1

        client_id = str(client[0])
        client_name = client[1]
        client_phone = client[2]

        ctk.CTkLabel(scroll_frame, text=client_id, font=("Comic Sans MS", 14)).grid(row=row_num, column=0, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(scroll_frame, text=client_name, font=("Comic Sans MS", 14)).grid(row=row_num, column=1, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(scroll_frame, text=client_phone, font=("Comic Sans MS", 14)).grid(row=row_num, column=2, padx=10, pady=2, sticky="w")

def show_schedule(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()

    title = ctk.CTkLabel(main_frame, text="Расписание и запись", font=("Comic Sans MS", 24, "bold"))
    title.pack(pady=20)

    clients = get_all_clients()
    photographers = get_all_photographers()
    services = get_all_services()

    client_list = [f"{c[0]}: {c[1]}" for c in clients]
    photo_list = [f"{p[0]}: {p[1]}" for p in photographers]
    service_list = [f"{s[0]}: {s[1]}" for s in services]

    client_combo = ctk.CTkComboBox(main_frame, values=client_list, width=250)
    client_combo.pack(pady=10)
    client_combo.set("Выберете клиента")

    photo_combo = ctk.CTkComboBox(main_frame, values=photo_list, width=250)
    photo_combo.pack(pady=10)
    photo_combo.set("Выберете фотографа")

    service_combo = ctk.CTkComboBox(main_frame, values=service_list, width=250)
    service_combo.pack(pady=10)
    service_combo.set("Выберете услугу")

    date_entry = ctk.CTkEntry(main_frame, placeholder_text="Дата (ГГГГ-ММ-ДД ЧЧ:ММ)", width=250)
    date_entry.pack(pady=10)

    def book_clicked():
        client_id = client_combo.get().split(":")[0]
        photo_id = photo_combo.get().split(":")[0]
        service_id = service_combo.get().split(":")[0]
        date = date_entry.get()

        if "Выберите" not in client_id and date != "":
            add_booking(client_id, photo_id, service_id, date)
            print("[UI] Запись успешно оформлена.")
            date_entry.delete(0, 'end')
        else:
            print("[UI] Ошибка: Заполните все поля корректно.")

    btn = ctk.CTkButton(main_frame, text="Записать", font=("Comic Sans MS", 14), command=book_clicked)
    btn.pack(pady=20)

def show_photo_tab(main_frame):
    for widget in main_frame.winfo_children():
            widget.destroy()

    title = ctk.CTkLabel(main_frame, text="Обработка фотографий", font=("Comic Sans MS", 24, "bold"))
    title.pack(pady=20)

    file_path_var = ctk.StringVar(value="Файл не выбран")

    def choose_file():
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if path:
            file_path_var.set(path)

    def convert_to_png():
        current_path = file_path_var.get()
        if current_path != "Файл не выбран":
            img = Image.open(current_path)
            new_path = current_path.rsplit('.', 1)[0] + "_converted.png"
            img.save(new_path, "PNG")
            file_path_var.set(f"Сохранено как: \n{new_path}")
            print(f"Файл конвертирован: {new_path}")

    choose_btn = ctk.CTkButton(main_frame, text="Выбрать фото", font=("Comic Sans MS", 14), command=choose_file)
    choose_btn.pack(pady=10)

    path_label = ctk.CTkLabel(main_frame, textvariable=file_path_var, text_color="gray")
    path_label.pack(pady=10)

    convert_btn = ctk.CTkButton(main_frame, text="Конвертировать в PNG", font=("Comic Sans MS", 14), command=convert_to_png)
    convert_btn.pack(pady=10)