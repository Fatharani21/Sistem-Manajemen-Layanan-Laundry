import re
from tkinter import messagebox
from datetime import datetime
from data import muat_data_akun
  
def validasi_akun_baru(username, password):
    if not username or not password:
        messagebox.showerror("Error", "Username dan Password harus diisi!")
        return False
    if len(username) < 3:
        messagebox.showerror("Error", "Username harus terdiri dari minimal 3 karakter!")
        return False
    if not re.search("[A-Za-z]", password) or not re.search("[0-9]", password):
        messagebox.showerror("Error", "Password harus mengandung kombinasi huruf dan angka!")
        return False
    
    users = muat_data_akun()
    
    if username in users:
        messagebox.showerror("Error", "Username sudah ada, coba username lain.")
        return False
    return True

def validasi_login(username, password):
    users = muat_data_akun()
    if username in users and users[username]["password"] == password:
        return True
    else:
        messagebox.showerror("Login gagal", "Username atau password salah")
        return False

def validasi_nama_pelanggan(nama):
    if len(nama) < 3:
        messagebox.showerror("Error", "Nama pelanggan harus terdiri dari minimal 3 karakter dan berupa huruf!")
        return False
    if not re.match("^[A-Za-z ]+$", nama):
        messagebox.showerror("Error", "Nama pelanggan hanya boleh mengandung huruf dan spasi!")
        return False
    return True

def validasi_email(email):
    if "@" not in email or "." not in email:
        messagebox.showerror("Error", "Email tidak valid!")
        return False
    return True

def validasi_tanggal(estimasi_waktu):
    current_date = datetime.now()
    tanggal_pilihan_obj = datetime.strptime(estimasi_waktu, "%m/%d/%y")
    if tanggal_pilihan_obj < current_date:
        messagebox.showerror("Error", "Tanggal yang dipilih tidak valid! Pilih tanggal setelah hari pesanan dibuat.")
        return False
    return True

def validasi_layanan(layanan):
    if not layanan:
        messagebox.showerror("Error", "Jenis layanan harus terisi!")
        return False
    return True

def validasi_jenis_pakaian(jenis_pakaian_values, berat_entries, layanan, estimasi_waktu):
    if not isinstance(jenis_pakaian_values, dict) or not isinstance(berat_entries, dict):
        return False, "Data jenis pakaian atau berat tidak valid!"  

    pakaian_terpilih = []  
    pesan_error = ""

    for jenis, var in jenis_pakaian_values.items():
        if var.get():  
            berat = berat_entries.get(jenis, None)  
            if berat is None or not berat.get():  
                pesan_error = f"Berat untuk {jenis} harus diisi!"  
                return False, pesan_error
            
            if berat.get().isdigit():  
                pakaian_terpilih.append({
                    "jenis_pakaian": jenis,
                    "berat": float(berat.get()),  
                    "jenis_layanan": layanan,
                    "estimasi_waktu": estimasi_waktu
                })
            else:
                pesan_error = f"Berat untuk {jenis} harus berupa angka!"  
                return False, pesan_error

    if not pakaian_terpilih:  
        pesan_error = "Pilih jenis pakaian terlebih dahulu!"  
        return False, pesan_error

    return pakaian_terpilih, None 

def validasi_harga(normal, express, jenis):
    if not normal or not express:
        messagebox.showerror("Error", f"Kolom untuk {jenis} tidak boleh kosong!")
        return False
    
    if not normal.isdigit() or not express.isdigit():
        messagebox.showerror("Error", f"Input untuk {jenis} harus berupa angka!")
        return False

    return True