import tkinter as tk
import json
import os
import sys
from tkinter import ttk, messagebox, Label, Frame, Entry, BooleanVar, Checkbutton
from tkcalendar import Calendar
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw, ImageFont
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from data import buat_id_pesanan, muat_data_akun,  muat_data_pesanan, simpan_data_akun, current_user, buat_folder_dan_file_akun, load_harga, save_harga
from validasi import validasi_akun_baru, validasi_login, validasi_tanggal, validasi_nama_pelanggan, validasi_email, validasi_jenis_pakaian, validasi_layanan, validasi_harga

os.environ["TCL_LIBRARY"] = r"C:\Program Files\Python313\tcl\tcl8.6"
os.environ["TK_LIBRARY"] = r"C:\Program Files\Python313\tcl\tk8.6"

global root
def logout(root):
    global current_user
    current_user = None
    messagebox.showinfo("Logout", "Anda telah logout")
    menu_login(root)
    
def leave(root):
    confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin keluar?")
    if confirm:
        root.quit()
        root.destroy()  
        sys.exit()
        
def clear_window(window):
    try:
        if window.winfo_exists():
            for widget in window.winfo_children():
                widget.destroy()
    except tk.TclError:
        pass  

def on_hover(event):
    canvas.itemconfig(oval_button, fill="#FF99CC") 
    canvas.itemconfig(text_button, fill="white")
    canvas.config(cursor="hand2")
    
def on_leave(event):
    canvas.itemconfig(oval_button, fill="white")
    canvas.itemconfig(text_button, fill="#9B0067")
    canvas.config(cursor="")

def on_click_sign_up(event=None):
    sign_up(event.widget.master if event else root)

def tampilkan_halaman_awal(root):
    clear_window(root)
    global canvas, bg_image, oval_button, text_button
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    bg_image = Image.open(r"halaman awal.png")
    bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_image)
    background_label = tk.Label(root, image=bg_image)
    background_label.place(relwidth=1, relheight=1)
    background_label.image = bg_image 

    canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    shadow_x1 = screen_width // 2 - 105
    shadow_y1 = screen_height - 175
    shadow_x2 = screen_width // 2 + 105
    shadow_y2 = shadow_y1 + 55
    canvas.create_oval(shadow_x1, shadow_y1, shadow_x2, shadow_y2, fill="#D3D3D3", outline="") 

    oval_width = 200
    oval_height = 50
    button_x1 = (screen_width // 2) - (oval_width // 2)
    button_y1 = screen_height - 170
    button_x2 = (screen_width // 2) + (oval_width // 2) 
    button_y2 = button_y1 + oval_height 

    oval_button = canvas.create_oval(button_x1, button_y1, button_x2, button_y2, fill="white", outline="#FF69B4", width=3)
    text_button = canvas.create_text((button_x1 + button_x2) // 2, (button_y1 + button_y2) // 2, text="Mulai", font=("Helvetica", 16, "bold"), fill="#9B0067")

    canvas.tag_bind(oval_button, "<Button-1>", on_click_sign_up)
    canvas.tag_bind(text_button, "<Button-1>", on_click_sign_up)

    canvas.tag_bind(oval_button, "<Enter>", on_hover)
    canvas.tag_bind(text_button, "<Enter>", on_hover)
    canvas.tag_bind(oval_button, "<Leave>", on_leave)
    canvas.tag_bind(text_button, "<Leave>", on_leave)

    background_label.image = bg_image

    root.bind('<Return>', lambda event: sign_up(root))


def sign_up(root):
    clear_window(root)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    try:
        bg_image = Image.open(r"sign up.png")
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        messagebox.showerror("Error", f"Error loading background image: {e}")
        return

    background_label = tk.Label(root, image=bg_image)
    background_label.place(relwidth=1, relheight=1)
    background_label.image = bg_image

    username_entry = tk.Entry(root, font=("Helvetica", 14), justify="center")
    username_entry.pack(pady=5)
    username_entry.place(relx=0.5, rely=0.308, anchor="center")

    password_entry = tk.Entry(root, show="*", font=("Helvetica", 14), justify="center")
    password_entry.pack(pady=5)
    password_entry.place(relx=0.5, rely=0.424, anchor="center")
    background_label.image = bg_image

    def buat_akun(event=None):
        username = username_entry.get()
        password = password_entry.get()

        if not validasi_akun_baru(username, password):
            return 

        users = muat_data_akun()
        
        user_data = {"password": password}
        users[username] = user_data
        simpan_data_akun(username, user_data)
        buat_folder_dan_file_akun(username)

        messagebox.showinfo("Success", "Akun berhasil dibuat. Silakan login.")
        menu_login(root)             

    tk.Button(root, text="Buat Akun", font=("Helvetica", 16), bg="#FF69B4", fg="white", 
              relief="flat", activebackground="#D1006F", activeforeground="white", 
              cursor="hand2", command=buat_akun).place(relx=0.5, rely=0.5, anchor="center")

    tk.Button(root, text="Saya sudah punya akun", font=("Helvetica", 14), fg="#FF69B4", bg="#fdd5ed", activeforeground="#FF69B4",
              relief="flat", cursor="hand2", command=lambda: menu_login(root)).place(relx=0.5, rely=0.58, anchor="center")
    
    root.bind('<Return>', lambda event: buat_akun())
    
    leave_photo = Image.open(r"logo leave.png")
    leave_photo = leave_photo.resize((90, 90), Image.Resampling.LANCZOS)
    leave_image = ImageTk.PhotoImage(leave_photo)

    leave_button = tk.Button(root, image=leave_image, command=lambda: leave(root), bd=0, relief="flat",
                                 activebackground="#f0f0f0", cursor="hand2")
    leave_button.place(relx=0.031, rely=0.105, anchor="w")
    root.leave_image = leave_image
   
def menu_login(root):
    clear_window(root)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    bg_image = Image.open(r"login.png")
    bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_image)
    background_label = tk.Label(root, image=bg_image)
    background_label.place(relwidth=1, relheight=1)
    background_label.image = bg_image 

    username_entry = tk.Entry(root, font=("Helvetica", 14), justify="center")
    username_entry.pack(pady=5)
    username_entry.place(relx=0.5, rely=0.308, anchor="center")

    password_entry = tk.Entry(root, show="*", font=("Helvetica", 14), justify="center")
    password_entry.pack(pady=5)
    password_entry.place(relx=0.5, rely=0.424, anchor="center")
    background_label.image = bg_image

    def login():
        global current_user
        username = username_entry.get()
        password = password_entry.get()

        if validasi_login(username, password):
            current_user = username  
            messagebox.showinfo("Login berhasil", "Selamat datang di Swift Clean")
            menu_admin(root) 
        else:
            return

    login_button = tk.Button(root, text="Login", bg="#FF69B4", fg="white", font=("Helvetica", 16, "bold"), command=login, 
                         bd=0, relief="flat", activebackground="#D1006F", activeforeground="white", cursor="hand2")

    login_button.place(relx=0.5, rely=0.5, anchor="center")

    tk.Button(root, text="Saya belum punya akun", font=("Helvetica", 14), fg="#FF69B4", bg="#fdd5ed", activeforeground="#FF69B4",
              relief="flat", cursor="hand2", command=lambda: sign_up(root)).place(relx=0.5, rely=0.58, anchor="center")
    
    try:
        leave_photo = Image.open(r"logo leave.png")
        leave_photo = leave_photo.resize((90, 90), Image.Resampling.LANCZOS)
        leave_image = ImageTk.PhotoImage(leave_photo)

        leave_button = tk.Button(root, image=leave_image, command=lambda: leave(root), bd=0, relief="flat",
                                 activebackground="#f0f0f0", cursor="hand2")
        leave_button.place(relx=0.031, rely=0.105, anchor="w")
        root.leave_image = leave_image
    except Exception as e:
        print(f"Error loading leave button image: {e}")

    root.bind('<Return>', lambda event: login())   
       
def menu_admin(root):
    clear_window(root)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    bg_image = Image.open(r"menu utama.png")
    bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_image)
    
    background_label = tk.Label(root, image=bg_image)
    background_label.place(relwidth=1, relheight=1)
    background_label.image = bg_image

    tk.Button(root, text="Kelola Harga", font=("Helvetica", 15), fg="#9B0067", bg="#EDEDED", relief="flat", activebackground="#FF69B4", activeforeground="white", cursor="hand2", command=lambda: kelola_harga(root)).place(relx=0.5, rely=0.228, anchor="center")
    tk.Button(root, text="Tambah Pesanan", font=("Helvetica", 15), fg="#9B0067", bg="#EDEDED", relief="flat", activebackground="#FF69B4", activeforeground="white", cursor="hand2", command=lambda: tampilkan_tambah_pesanan(root)).place(relx=0.5, rely=0.318, anchor="center")
    tk.Button(root, text="Tampilkan Semua Pesanan", font=("Helvetica", 15), fg="#9B0067", bg="#EDEDED", relief="flat", activebackground="#FF69B4", activeforeground="white", cursor="hand2", command=lambda: tampilkan_pesanan(root)).place(relx=0.5, rely=0.400, anchor="center")
    tk.Button(root, text="Cetak Tagihan", font=("Helvetica", 15), fg="#9B0067", bg="#EDEDED", relief="flat", activebackground="#FF69B4", activeforeground="white", cursor="hand2", command=lambda: tampilkan_tagihan(root)).place(relx=0.5, rely=0.484, anchor="center")
    tk.Button(root, text="Logout", font=("Helvetica", 15), fg="#9B0067", bg="#EDEDED", relief="flat", activebackground="#FF69B4", activeforeground="white", cursor="hand2", command=lambda: logout(root)).place(relx=0.5, rely=0.578, anchor="center")

def kelola_harga(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    bg_image = Image.open(r"kelola harga.png")
    bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_image)
    
    background_label = tk.Label(root, image=bg_image)
    background_label.place(relwidth=1, relheight=1)
    background_label.image = bg_image
    
    main_frame = tk.Frame(root, bg="#EDEDED", bd=0)
    main_frame.place(relx=0.5, rely=0.445, anchor="center", relwidth=0.7, relheight=0.38)

    row_start = 1

    tk.Label(main_frame, text="Jenis Pakaian", font=("Helvetica", 14, "bold"), anchor="center", fg="#9B0067", bg="#EDEDED").grid(row=row_start, column=0, padx=10, pady=5)
    tk.Label(main_frame, text="Normal (per kg)", font=("Helvetica", 14, "bold"), anchor="center", fg="#9B0067", bg="#EDEDED").grid(row=row_start, column=1, padx=10, pady=5)
    tk.Label(main_frame, text="Express (per kg)", font=("Helvetica", 14, "bold"), anchor="center", fg="#9B0067", bg="#EDEDED").grid(row=row_start, column=2, padx=10, pady=5)
    tk.Label(main_frame, text="Harga Sebelumnya", font=("Helvetica", 14, "bold"), anchor="center", fg="#9B0067", bg="#EDEDED").grid(row=row_start, column=3, padx=10, pady=5)
    
    row_start += 1 

    entries = {} 

    for idx, jenis in enumerate(["Baju", "Selimut/Seprai", "Karpet"]):
        tk.Label(main_frame, text=jenis, font=("Helvetica", 14), fg="#9B0067", bg="#EDEDED").grid(row=row_start + idx, column=0, padx=10, pady=5, sticky="w")

        normal_entry = tk.Entry(main_frame, width=10)
        normal_entry.grid(row=row_start + idx, column=1, padx=10, pady=5)

        express_entry = tk.Entry(main_frame, width=10)
        express_entry.grid(row=row_start + idx, column=2, padx=10, pady=5)
        
        harga = load_harga()  
        harga_sebelumnya = harga.get(jenis, {"Normal": 0, "Express": 0})
        tk.Label(main_frame, text=f"Normal: Rp{harga_sebelumnya['Normal']}, Express: Rp{harga_sebelumnya['Express']}",
                 font=("Helvetica", 14), bg="#EDEDED", fg="gray", justify="right").grid(row=row_start + idx, column=3, padx=10, pady=5, sticky="w")

        entries[jenis] = {"Normal": normal_entry, "Express": express_entry}

    def simpan_harga():
        harga_baru = {}
        for jenis, fields in entries.items():
            normal = fields["Normal"].get().strip()
            express = fields["Express"].get().strip()

            if not validasi_harga(normal, express, jenis):
                return

            harga_baru[jenis] = {"Normal": int(normal), "Express": int(express)}

        save_harga(harga_baru)
        messagebox.showinfo("Berhasil", "Harga berhasil diperbarui!")
        menu_admin(root)

    frame_tombol = tk.Frame(main_frame, bg="#EDEDED")
    frame_tombol.grid(row=row_start + len(entries), column=0, columnspan=30, pady=60)

    simpan_button = tk.Button(frame_tombol, text="Simpan Harga", font=("Helvetica", 15), bg="#FF69B4", fg="white", width=15, 
                              bd=0, relief="flat", activebackground="#D1006F", activeforeground="white", cursor="hand2", command=simpan_harga)
    simpan_button.pack(side=tk.RIGHT, padx=15, expand=True)

    menu_button = tk.Button(frame_tombol, text="Kembali ke Menu", font=("Helvetica", 15), bg="#FF69B4", fg="white", width=15, 
                            bd=0, relief="flat", activebackground="#D1006F", activeforeground="white", cursor="hand2", command=lambda: menu_admin(root))
    menu_button.pack(side=tk.LEFT, padx=15, expand=True)

    root.bind('<Return>', lambda event: simpan_harga())

def tampilkan_tambah_pesanan(root):
    clear_window(root)
    global current_user

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    bg_image = Image.open(r"tambah pesanan.png")
    bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_image)
    
    background_label = tk.Label(root, image=bg_image)
    background_label.place(relwidth=1, relheight=1)
    background_label.image = bg_image

    main_frame = Frame(root, bg="#EDEDED", bd=0)
    main_frame.place(relx=0.535, rely=0.567, anchor="center", relwidth=0.65, relheight=0.79)

    frame_nama = tk.Frame(main_frame, pady=5, bg="#EDEDED")
    frame_nama.pack(fill=tk.X, padx=150)
    tk.Label(frame_nama, text="Nama Pelanggan:", font=("Helvetica", 14), anchor="w", fg="#9B0067", bg="#EDEDED").pack(side=tk.LEFT)
    nama_pelanggan_entry = tk.Entry(frame_nama, font=("Helvetica", 14), width=35)
    nama_pelanggan_entry.pack(side=tk.RIGHT, padx=10)

    frame_email = tk.Frame(main_frame, pady=10, bg="#EDEDED")
    frame_email.pack(fill=tk.X, padx=150)
    tk.Label(frame_email, text="Email Pelanggan:", font=("Helvetica", 14), anchor="w", fg="#9B0067", bg="#EDEDED").pack(side=tk.LEFT)
    email_pelanggan_entry = tk.Entry(frame_email, font=("Helvetica", 14), width=35)
    email_pelanggan_entry.pack(side=tk.RIGHT, padx=10)
 
    frame_jenis = tk.Frame(main_frame, pady=10, bg="#EDEDED")
    frame_jenis.pack(fill=tk.X, padx=150)
    tk.Label(frame_jenis, text="Jenis Pakaian     :", font=("Helvetica", 14), anchor="w", fg="#9B0067", bg="#EDEDED").pack(side=tk.LEFT)
    
    jenis_pakaian_values = {"Baju": BooleanVar(), "Selimut/Seprai": BooleanVar(), "Karpet": BooleanVar()}
    berat_entries = {}

    for jenis in jenis_pakaian_values:
        col = Frame(frame_jenis, bg="#EDEDED", padx=5)
        col.pack(side="left", expand=True)
        Checkbutton(col, text=jenis, variable=jenis_pakaian_values[jenis], font=("Helvetica", 12), fg="#9B0067", bg="#EDEDED").pack()
        Label(col, text="Berat (kg):", font=("Helvetica", 10), fg="#9B0067", bg="#EDEDED").pack()
        berat_entries[jenis] = Entry(col, font=("Helvetica", 10), width=10)
        berat_entries[jenis].pack()

    frame_layanan = tk.Frame(main_frame, pady=10, bg="#EDEDED")
    frame_layanan.pack(fill=tk.X, padx=150)
    tk.Label(frame_layanan, text="Jenis Layanan    :", font=("Helvetica", 14), anchor="w", fg="#9B0067", bg="#EDEDED").pack(side=tk.LEFT)
    layanan_options = ["", "Normal", "Express"]
    jenis_layanan = ttk.Combobox(frame_layanan, values=layanan_options, font=("Helvetica", 14), width=33)
    jenis_layanan.set("")
    jenis_layanan.pack(side=tk.LEFT, padx=10, fill=tk.X)

    current_date = datetime.now()
    Label(main_frame, text="Estimasi Tanggal Selesai:", font=("Helvetica", 14), fg="#9B0067", bg="#EDEDED").pack(pady=10)
    kalender = Calendar(main_frame, selectmode="day", year=current_date.year, month=current_date.month, day=current_date.day, background="#FF69B4", foreground="white",
    selectbackground="#9B0067", selectforeground="white", weekendbackground="#D1006F", weekendforeground="white", headersbackground="#D1006F",  # Pink pastel for header
    headersforeground="white", showweeknumbers=False)
    kalender.pack(pady=5)

    def simpan_pesanan():
        nama_pelanggan = nama_pelanggan_entry.get()
        email_pelanggan = email_pelanggan_entry.get()
        layanan = jenis_layanan.get()
        estimasi_waktu = kalender.get_date()

        if not validasi_nama_pelanggan(nama_pelanggan):
            return

        if not validasi_email(email_pelanggan):
            return

        jenis_pakaian_terpilih, pesan_error = validasi_jenis_pakaian(jenis_pakaian_values, berat_entries, layanan, estimasi_waktu)
        if not jenis_pakaian_terpilih:
            messagebox.showerror("Error", pesan_error) 
            return

        if not validasi_layanan(layanan):  
            return

        if not validasi_tanggal(estimasi_waktu): 
            return

        pesanan_baru = []
        pesanan_baru.extend(jenis_pakaian_terpilih)  
        id_pesanan = buat_id_pesanan(current_user)

        pesanan_data = {
            "nama_pelanggan": nama_pelanggan,
            "email": email_pelanggan,
            "items": pesanan_baru,  
            "jenis_layanan": layanan,
            "estimasi_waktu": estimasi_waktu
        }
        
        pesanan_file = f"user_data/{current_user}/{current_user}_pesanan.json"

        try:
            with open(pesanan_file, "r") as f:
                existing_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            existing_data = {}

        existing_data[id_pesanan] = pesanan_data

        with open(pesanan_file, "w") as f:
            json.dump(existing_data, f, indent=4)

        messagebox.showinfo("Pesanan berhasil", f"Pesanan {id_pesanan} berhasil ditambahkan!")
        menu_admin(root)


    frame_tombol = tk.Frame(main_frame, bg="#EDEDED")
    frame_tombol.pack(pady=20)
    
    menu_button = tk.Button(frame_tombol, text="Kembali ke Menu", font=("Helvetica", 15), bg="#FF69B4", fg="white", width=15, 
                            bd=0, relief="flat", activebackground="#D1006F", activeforeground="white", cursor="hand2", command=lambda: menu_admin(root))
    menu_button.pack(side=tk.LEFT, padx=5, expand=True)

    simpan_button = tk.Button(frame_tombol, text="Simpan Pesanan", font=("Helvetica", 15), bg="#FF69B4", fg="white", width=15, 
                              bd=0, relief="flat", activebackground="#D1006F", activeforeground="white", cursor="hand2", command=simpan_pesanan)
    simpan_button.pack(side=tk.RIGHT, padx=5, expand=True)
    
    root.bind('<Return>', lambda event: simpan_pesanan())
    

def tampilkan_pesanan(root):
    clear_window(root)
    global current_user
    pesanan = muat_data_pesanan(current_user) 

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    bg_image = Image.open(r"daftar pesanan.png")
    bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_image)
    
    background_label = tk.Label(root, image=bg_image)
    background_label.place(relwidth=1, relheight=1)
    background_label.image = bg_image 
    
    main_frame = tk.Frame(root, bg="#EDEDED", bd=0)
    main_frame.place(relx=0.5, rely=0.521, anchor="center", relwidth=0.47, relheight=0.715)

    canvas = tk.Canvas(main_frame, bg="#EDEDED", bd=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) 
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    frame_scrollable = tk.Frame(canvas)

    frame_scrollable.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")) )
    canvas.create_window((0, 0), window=frame_scrollable, anchor="nw")
    canvas.config(yscrollcommand=scrollbar.set)

    def on_mouse_wheel(event):
        if event.delta: 
            canvas.yview_scroll(-1 * (event.delta // 120), "units")
        elif event.num in (4, 5):  
            canvas.yview_scroll(-1 if event.num == 4 else 1, "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)  
    canvas.bind_all("<Button-4>", on_mouse_wheel) 
    canvas.bind_all("<Button-5>", on_mouse_wheel) 

    for id_pesanan, data in pesanan.items():
        frame_pesanan = tk.Frame(frame_scrollable, padx=15, pady=10, relief="solid", bd=1, bg="white")
        frame_pesanan.pack(fill=tk.BOTH, pady=10, padx=5)

        tk.Label(
            frame_pesanan,
            text=f"ID Pesanan: {id_pesanan}",
            font=("Helvetica", 14, "bold"),
            anchor="w", fg="#FF69B4", bg="white"
        ).grid(row=0, column=0, sticky="w", columnspan=2, pady=5)

        tk.Label(
            frame_pesanan,
            text=f"Nama: {data['nama_pelanggan']} ({data['email']})",
            font=("Helvetica", 12, "bold"), 
            anchor="w", fg="#FF69B4", bg="white"
        ).grid(row=1, column=0, sticky="w", columnspan=2, pady=3)

        tk.Label(
            frame_pesanan,
            text="Daftar Item:",
            font=("Helvetica", 12, "italic"),
            anchor="w", fg="#FF69B4", bg="white"
        ).grid(row=2, column=0, sticky="w", columnspan=2, pady=5)

        for idx, item in enumerate(data.get("items", []), start=3): 
            tk.Label(
                frame_pesanan,
                text=f"• {item['jenis_pakaian']} - Berat: {item['berat']}kg",
                font=("Helvetica", 12),
                anchor="w", fg="#FF69B4", bg="white"
            ).grid(row=idx, column=0, sticky="w", pady=2)
            tk.Label(
                frame_pesanan,
                text=f"Layanan: {data['jenis_layanan']}, Estimasi: {data['estimasi_waktu']}",
                font=("Helvetica", 12),
                anchor="w", fg="#FF69B4", bg="white"
            ).grid(row=idx, column=1, sticky="w", padx=10, pady=2)

    frame_tombol = tk.Frame(frame_scrollable, pady=20)
    frame_tombol.pack(fill=tk.X)
    tk.Button(frame_tombol, text="Kembali ke Menu", font=("Helvetica", 15), bg="#FF69B4", fg="white", width=15, 
                        bd=0, relief="flat", activebackground="#D1006F", activeforeground="white", cursor="hand2", command=lambda: menu_admin(root)).pack(anchor="center")

def tampilkan_tagihan(root):
    clear_window(root)
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    bg_image = Image.open(r"cetak tagihan.png")
    bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_image)
    
    background_label = tk.Label(root, image=bg_image)
    background_label.place(relwidth=1, relheight=1)
    background_label.image = bg_image 

    main_frame = tk.Frame(root, bg="#EDEDED", bd=0)
    main_frame.place(relx=0.5, rely=0.408, anchor="center", relwidth=0.47, relheight=0.4)

    id_pesanan_entry = tk.Entry(main_frame, font=("Helvetica", 14), justify="center")
    id_pesanan_entry.pack(pady=10)

    def hitung_tagihan(event=None): 
        id_pesanan = id_pesanan_entry.get().strip() 
        pesanan = muat_data_pesanan(current_user) 
        harga_per_kg = load_harga()
        
        if id_pesanan in pesanan:
            data_pesanan = pesanan[id_pesanan]
            nama_pelanggan = data_pesanan['nama_pelanggan']
            email_pelanggan = data_pesanan['email']

            total_tagihan = 0
            tagihan_text = ""

            for item in data_pesanan['items']:
                jenis = item["jenis_pakaian"]
                layanan = item["jenis_layanan"]
                berat = item["berat"]
                biaya = berat * harga_per_kg[jenis][layanan]
                total_tagihan += biaya
                tagihan_text += f"| {jenis:<15} | {berat:<4}kg   | {layanan:<8} | Rp{biaya:<10,} |\n"

            tanggal_estimasi = data_pesanan['items'][0]["estimasi_waktu"]
            tanggal_estimasi = datetime.strptime(tanggal_estimasi, "%m/%d/%y").strftime("%d/%m/%Y")

            tanggal_sekarang = datetime.now()
            tanggal_str = tanggal_sekarang.strftime("%d/%m/%Y")
            struk = f"""
========================================================
                   Swift Clean Laundry
               Struk Resmi Layanan Laundry
========================================================
ID Pesanan      : {id_pesanan}
Nama Pelanggan  : {nama_pelanggan}
Tanggal Tagihan : {tanggal_str}
Estimasi Selesai: {tanggal_estimasi}

--------------------------------------------------------
| Jenis Pakaian   | Berat    | Layanan  | Biaya        |
--------------------------------------------------------
{tagihan_text}
========================================================
                        Total Tagihan   : Rp{total_tagihan:,.1f}
========================================================
              Terima Kasih telah menggunakan
                  Swift Clean Laundry!
========================================================
"""

            clear_window(root)
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
    
            bg_image = Image.open(r"struk tagihan.png")
            bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            bg_image = ImageTk.PhotoImage(bg_image)
    
            background_label = tk.Label(root, image=bg_image)
            background_label.place(relwidth=1, relheight=1)
            background_label.image = bg_image
            
            main_frame = tk.Frame(root, bg="#EDEDED", bd=0)
            main_frame.place(relx=0.52, rely=0.54, anchor="center", relwidth=0.47, relheight=0.8)
    
            tk.Label(main_frame, text=struk, font=("Courier", 12), justify="left").pack(pady=10)

            nama_file = f"struk_{id_pesanan}.png"
            buat_gambar_struk(nama_file, id_pesanan, nama_pelanggan, tanggal_str, tanggal_estimasi, tagihan_text, total_tagihan)

            def kirim_tagihan():
                kirim_email_dengan_gambar(nama_file, email_pelanggan)
                messagebox.showinfo("Email Dikirim", "Struk berhasil dikirim ke email pelanggan!")

            tk.Button(main_frame, text="Kirim Tagihan via Email", font=("Helvetica", 15), bg="#FF69B4", fg="white",
                        bd=0, relief="flat", activebackground="#D1006F", activeforeground="white", cursor="hand2", command=lambda: kirim_tagihan()).pack(pady=0.6)
            tk.Button(main_frame, text="Kembali ke Menu", font=("Helvetica", 15), bg="#FF69B4", fg="white", width=15, 
                        bd=0, relief="flat", activebackground="#D1006F", activeforeground="white", cursor="hand2", command=lambda: menu_admin(root)).pack(pady=0.8)

        else:
            messagebox.showerror("Error", "ID Pesanan tidak ditemukan!")

    tk.Button(main_frame, text="Cari Tagihan", font=("Helvetica", 15), bg="#FF69B4", fg="white", width=15, 
                        bd=0, relief="flat", activebackground="#D1006F", activeforeground="white", cursor="hand2", command=lambda: hitung_tagihan()).pack(pady=10)
    tk.Button(main_frame, text="Kembali ke Menu", font=("Helvetica", 15), bg="#FF69B4", fg="white", width=15, 
                        bd=0, relief="flat", activebackground="#D1006F", activeforeground="white", cursor="hand2", command=lambda: menu_admin(root)).pack(pady=5)
    root.bind('<Return>', lambda event: hitung_tagihan())

def kirim_email_dengan_gambar(nama_file, email_pelanggan):
    msg = MIMEMultipart()
    msg["From"] = "swiftcleanlaundry1@gmail.com"
    msg["To"] = email_pelanggan
    msg["Subject"] = "Struk Laundry Anda"

    body = "Berikut adalah struk laundry Anda."
    msg.attach(MIMEText(body, "plain"))
    file_path = f"user_data/{current_user}/{nama_file}"

    with open(file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={nama_file}")
        msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("swiftcleanlaundry1@gmail.com", "gnnb jhpj nwif xfzs")
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        
def buat_gambar_struk(nama_file, id_pesanan, nama_pelanggan, tanggal_str, tanggal_estimasi, tagihan_text, total_tagihan):
    with open(f'user_data/{current_user}/{current_user}_pesanan.json', 'r') as file:
        data_pesanan = json.load(file)

    if id_pesanan in data_pesanan:
        # Menghitung jumlah jenis pakaian yang unik
        jenis_pakaian = set(item['jenis_pakaian'] for item in data_pesanan[id_pesanan]['items'])
        jumlah_jenis_pakaian = len(jenis_pakaian)

    if jumlah_jenis_pakaian == 1:
        img = Image.open(r"struk1.png")  
    elif jumlah_jenis_pakaian == 2:
        img = Image.open(r"struk2.png") 
    else:
        img = Image.open(r"struk.png")

    draw = ImageDraw.Draw(img)

    font_path = "C:/Windows/Fonts/consola.ttf" 
    font_body = ImageFont.truetype(font_path, 38)
    line_spacing = 40

    y = 150  

    y += 332
    draw.text((325, y), f"{id_pesanan}", font=font_body, fill="black")
    draw.text((1025, y), f"{tanggal_str}", font=font_body, fill="black")
    y += line_spacing + 14
    draw.text((418, y), f"{nama_pelanggan}", font=font_body, fill="black")
    draw.text((995, y), f"{tanggal_estimasi}", font=font_body, fill="black")

    y += 280  
    for line in tagihan_text.splitlines():
        line_cleaned = line.replace("|", "").strip()
        parts = line_cleaned.split("Rp")
        if len(parts) == 2: 
            line_with_padding = f"{parts[0]}{' ' * 5}Rp{parts[1]}" 
        else:
            line_with_padding = line_cleaned
        parts = line_with_padding.split("kg")
        if len(parts) == 2: 
            line_with_padding2 = f"{parts[0]}kg{' ' * 2}{parts[1]}"  
        else:
            line_with_padding2 = line_cleaned 
        draw.text((110, y), line_with_padding2, font=font_body, fill="black")
        y += 140 

    y = 1374
    draw.text((508, y), f"                         Rp{total_tagihan:,}", font=font_body, fill="black")

    folder_path = f"user_data/{current_user}"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, nama_file)

    img.save(file_path)