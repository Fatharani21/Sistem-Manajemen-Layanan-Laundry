import tkinter as tk
from tkinter import messagebox
import json
import os
from tkcalendar import Calendar

os.environ["TCL_LIBRARY"] = r"C:\Program Files\Python313\tcl\tcl8.6"
os.environ["TK_LIBRARY"] = r"C:\Program Files\Python313\tcl\tk8.6"

# Lokasi penyimpanan data
FILE_PESANAN = "pesanan.json"

# Membaca data pesanan dari file JSON
def muat_data():
    if not os.path.exists(FILE_PESANAN):
        with open(FILE_PESANAN, "w") as f:
            json.dump({}, f)
    with open(FILE_PESANAN, "r") as f:
        return json.load(f)

# Menyimpan data pesanan ke file JSON
def simpan_data(pesanan):
    with open(FILE_PESANAN, "w") as f:
        json.dump(pesanan, f, indent=4)

# Menghapus semua elemen dari jendela
def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()

# Halaman utama
def tampilkan_halaman_awal():
    clear_window(root)

    title_label = tk.Label(root, text="Swift Clean", font=("Helvetica", 60, "bold"))  
    title_label.pack(pady=100)

    caption_label = tk.Label(root, text="Washing, washing, washing \nIt’s Swift Clean, no stress!", font=("Helvetica", 20, "italic"), fg="gray")  # Abu
    caption_label.pack(pady=20)

    start_button = tk.Button(root, text="Mulai", font=("Helvetica", 16), command=menu_login)
    start_button.pack(pady=50)

    # Bind enter key to start the app
    root.bind('<Return>', lambda event: menu_login())

# Login
def menu_login():
    clear_window(root)

    tk.Label(root, text="Login", font=("Helvetica", 36, "bold")).pack(pady=20)
    tk.Label(root, text="Masukkan username dan password Anda", font=("Helvetica", 18)).pack(pady=10)

    tk.Label(root, text="Username:", font=("Helvetica", 16)).pack(pady=5)
    username_entry = tk.Entry(root, font=("Helvetica", 14))
    username_entry.pack(pady=5)

    tk.Label(root, text="Password:", font=("Helvetica", 16)).pack(pady=5)
    password_entry = tk.Entry(root, show="*", font=("Helvetica", 14))
    password_entry.pack(pady=5)

    def login(event=None):
        username = username_entry.get()
        password = password_entry.get()

        if username == "admin" and password == "rahasia":  # Login default untuk admin
            messagebox.showinfo("Login berhasil", "Selamat datang di Sistem Manajemen Laundry")
            menu_admin()  # Pindah ke menu admin setelah login berhasil
        else:
            messagebox.showerror("Login gagal", "Username atau password salah")

    login_button = tk.Button(root, text="Login", font=("Helvetica", 16), command=login)
    login_button.pack(pady=20)

    # Bind enter key for login
    root.bind('<Return>', login)

# Menu utama 
def menu_admin():
    clear_window(root)
    tk.Label(root, text="Menu Utama", font=("Helvetica", 36, "bold")).pack(pady=20)
    tk.Button(root, text="Tambah Pesanan", font=("Helvetica", 16), command=tampilkan_tambah_pesanan).pack(pady=10)
    tk.Button(root, text="Tampilkan Semua Pesanan", font=("Helvetica", 16), command=tampilkan_pesanan).pack(pady=10)
    tk.Button(root, text="Cetak Tagihan", font=("Helvetica", 16), command=tampilkan_tagihan).pack(pady=10)
    tk.Button(root, text="Logout", font=("Helvetica", 16), command=logout).pack(pady=10)

    # Bind enter key for logout
    root.bind('<Return>', lambda event: logout())

# Fungsi logout
def logout():
    messagebox.showinfo("Logout", "Anda telah logout. Program akan ditutup.")
    root.quit()  # Menutup aplikasi setelah logout
    
def buat_id_pesanan():
    data = muat_data()  # Ambil data pesanan dari sumber data
    # Hanya ambil ID pesanan yang valid (numerik)
    valid_ids = [id_pesanan for id_pesanan in data.keys() if id_pesanan.isdigit()]
    
    if valid_ids:  # Jika ada ID pesanan yang valid
        nomor_terakhir = max([int(id_pesanan) for id_pesanan in valid_ids])
    else:
        nomor_terakhir = 0  # Jika tidak ada ID pesanan sebelumnya, mulai dari 0
    
    # ID pesanan berikutnya dengan format 3 digit (contoh: 001, 002, ...)
    id_baru = str(nomor_terakhir + 1).zfill(3)
    
    return id_baru


def tampilkan_tambah_pesanan():
    clear_window(root)
    pesanan = muat_data()

    # Judul
    tk.Label(root, text="Tambah Pesanan Baru", font=("Helvetica", 16, "bold"), anchor="center").pack(pady=10, fill=tk.X, expand=True)

    # Nama pelanggan
    frame_nama = tk.Frame(root, pady=5)
    frame_nama.pack(fill=tk.X, expand=True)
    tk.Label(frame_nama, text="Nama Pelanggan:", font=("Helvetica", 10), width=20, anchor="center").pack(side=tk.LEFT, expand=True)
    nama_pelanggan_entry = tk.Entry(frame_nama, font=("Helvetica", 10), width=30, justify="center")
    nama_pelanggan_entry.pack(side=tk.LEFT, expand=True)

    # Email pelanggan
    frame_email = tk.Frame(root, pady=5)
    frame_email.pack(fill=tk.X, expand=True)
    tk.Label(frame_email, text="Email Pelanggan:", font=("Helvetica", 10), width=20, anchor="center").pack(side=tk.LEFT, expand=True)
    email_pelanggan_entry = tk.Entry(frame_email, font=("Helvetica", 10), width=30, justify="center")
    email_pelanggan_entry.pack(side=tk.LEFT, expand=True)

    # Jenis pakaian
    tk.Label(root, text="Jenis Pakaian:", font=("Helvetica", 10), anchor="center").pack(pady=5, fill=tk.X, expand=True)
    frame_jenis = tk.Frame(root)
    frame_jenis.pack(pady=5, expand=True)
    jenis_pakaian_values = {"Baju": tk.BooleanVar(), "Selimut/Seprai": tk.BooleanVar(), "Karpet": tk.BooleanVar()}
    berat_entries = {}

    for jenis in jenis_pakaian_values:
        col = tk.Frame(frame_jenis, padx=10)
        col.pack(side=tk.LEFT, expand=True)
        tk.Checkbutton(col, text=jenis, variable=jenis_pakaian_values[jenis], font=("Helvetica", 10), anchor="center").pack(pady=5)
        tk.Label(col, text="Berat (kg):", font=("Helvetica", 8), anchor="center").pack()
        berat_entries[jenis] = tk.Entry(col, font=("Helvetica", 8), width=8, justify="center")
        berat_entries[jenis].pack()

    # Jenis layanan
    frame_layanan = tk.Frame(root, pady=5)
    frame_layanan.pack(fill=tk.X, expand=True)
    tk.Label(frame_layanan, text="Jenis Layanan:", font=("Helvetica", 10), width=20, anchor="center").pack(side=tk.LEFT, expand=True)
    layanan_options = ["", "Normal", "Express"]  # Tambahkan pilihan kosong
    jenis_layanan = tk.StringVar(value="")  # Default kosong
    layanan_menu = tk.OptionMenu(frame_layanan, jenis_layanan, *layanan_options)
    layanan_menu.config(width=20)
    layanan_menu.pack(side=tk.LEFT, expand=True)

    # Estimasi tanggal selesai
    tk.Label(root, text="Estimasi Tanggal Selesai:", font=("Helvetica", 10), anchor="center").pack(pady=5, fill=tk.X, expand=True)
    kalender = Calendar(root, selectmode="day")
    kalender.pack(pady=5, expand=True)

    # Fungsi untuk menyimpan pesanan
    def simpan_pesanan(event=None):
        nama_pelanggan = nama_pelanggan_entry.get()
        email_pelanggan = email_pelanggan_entry.get()
        layanan = jenis_layanan.get()
        estimasi_waktu = kalender.get_date()

        pesanan_baru = []

        # Validasi nama pelanggan
        if not nama_pelanggan.isalpha():
            messagebox.showerror("Error", "Nama pelanggan hanya boleh berupa huruf!")
            return

        # Validasi email
        if "@" not in email_pelanggan or "." not in email_pelanggan:
            messagebox.showerror("Error", "Email tidak valid!")
            return

        # Validasi apakah jenis pakaian sudah dipilih terlebih dahulu
        jenis_pakaian_terpilih = False  # Flag untuk memeriksa apakah jenis pakaian dipilih
        for jenis, var in jenis_pakaian_values.items():
            if var.get():  # Jika jenis pakaian dipilih
                jenis_pakaian_terpilih = True  # Tandai bahwa jenis pakaian dipilih
                berat = berat_entries[jenis].get()
                if not berat.isdigit():  # Validasi berat harus berupa angka
                    messagebox.showerror("Error", f"Berat untuk {jenis} harus berupa angka!")
                    return
                pesanan_baru.append({
                    "jenis_pakaian": jenis,
                    "berat": float(berat),
                    "jenis_layanan": layanan,
                    "estimasi_waktu": estimasi_waktu
                })
    
        if not jenis_pakaian_terpilih:  # Jika tidak ada jenis pakaian yang dipilih
            messagebox.showerror("Error", "Pilih jenis pakaian terlebih dahulu!")
            return

        # Validasi jenis layanan
        if not layanan:
            messagebox.showerror("Error", f"Jenis layanan harus terisi!")
            return

        # Validasi input
        if nama_pelanggan and email_pelanggan and pesanan_baru and layanan:
            # Buat ID Pesanan Baru
            id_pesanan = buat_id_pesanan()
            
                        # Menambahkan pesanan baru dengan ID pesanan
            pesanan[id_pesanan] = {
                "nama_pelanggan": nama_pelanggan,
                "email": email_pelanggan,
                "items": pesanan_baru
            }

        # Menambahkan pesanan baru dengan ID pesanan
        pesanan[id_pesanan] = {
            "nama_pelanggan": nama_pelanggan,
            "email": email_pelanggan,
            "items": pesanan_baru
        }

        simpan_data(pesanan)  # Simpan data yang sudah diupdate
        messagebox.showinfo("Pesanan berhasil", f"Pesanan {id_pesanan} berhasil ditambahkan!")
        menu_admin()  # Kembali ke menu admin
       
    # Tombol simpan
    frame_tombol = tk.Frame(root, pady=10)
    frame_tombol.pack(fill=tk.X, anchor="center", expand=True)
    
    # Tombol Kembali di sebelah kiri
    tk.Button(frame_tombol, text="Kembali ke Menu", font=("Helvetica", 10), command=menu_admin).pack(side=tk.LEFT, padx=5, expand=True)
    
    # Tombol Simpan di sebelah kanan
    tk.Button(frame_tombol, text="Simpan Pesanan", font=("Helvetica", 10), command=simpan_pesanan).pack(side=tk.RIGHT, padx=5, expand=True)
    
    root.bind('<Return>', simpan_pesanan)
    
# Membuat window utama
root = tk.Tk()
root.title("Swift Clean Laundry Management System")
root.geometry("600x600")  # Ukuran window

tampilkan_halaman_awal()

root.mainloop()