import customtkinter as ctk
from database import add_client, get_all_clients, delete_client, update_client, add_photographer, get_all_photographers,  delete_photographer, update_photographer, add_service, get_all_services, delete_service, update_service, add_booking, get_all_bookings, delete_booking
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont

def show_clients(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    title = ctk.CTkLabel(main_frame, text="Управление клиентами", font=("Comic Sans MS", 24, "bold"))
    title.pack(pady=10)

    name_entry = ctk.CTkEntry(main_frame, placeholder_text="Имя клиента", width=250)
    name_entry.pack(pady=5)

    phone_entry = ctk.CTkEntry(main_frame, placeholder_text="Телефон клиента (например: 89991234567)", width=250)
    phone_entry.pack(pady=5)

    current_edit_id = None

    def save_btn_clicked():
        nonlocal current_edit_id
        client_name = name_entry.get()
        client_phone = phone_entry.get()

        if client_name != "":
            if current_edit_id is None:
                add_client(client_name, client_phone)
                print("[UI] Клиент сохранён.")
            else:
                update_client(current_edit_id, client_name, client_phone)
                print(f"[UI] Клиент {current_edit_id} обновлён.")
                current_edit_id = None

            show_clients(main_frame)
        else:
            print("[UI] Ошибка: Имя не может быть пустым!")

    add_btn = ctk.CTkButton(main_frame, text="Сохранить", font=("Comic Sans MS", 14), command=save_btn_clicked)
    add_btn.pack(pady=10)

    table_label = ctk.CTkLabel(main_frame, text="Список клиентов:", font=("Comic Sans MS", 16, "bold"))
    table_label.pack(pady=(20, 5))

    scroll_frame = ctk.CTkScrollableFrame(main_frame, width=400, height=200)
    scroll_frame.pack(pady=5, fill="both", expand=True)

    ctk.CTkLabel(scroll_frame, text="ID", font=("Comic Sans MS", 14, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(scroll_frame, text="Имя", font=("Comic Sans MS", 14, "bold")).grid(row=0, column=1, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(scroll_frame, text="Телефон", font=("Comic Sans MS", 14, "bold")).grid(row=0, column=2, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(scroll_frame, text="Действия", font=("Comic Sans MS", 14, "bold")).grid(row=0, column=3, padx=10, pady=5, sticky="w")

    clients = get_all_clients()

    def edit_action(c_id, c_name, c_phone):
        nonlocal current_edit_id
        current_edit_id = c_id

        name_entry.delete(0, 'end')
        name_entry.insert(0, c_name)
        phone_entry.delete(0, 'end')
        phone_entry.insert(0, c_phone)
        add_btn.configure(text="Обновить данные")

    def delete_action(c_id):
        delete_client(c_id)
        print("[UI] Клиент удалён.")
        show_clients(main_frame)

    for index, client in enumerate(clients):
        row_num = index + 1

        c_id = client[0]
        c_name = client[1]
        c_phone = client[2]

        ctk.CTkLabel(scroll_frame, text=str(c_id), font=("Comic Sans MS", 14)).grid(row=row_num, column=0, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(scroll_frame, text=c_name, font=("Comic Sans MS", 14)).grid(row=row_num, column=1, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(scroll_frame, text=c_phone, font=("Comic Sans MS", 14)).grid(row=row_num, column=2, padx=10, pady=2, sticky="w")

        action_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        action_frame.grid(row=row_num, column=3, padx=10, pady=2, sticky="w")

        edit_btn = ctk.CTkButton(action_frame, text="Изменить", width=60, command=lambda id=c_id, n=c_name, p=c_phone: edit_action(id, n, p))
        edit_btn.pack(side="left", padx=2)

        del_btn = ctk.CTkButton(action_frame, text="Удалить", fg_color="red", width=60, command=lambda id=c_id: delete_action(id))
        del_btn.pack(side="left", padx=2)

def show_photographers(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    title = ctk.CTkLabel(main_frame, text="Управление фотографами", font=("Comic Sans MS", 24, "bold"))
    title.pack(pady=10)

    name_entry = ctk.CTkEntry(main_frame, placeholder_text="Имя фотографа", width=250)
    name_entry.pack(pady=5)

    spec_entry = ctk.CTkEntry(main_frame, placeholder_text="Специализация (например: Свадьбы)", width=250)
    spec_entry.pack(pady=5)
    
    link_entry = ctk.CTkEntry(main_frame, placeholder_text="Ссылка на портфолио (например: C:/photos/anna)", width=250)
    link_entry.pack(pady=5)

    current_edit_id = None

    def save_btn_clicked():
        nonlocal current_edit_id
        p_name = name_entry.get()
        p_spec = spec_entry.get()
        p_link = link_entry.get()

        if p_name != "":
            if current_edit_id is None:
                add_photographer(p_name, p_spec, p_link)
                print("[UI] Фотограф сохранён.")
            else:
                update_photographer(current_edit_id, p_name, p_spec, p_link)
                print(f"[UI] Фотограф {current_edit_id} обновлён.")
                current_edit_id = None
            show_photographers(main_frame)
        else:
            print("[UI] Ошибка: Имя не может быть пустым.")

    add_btn = ctk.CTkButton(main_frame, text="Сохранить", font=("Comic Sans MS", 14), command=save_btn_clicked)
    add_btn.pack(pady=10)

    table_label = ctk.CTkLabel(main_frame, text="Список фотографов:", font=("Comic Sans MS", 16, "bold"))
    table_label.pack(pady=(20, 5))

    scroll_frame = ctk.CTkScrollableFrame(main_frame, width=400, height=200)
    scroll_frame.pack(pady=5, fill="both", expand=True)

    ctk.CTkLabel(scroll_frame, text="ID", font=("Comic Sans MS", 14, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(scroll_frame, text="Имя", font=("Comic Sans MS", 14, "bold")).grid(row=0, column=1, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(scroll_frame, text="Спец-ть", font=("Comic Sans MS", 14, "bold")).grid(row=0, column=2, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(scroll_frame, text="Портфолио", font=("Comic Sans MS", 14, "bold")).grid(row=0, column=3, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(scroll_frame, text="Действия", font=("Comic Sans MS", 14, "bold")).grid(row=0, column=4, padx=10, pady=5, sticky="w")

    photographers = get_all_photographers()

    def edit_action(p_id, p_name, p_spec, p_link):
        nonlocal current_edit_id
        current_edit_id = p_id
        name_entry.delete(0, 'end')
        name_entry.insert(0, p_name)
        spec_entry.delete(0, 'end')
        spec_entry.insert(0, p_spec)
        link_entry.delete(0, 'end')
        link_entry.insert(0, p_link)
        add_btn.configure(text="Обновить данные")

    def delete_action(p_id):
        delete_photographer(p_id)
        print("[UI] Фотограф удалён.")
        show_photographers(main_frame)

    for index, photo in enumerate(photographers):
        row_num = index + 1
        p_id, p_name, p_spec, p_link = photo[0], photo[1], photo[2], photo[3]

        ctk.CTkLabel(scroll_frame, text=str(p_id), font=("Comic Sans MS", 14)).grid(row=row_num, column=0, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(scroll_frame, text=p_name, font=("Comic Sans MS", 14)).grid(row=row_num, column=1, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(scroll_frame, text=p_spec, font=("Comic Sans MS", 14)).grid(row=row_num, column=2, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(scroll_frame, text=p_link, font=("Comic Sans MS", 14)).grid(row=row_num, column=3, padx=10, pady=2, sticky="w")

        action_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        action_frame.grid(row=row_num, column=4, padx=10, pady=2, sticky="w")

        edit_btn = ctk.CTkButton(action_frame, text="Изменить", width=60, command=lambda id=p_id, n=p_name, s=p_spec, l=p_link: edit_action(id, n, s, l))
        edit_btn.pack(side="left", padx=2)
        del_btn = ctk.CTkButton(action_frame, text="Удалить", fg_color="red", width=60, command=lambda id=p_id: delete_action(id))
        del_btn.pack(side="left", padx=2)

def show_services(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    title = ctk.CTkLabel(main_frame, text="Управление услугами", font=("Comic Sans MS", 24, "bold"))
    title.pack(pady=10)

    title_entry = ctk.CTkEntry(main_frame, placeholder_text="Название услуги", width=250)
    title_entry.pack(pady=5)

    price_entry = ctk.CTkEntry(main_frame, placeholder_text="Цена (руб)", width=250)
    price_entry.pack(pady=5)

    current_edit_id = None

    def save_btn_clicked():
        nonlocal current_edit_id
        s_title = title_entry.get()
        s_price = price_entry.get()

        if s_title != "" and s_price != "":
            if current_edit_id is None:
                add_service(s_title, s_price)
                print("[UI] Услуга сохранёна.")
            else:
                update_service(current_edit_id, s_title, s_price)
                print(f"[UI] Услуга {current_edit_id} обновлёна.")
                current_edit_id = None
            show_services(main_frame)
        else:
            print("[UI] Ошибка: Заполните все поля.")

    add_btn = ctk.CTkButton(main_frame, text="Сохранить", font=("Comic Sans MS", 14), command=save_btn_clicked)
    add_btn.pack(pady=10)

    table_label = ctk.CTkLabel(main_frame, text="Список услуг:", font=("Comic Sans MS", 16, "bold"))
    table_label.pack(pady=(20, 5))

    scroll_frame = ctk.CTkScrollableFrame(main_frame, width=400, height=200)
    scroll_frame.pack(pady=5, fill="both", expand=True)

    ctk.CTkLabel(scroll_frame, text="ID", font=("Comic Sans MS", 14, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(scroll_frame, text="Название", font=("Comic Sans MS", 14, "bold")).grid(row=0, column=1, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(scroll_frame, text="Цена", font=("Comic Sans MS", 14, "bold")).grid(row=0, column=2, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(scroll_frame, text="Действия", font=("Comic Sans MS", 14, "bold")).grid(row=0, column=3, padx=10, pady=5, sticky="w")

    services = get_all_services()

    def edit_action(s_id, s_title, s_price):
        nonlocal current_edit_id
        current_edit_id = s_id
        title_entry.delete(0, 'end')
        title_entry.insert(0, s_title)
        price_entry.delete(0, 'end')
        price_entry.insert(0, s_price)
        add_btn.configure(text="Обновить данные")

    def delete_action(s_id):
        delete_service(s_id)
        print("[UI] Услуга удалёна.")
        show_services(main_frame)

    for index, service in enumerate(services):
        row_num = index + 1
        s_id, s_title, s_price = service[0], service[1], service[2]

        ctk.CTkLabel(scroll_frame, text=str(s_id), font=("Comic Sans MS", 14)).grid(row=row_num, column=0, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(scroll_frame, text=s_title, font=("Comic Sans MS", 14)).grid(row=row_num, column=1, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(scroll_frame, text=str(s_price), font=("Comic Sans MS", 14)).grid(row=row_num, column=2, padx=10, pady=2, sticky="w")

        action_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        action_frame.grid(row=row_num, column=3, padx=10, pady=2, sticky="w")

        edit_btn = ctk.CTkButton(action_frame, text="Изменить", width=60, command=lambda id=s_id, t=s_title, p=s_price: edit_action(id, t, p))
        edit_btn.pack(side="left", padx=2)
        del_btn = ctk.CTkButton(action_frame, text="Удалить", fg_color="red", width=60, command=lambda id=s_id: delete_action(id))
        del_btn.pack(side="left", padx=2)

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

    schedule_label = ctk.CTkLabel(main_frame, text="Текущие записи:", font=("Comic Sans MS", 16, "bold"))
    schedule_label.pack(pady=(20, 5))

    scroll_frame = ctk.CTkScrollableFrame(main_frame, width=600, height=200)
    scroll_frame.pack(pady=5, fill="both", expand=True)

    ctk.CTkLabel(scroll_frame, text="ID", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(scroll_frame, text="Клиент", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(scroll_frame, text="Фотограф", font=("Arial", 14, "bold")).grid(row=0, column=2, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(scroll_frame, text="Услуга", font=("Arial", 14, "bold")).grid(row=0, column=3, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(scroll_frame, text="Дата", font=("Arial", 14, "bold")).grid(row=0, column=4, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(scroll_frame, text="Действие", font=("Arial", 14, "bold")).grid(row=0, column=5, padx=10, pady=5, sticky="w")

    bookings = get_all_bookings()

    def delete_action(booking_id):
        delete_booking(booking_id)
        print("[UI] Запись удалена, обновляю таблицу.")
        show_schedule(main_frame)

    for index, booking in enumerate(bookings):
        row_num = index + 1

        b_id = str(booking[0])
        b_client = booking[1]
        b_photo = booking[2]
        b_service = booking[3]
        b_date = booking[4]

        ctk.CTkLabel(scroll_frame, text=b_id, font=("Arial", 14)).grid(row=row_num, column=0, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(scroll_frame, text=b_client, font=("Arial", 14)).grid(row=row_num, column=1, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(scroll_frame, text=b_photo, font=("Arial", 14)).grid(row=row_num, column=2, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(scroll_frame, text=b_service, font=("Arial", 14)).grid(row=row_num, column=3, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(scroll_frame, text=b_date, font=("Arial", 14)).grid(row=row_num, column=4, padx=10, pady=2, sticky="w")

        del_btn = ctk.CTkButton(scroll_frame, text="Отменить", fg_color="red", width=80, command=lambda current_id=b_id: delete_action(current_id))
        del_btn.grid(row=row_num, column=5, padx=10, pady=2, sticky="w")

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
            img = Image.open(current_path).convert("RGBA")

            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except IOError:
                font = ImageFont.load_default()

            txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))

            draw = ImageDraw.Draw(txt_layer)
            watermark_text = "PhotoStudio Pro"

            draw.text((50, 50), watermark_text, font=font, fill=(128, 137, 138, 128))
            watermarked_img = Image.alpha_composite(img, txt_layer)

            new_path = current_path.rsplit('.', 1)[0] + "_converted.png"
            watermarked_img.save(new_path, "PNG")

            file_path_var.set(f"Сохранено как: \n{new_path}")
            print(f"[UI] Файл конвертирован с водяным знаком: {new_path}")

    def convert_to_jpg():
        current_path = file_path_var.get()
        if current_path != "Файл не выбран":
            img = Image.open(current_path).convert("RGBA")

            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except IOError:
                font = ImageFont.load_default()

            txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))

            draw = ImageDraw.Draw(txt_layer)
            watermark_text = "PhotoStudio Pro"

            draw.text((50, 50), watermark_text, font=font, fill=(128, 137, 138, 128))
            watermarked_img = Image.alpha_composite(img, txt_layer)

            final_image = watermarked_img.convert("RGB")

            new_path = current_path.rsplit('.', 1)[0] + "_converted.jpg"
            final_image.save(new_path, "JPEG")

            file_path_var.set(f"Сохранено как: \n{new_path}")
            print(f"[UI] Файл конвертирован с водяным знаком: {new_path}")

    choose_btn = ctk.CTkButton(main_frame, text="Выбрать фото", font=("Comic Sans MS", 14), command=choose_file)
    choose_btn.pack(pady=10)

    path_label = ctk.CTkLabel(main_frame, textvariable=file_path_var, text_color="gray")
    path_label.pack(pady=10)

    convert_btn = ctk.CTkButton(main_frame, text="Конвертировать в PNG и добавить водяной знак", font=("Comic Sans MS", 14), command=convert_to_png)
    convert_btn.pack(pady=10)

    convert_jpg_btn = ctk.CTkButton(main_frame, text="Конвертировать в JPG и добавить водяной знак", font=("Comic Sans MS", 14), command=convert_to_jpg)
    convert_jpg_btn.pack(pady=10)