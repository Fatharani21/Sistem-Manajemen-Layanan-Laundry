import tkinter as tk
from tkinter import messagebox
import json
import os

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
    
# Membuat window utama
root = tk.Tk()
root.title("Swift Clean Laundry Management System")
root.geometry("600x600")  # Ukuran window

tampilkan_halaman_awal()

root.mainloop()