import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import smtplib
from PIL import Image, ImageTk
from tkinter import Label, Frame, Entry, StringVar, BooleanVar, Checkbutton, OptionMenu

os.environ["TCL_LIBRARY"] = r"C:\Program Files\Python313\tcl\tcl8.6"
os.environ["TK_LIBRARY"] = r"C:\Program Files\Python313\tcl\tk8.6"

DATA_FILE = "data_users.json" 

def muat_data_akun():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as file:
            json.dump({}, file, indent=4)
        return {}

    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            with open(DATA_FILE, "w") as f:
                json.dump({}, f, indent=4)
            return {}

def simpan_data_akun(username, user_data):
    users = muat_data_akun()
    users[username] = {"password": user_data["password"]}
    with open(DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)
        
def muat_data_pesanan(username):
    pesanan_file = f"user_data/{username}/{username}_pesanan.json"
    if not os.path.exists(pesanan_file):
        with open(pesanan_file, "w") as file:
            json.dump({}, file, indent=4)
        return {}

    with open(pesanan_file, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            with open(pesanan_file, "w") as f:
                json.dump({}, f, indent=4)
            return {}

def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()

def leave():
    messagebox.showinfo("Close Program", "Anda telah keluar. Program akan ditutup.")
    root.quit()
    
def menu_login():
    print("Tombol 'Mulai' ditekan!") 

def on_click(event):
    menu_login()

def on_hover(event):
    canvas.itemconfig(oval_button, fill="#FF99CC") 
    canvas.itemconfig(text_button, fill="white")
    canvas.config(cursor="hand2")
    
def on_leave(event):
    """Kembalikan warna tombol setelah hover."""
    canvas.itemconfig(oval_button, fill="white")
    canvas.itemconfig(text_button, fill="#9B0067")
    canvas.config(cursor="")
    
def on_click_sign_up(event=None):
    sign_up() 

def tampilkan_halaman_awal():
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

    root.bind('<Return>', lambda event: sign_up())
    
def sign_up():
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

        if not username or not password:
            messagebox.showerror("Error", "Username dan Password harus diisi!")
            return
        if len(username) < 3:
            messagebox.showerror("Error", "Username harus terdiri dari minimal 3 karakter!")
            return

# Validasi password harus memiliki kombinasi huruf dan angka
        if not re.search("[A-Za-z]", password) or not re.search("[0-9]", password):
            messagebox.showerror("Error", "Password harus mengandung kombinasi huruf dan angka!")
            return

        users = muat_data_akun()

        if username in users:
            messagebox.showerror("Error", "Username sudah ada, coba username lain.")
            return

        user_data = {"password": password}
        users[username] = user_data
        simpan_data_akun(username, user_data)

        messagebox.showinfo("Success", "Akun berhasil dibuat. Silakan login.")
        menu_login()

    tk.Button(root, text="Buat Akun", font=("Helvetica", 16), bg="#FF69B4", fg="white", 
              relief="flat", activebackground="#D1006F", activeforeground="white", 
              cursor="hand2", command=buat_akun).place(relx=0.5, rely=0.5, anchor="center")

    tk.Button(root, text="Saya sudah punya akun", font=("Helvetica", 14), fg="#FF69B4", bg="#fdd5ed", activeforeground="#FF69B4",
              relief="flat", cursor="hand2", command=menu_login).place(relx=0.5, rely=0.58, anchor="center")
    
    root.bind('<Return>', lambda event: buat_akun())
    
    try:
        leave_photo = Image.open(r"logo leave.png")
        leave_photo = leave_photo.resize((90, 90), Image.Resampling.LANCZOS)
        leave_image = ImageTk.PhotoImage(leave_photo)

        leave_button = tk.Button(root, image=leave_image, command=leave, bd=0, relief="flat",
                                 activebackground="#f0f0f0", cursor="hand2")
        leave_button.place(relx=0.031, rely=0.105, anchor="w")
        root.leave_image = leave_image
    except Exception as e:
        print(f"Error loading leave button image: {e}")
        
current_user = None

def menu_login():
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

    def login(event=None):
        global current_user
        username = username_entry.get()
        password = password_entry.get()

        users = muat_data_akun()

        if username in users and users[username]["password"] == password:
            current_user = username
            messagebox.showinfo("Login berhasil", "Selamat datang di Swift Clean")
            menu_admin()
        else:
            messagebox.showerror("Login gagal", "Username atau password salah")

    login_button = tk.Button(root, text="Login", bg="#FF69B4", fg="white", font=("Helvetica", 16, "bold"), command=login, 
                         bd=0, relief="flat", activebackground="#D1006F", activeforeground="white", cursor="hand2")

    login_button.place(relx=0.5, rely=0.5, anchor="center")

    tk.Button(root, text="Saya belum punya akun", font=("Helvetica", 14), fg="#FF69B4", bg="#fdd5ed", activeforeground="#FF69B4",
              relief="flat", cursor="hand2", command=sign_up).place(relx=0.5, rely=0.58, anchor="center")
    
    try:
        leave_photo = Image.open(r"logo leave.png")
        leave_photo = leave_photo.resize((90, 90), Image.Resampling.LANCZOS)
        leave_image = ImageTk.PhotoImage(leave_photo)

        leave_button = tk.Button(root, image=leave_image, command=leave, bd=0, relief="flat",
                                 activebackground="#f0f0f0", cursor="hand2")
        leave_button.place(relx=0.031, rely=0.105, anchor="w")
        root.leave_image = leave_image
    except Exception as e:
        print(f"Error loading leave button image: {e}")

    root.bind('<Return>', login)   
    
def menu_admin():
    clear_window(root)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    bg_image = Image.open(r"menu utama.png")
    bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_image)
    
    background_label = tk.Label(root, image=bg_image)
    background_label.place(relwidth=1, relheight=1)
    background_label.image = bg_image

    tk.Button(root, text="Tambah Pesanan", font=("Helvetica", 15), fg="#9B0067", bg="#EDEDED", relief="flat", activebackground="#FF69B4", activeforeground="white", cursor="hand2", command=tampilkan_tambah_pesanan).place(relx=0.5, rely=0.235, anchor="center")
    tk.Button(root, text="Tampilkan Semua Pesanan", font=("Helvetica", 15), fg="#9B0067", bg="#EDEDED", relief="flat", activebackground="#FF69B4", activeforeground="white", cursor="hand2", command=tampilkan_pesanan).place(relx=0.5, rely=0.324, anchor="center")
    tk.Button(root, text="Cetak Tagihan", font=("Helvetica", 15), fg="#9B0067", bg="#EDEDED", relief="flat", activebackground="#FF69B4", activeforeground="white", cursor="hand2", command=tampilkan_tagihan).place(relx=0.5, rely=0.412, anchor="center")
    tk.Button(root, text="Logout", font=("Helvetica", 15), fg="#9B0067", bg="#EDEDED", relief="flat", activebackground="#FF69B4", activeforeground="white", cursor="hand2", command=logout).place(relx=0.5, rely=0.5, anchor="center")

    root.bind('<Return>', lambda event: logout())

def logout():
    global current_user
    current_user = None
    messagebox.showinfo("Logout", "Anda telah logout")
    menu_login()

def buat_id_pesanan(username):
    pesanan_file = f"user_data/{username}/{username}_pesanan.json"
    
    if os.path.exists(pesanan_file):
        with open(pesanan_file, "r") as f:
            pesanan_data = json.load(f)
            if pesanan_data:
                last_id = max(int(id_pesanan) for id_pesanan in pesanan_data.keys())
                new_id = str(last_id + 1).zfill(3)
            else:
                new_id = "001" 
    else:
        new_id = "001" 
    return new_id

def tampilkan_tambah_pesanan():
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
    
    if len(nama_pelanggan_entry) < 3:
        messagebox.showerror("Error", "Nama pelanggan harus terdiri dari minimal 3 karakter!")
        return

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
    
    def validasi_tanggal(estimasi_waktu):
        tanggal_pilihan_obj = datetime.strptime(estimasi_waktu, "%m/%d/%y")
        if tanggal_pilihan_obj < current_date:
            messagebox.showerror("Error", "Tanggal yang dipilih tidak valid! Pilih tanggal setelah hari pesanan dibuat.")
            return False
        return True

    def simpan_pesanan():
        nama_pelanggan = nama_pelanggan_entry.get()
        email_pelanggan = email_pelanggan_entry.get()
        layanan = jenis_layanan.get()
        estimasi_waktu = kalender.get_date()

        if validasi_tanggal(estimasi_waktu):
            pesanan_baru = []

            if not nama_pelanggan.isalpha():
                messagebox.showerror("Error", "Nama pelanggan hanya boleh berupa huruf!")
                return

            if "@" not in email_pelanggan or "." not in email_pelanggan:
                messagebox.showerror("Error", "Email tidak valid!")
                return

            jenis_pakaian_terpilih = False
            for jenis, var in jenis_pakaian_values.items():
                if var.get():
                    jenis_pakaian_terpilih = True
                    berat = berat_entries[jenis].get()
                    if not berat.isdigit():
                        messagebox.showerror("Error", f"Berat untuk {jenis} harus berupa angka!")
                        return
                    pesanan_baru.append({
                        "jenis_pakaian": jenis,
                        "berat": float(berat),
                        "jenis_layanan": layanan,
                        "estimasi_waktu": estimasi_waktu
                    })

            if not jenis_pakaian_terpilih:
                messagebox.showerror("Error", "Pilih jenis pakaian terlebih dahulu!")
                return

            if not layanan:
                messagebox.showerror("Error", "Jenis layanan harus terisi!")
                return

            id_pesanan = buat_id_pesanan(current_user)

            pesanan_data = {
                "nama_pelanggan": nama_pelanggan,
                "email": email_pelanggan,
                "items": pesanan_baru}

            folder_path = f"user_data/{current_user}"  
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                
            pesanan_file = f"{folder_path}/{current_user}_pesanan.json"
            if os.path.exists(pesanan_file):
                with open(pesanan_file, "r") as f:
                    existing_data = json.load(f)
            else:
                existing_data = {}
                
            existing_data[id_pesanan] = pesanan_data

            with open(pesanan_file, "w") as f:
                json.dump(existing_data, f, indent=4)

            messagebox.showinfo("Pesanan berhasil", f"Pesanan {id_pesanan} berhasil ditambahkan!")
            menu_admin()

    frame_tombol = tk.Frame(main_frame, bg="#EDEDED")
    frame_tombol.pack(pady=20)
    
    menu_button = tk.Button(frame_tombol, text="Kembali ke Menu", font=("Helvetica", 15), bg="#FF69B4", fg="white", width=15, 
                            bd=0, relief="flat", activebackground="#D1006F", activeforeground="white", cursor="hand2", command=menu_admin)
    menu_button.pack(side=tk.LEFT, padx=5, expand=True)

    simpan_button = tk.Button(frame_tombol, text="Simpan Pesanan", font=("Helvetica", 15), bg="#FF69B4", fg="white", width=15, 
                              bd=0, relief="flat", activebackground="#D1006F", activeforeground="white", cursor="hand2", command=simpan_pesanan)
    simpan_button.pack(side=tk.RIGHT, padx=5, expand=True)
    
    root.bind('<Return>', lambda event: simpan_pesanan())
    

def tampilkan_pesanan():
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
                text=f"Layanan: {item['jenis_layanan']}, Estimasi: {item['estimasi_waktu']}",
                font=("Helvetica", 12),
                anchor="w", fg="#FF69B4", bg="white"
            ).grid(row=idx, column=1, sticky="w", padx=10, pady=2)

    frame_tombol = tk.Frame(frame_scrollable, pady=20)
    frame_tombol.pack(fill=tk.X)
    tk.Button(frame_tombol, text="Kembali ke Menu", font=("Helvetica", 15), bg="#FF69B4", fg="white", width=15, 
                        bd=0, relief="flat", activebackground="#D1006F", activeforeground="white", cursor="hand2", command=menu_admin).pack(anchor="center")

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

def tampilkan_tagihan():
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
        harga_per_kg = {
            "Baju": {"Normal": 4000, "Express": 5000},
            "Selimut/Seprai": {"Normal": 6000, "Express": 8000},
            "Karpet": {"Normal": 8000, "Express": 12000}
        }

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
                        bd=0, relief="flat", activebackground="#D1006F", activeforeground="white", cursor="hand2", command=kirim_tagihan).pack(pady=0.6)
            tk.Button(main_frame, text="Kembali ke Menu", font=("Helvetica", 15), bg="#FF69B4", fg="white", width=15, 
                        bd=0, relief="flat", activebackground="#D1006F", activeforeground="white", cursor="hand2", command=menu_admin).pack(pady=0.8)

        else:
            messagebox.showerror("Error", "ID Pesanan tidak ditemukan!")

    tk.Button(main_frame, text="Cari Tagihan", font=("Helvetica", 15), bg="#FF69B4", fg="white", width=15, 
                        bd=0, relief="flat", activebackground="#D1006F", activeforeground="white", cursor="hand2", command=hitung_tagihan).pack(pady=10)
    tk.Button(main_frame, text="Kembali ke Menu", font=("Helvetica", 15), bg="#FF69B4", fg="white", width=15, 
                        bd=0, relief="flat", activebackground="#D1006F", activeforeground="white", cursor="hand2", command=menu_admin).pack(pady=5)
    root.bind('<Return>', hitung_tagihan)

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

root = tk.Tk()
root.title("Swift Clean")

root.state=('zoomed')
root.resizable(True, True)

tampilkan_halaman_awal()

root.mainloop()