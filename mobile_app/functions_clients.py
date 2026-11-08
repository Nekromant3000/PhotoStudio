import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import database

def get_busy_slots(photographer_id, date_str):
    try:
        conn = sqlite3.connect("photostudio.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT booking_date FROM bookings WHERE photographer_id = ? AND booking_date LIKE ?", 
        (photographer_id, f"{date_str}%"))

        rows = cursor.fetchall()
        conn.close()

        busy_times = [r[0].split(" ") [1] for r in rows if " " in r[0]]

        return busy_times
    except Exception:
        return []

def get_or_create_client_id(name, phone):
    clients = database.get_all_clients()
    for c in clients:
        if len(c) >= 3 and str(c[2]).strip() == phone.strip():
                               return c[0]
    database.add_client(name, phone)

    updated_clients = database.get_all_clients()
    for c in updated_clients:
         if len(c) >= 3 and str(c[2]).strip() == phone.strip():
              return c[0]

    return None

def new_entry(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()

    title_lable = ctk.CTkLabel(main_frame, text="Онлайн-запись", font=("Comic Sans MS", 20, "bold"))
    title_lable.pack(pady=(15,5))

    scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
    scroll.pack(fill="both", expand=True, padx=15, pady=5)

    name_entry = ctk.CTkEntry(scroll, placeholder_text="Ваше имя", height=38)
    name_entry.pack(fill="x", pady=5)

    phone_entry = ctk.CTkEntry(scroll, placeholder_text="Телефон (89********)", height=38)
    phone_entry.pack(fill="x", pady=5)

    photographers = database.get_all_photographers()
    photo_map = {f"{p[1]} (ID: {p[0]})": p[0] for p in photographers}
    photo_values = list(photo_map.keys()) if photo_map else ["Нет специалистов"]

    ctk.CTkLabel(scroll, text="Выбор фотографа: ", font=("Comic Sans MS", 12, "bold")).pack(anchor="w", pady=(10, 2))

    combo_photo = ctk.CTkComboBox(scroll, values=photo_values, height=36)
    combo_photo.pack(fill="x", pady=2)

    services = database.get_all_services()
    service_map = {f"{s[1]}": s[0] for s in services}
    service_values = list(service_map.keys()) if service_map else ["Нет доступных услуг"]

    ctk.CTkLabel(scroll, text="Выберете услугу: ", font=("Comic Sans MS", 12, "bold")).pack(anchor="w", pady=(10, 2))

    combo_service = ctk.CTkComboBox(scroll, values=service_values, height=36)
    combo_service.pack(fill="x", pady=2)

    ctk.CTkLabel(scroll, text="Дата (ГГГГ-ММ-ДД):", font=("Comic Sans MS", 12, "bold")).pack(anchor="w", pady=(10, 2))
    date_entry = ctk.CTkEntry(scroll, placeholder_text="2026-11-15", height=36)
    date_entry.insert(0, "2026-11-15")
    date_entry.pack(fill="x", pady=2)

    ctk.CTkLabel(scroll, text="Свободное время для записи:", font=("Comic Sans MS", 12, "bold")).pack(anchor="w", pady=(12, 4))

    slots_frame = ctk.CTkFrame(scroll, fg_color="transparent")
    slots_frame.pack(fill="x", pady=2)
    slots_frame.grid_columnconfigure((0, 1, 2), weight=1)

    time_slots = ["10:00", "12:00", "14:00", "16:00", "18:00", "20:00"]
    selected_time = ctk.StringVar(value="")
    slot_buttons = {}

    def set_time(val):
        selected_time.set(val)
        for t, b in slot_buttons.items():
            if t == val:
                b.configure(fg_color="#2563eb")
            else:
                b.configure(fg_color="#3f3f46")

    for i, t in enumerate(time_slots):
        r, c = i // 3, i % 3
        btn = ctk.CTkButton(
            slots_frame, text=t, height=34, fg_color="#3f3f46",
            command=lambda val=t: set_time(val)
        )
        btn.grid(row=r, column=c, padx=3, pady=3, sticky="ew")
        slot_buttons[t] = btn

    def check_availability():
        chosen_photo_str = combo_photo.get()
        chosen_date = date_entry.get().strip()

        if chosen_photo_str not in photo_map or not chosen_date:
            messagebox.showwarning("Внимание", "Выберите фотографа и укажите дату!")
            return

        p_id = photo_map[chosen_photo_str]
        busy_list = get_busy_slots(p_id, chosen_date)

        for t, btn in slot_buttons.items():
            if t in busy_list:
                btn.configure(state="disabled", fg_color="#ef4444", text=f"{t}\nЗанято")
                if selected_time.get() == t:
                    selected_time.set("")
            else:
                btn.configure(state="normal", fg_color="#3f3f46", text=t)

    btn_check = ctk.CTkButton(scroll, text="Обновить свободные часы", height=30, fg_color="#4b5563", command=check_availability)
    btn_check.pack(fill="x", pady=(6, 12))

    def submit_booking():
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        chosen_photo_str = combo_photo.get()
        chosen_service_str = combo_service.get()
        date_val = date_entry.get().strip()
        time_val = selected_time.get()

        if not name or not phone:
            messagebox.showwarning("Внимание", "Пожалуйста, введите имя и номер телефона!")
            return

        if not time_val:
            messagebox.showwarning("Внимание", "Пожалуйста, выберите время (нажмите на слот)!")
            return

        if chosen_photo_str not in photo_map or chosen_service_str not in service_map:
            messagebox.showerror("Ошибка", "Выберите фотографа и услугу из списка!")
            return

        p_id = photo_map[chosen_photo_str]
        s_id = service_map[chosen_service_str]
        full_datetime = f"{date_val} {time_val}"

        client_id = get_or_create_client_id(name, phone)

        if not client_id:
            messagebox.showerror("Ошибка", "Не удалось зарегистрировать клиента в базе!")
            return

        try:
            database.add_booking(client_id, p_id, s_id, full_datetime)
            messagebox.showinfo("Успешно!", f"Запись оформлена на {full_datetime}!\nЖдём вас!")
            new_entry(main_frame)
        except Exception as e:
            messagebox.showerror("Ошибка БД", f"Не удалось сохранить запись: {e}")

    btn_book = ctk.CTkButton(
        scroll, text="Подтвердить запись", height=42, corner_radius=8,
        fg_color="#16a34a", hover_color="#15803d", font=("Comic Sans MS", 14, "bold"),
        command=submit_booking
    )
    btn_book.pack(fill="x", pady=(10, 15))

def show_photo(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()

    title_label = ctk.CTkLabel(main_frame, text="Портфолио работ", font=("Comic Sans MS", 20, "bold"))
    title_label.pack(pady=(15, 5))

    scroll_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
    scroll_frame.pack(fill="both", expand=True, pady=5, padx=10)

    works = [
        ("photo1.jpg", "Свадебная съемка", "Фотограф: Анна"),
        ("photo2.jpg", "Студийный портрет", "Фотограф: Олег"),
        ("photo3.jpg", "Съемка с собаками", "Фотограф: Олег"),
        ("photo4.jpg", "Выездная фотосессия", "Фотограф: Анна")
    ]

    for path, title, author in works:
        card = ctk.CTkFrame(scroll_frame, corner_radius=10, fg_color="#27272a")
        card.pack(fill="x", pady=8, padx=5)

        try:
            pil_image = Image.open(path)
            ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(320, 180))
            img_label = ctk.CTkLabel(card, text="", image=ctk_image)
            img_label.pack(pady=8, padx=8)
        except Exception:
            img_label = ctk.CTkLabel(
                card, text=f"[ Превью: {title} ]", width=320, height=130,
                fg_color="#3f3f46", corner_radius=8, font=("Comic Sans MS", 13, "bold")
            )
            img_label.pack(pady=8, padx=8)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(fill="x", padx=10, pady=(0, 8))
        ctk.CTkLabel(info, text=title, font=("Comic Sans MS", 14, "bold")).pack(anchor="w")
        ctk.CTkLabel(info, text=author, font=("Comic Sans MS ", 12), text_color="gray").pack(anchor="w")