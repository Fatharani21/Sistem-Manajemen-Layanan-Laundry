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

        if username == "admin" and password == "rahasia":  
            messagebox.showinfo("Login berhasil", "Selamat datang di Swift Clean")
            menu_admin()  
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
    data = muat_data()  
    # Hanya ambil ID pesanan yang valid (numerik)
    valid_ids = [id_pesanan for id_pesanan in data.keys() if id_pesanan.isdigit()]
    
    if valid_ids:  # Jika ada ID pesanan yang valid
        nomor_terakhir = max([int(id_pesanan) for id_pesanan in valid_ids])
    else:
        nomor_terakhir = 0  # Jika tidak ada ID pesanan sebelumnya, mulai dari 0
    
    # ID pesanan berikutnya dengan format 3 digit 
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
            messagebox.showerror("Error", "Nama pelanggan hanya bisa berupa huruf!")
            return

        # Validasi email
        if "@" not in email_pelanggan or "." not in email_pelanggan:
            messagebox.showerror("Error", "Email tidak valid!")
            return

        # Validasi apakah jenis pakaian sudah dipilih terlebih dahulu
        jenis_pakaian_terpilih = False  
        for jenis, var in jenis_pakaian_values.items():
            if var.get():  
                jenis_pakaian_terpilih = True  
                berat = berat_entries[jenis].get()
                if not berat.isdigit():
                    messagebox.showerror("Error", f"Berat {jenis} harus berupa angka!")
                    return
                pesanan_baru.append({
                    "jenis_pakaian": jenis,
                    "berat": float(berat),
                    "jenis_layanan": layanan,
                    "estimasi_waktu": estimasi_waktu
                })
    
        if not jenis_pakaian_terpilih:  
            messagebox.showerror("Error", "Jenis pakaian harus terisi!")
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

        simpan_data(pesanan)  
        messagebox.showinfo("Pesanan berhasil", f"Pesanan {id_pesanan} berhasil ditambahkan!")
        menu_admin()  
       
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
root.geometry("600x600")  

tampilkan_halaman_awal()

root.mainloop()

def tampilkan_pesanan():
    clear_window(root) 
    
    # Membuat canvas dan scrollbar untuk scrollable area
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    frame_scrollable = tk.Frame(canvas)

    frame_scrollable.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=frame_scrollable, anchor="nw")
    canvas.config(yscrollcommand=scrollbar.set)
    
    bg_image = Image.open(r"C:\Users\listi\OneDrive\Desktop\anaa\Images\yyyy.png")
    bg_image = ImageTk.PhotoImage(bg_image)
    
    canvas.create_image(0, 0, image=bg_image, anchor="nw")
     
    # Menempatkan canvas dan scrollbar di jendela
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    canvas.image = bg_image
    
    # Menambahkan dukungan scroll untuk touchpad (dua jari)
    def on_mouse_wheel(event):
        if event.delta:  # Untuk Windows dan Mac
            canvas.yview_scroll(-1 * (event.delta // 120), "units")
        elif event.num in (4, 5):  # Untuk Linux (event num 4=up, 5=down)
            canvas.yview_scroll(-1 if event.num == 4 else 1, "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Windows dan MacOS
    canvas.bind_all("<Button-4>", on_mouse_wheel)   # Linux (scroll up)
    canvas.bind_all("<Button-5>", on_mouse_wheel)   # Linux (scroll down)

    # Judul (centered)
    title_frame = tk.Frame(frame_scrollable)
    title_frame.pack(fill=tk.X, pady=20)
    tk.Label(title_frame, text="Daftar Pesanan", font=("Helvetica", 20, "bold")).pack(anchor="center")
    
    # Memuat data pesanan
    pesanan = muat_data()
    
    # Menampilkan setiap pesanan pelanggan
    for id_pesanan, data in pesanan.items():
        # Frame untuk ID Pesanan dan nama pelanggan
        frame_pesanan = tk.Frame(frame_scrollable, padx=20)
        frame_pesanan.pack(fill=tk.X, expand=True)
        # ID Pesanan
        tk.Label(
            frame_pesanan,
            text=f"ID Pesanan: {id_pesanan}",
            font=("Helvetica", 14, "bold"),
            anchor="w"
        ).grid(row=0, column=0, sticky="w", columnspan=2, pady=5)

        # Nama pelanggan di bawah ID Pesanan
        tk.Label(
            frame_pesanan,
            text=f"Nama: {data['nama_pelanggan']} ({data['email']})",
            font=("Helvetica", 12, "bold"),  # Bold untuk nama
            anchor="w"
            ).grid(row=1, column=0, sticky="w", columnspan=2, pady=5)

    
        # Menampilkan item pesanan
        for item in data.get("items", []):
            frame_item = tk.Frame(frame_scrollable, padx=20, pady=10)
            frame_item.pack(fill=tk.X, expand=True)
            tk.Label(frame_item, text=f"{item['jenis_pakaian']} - Berat: {item['berat']}kg, Layanan: {item['jenis_layanan']}, Estimasi: {item['estimasi_waktu']}",
                     font=("Helvetica", 12)).pack()
        
        # Header untuk daftar item
        tk.Label(
            frame_pesanan,
            text="Daftar Item:",
            font=("Helvetica", 12, "italic"),
            anchor="w"
        ).grid(row=2, column=0, sticky="w", columnspan=2, pady=5)

        # Menampilkan daftar item dengan grid
        for idx, item in enumerate(data.get("items", []), start=3):  # Mulai dari baris ke-3
            tk.Label(
                frame_pesanan,
                text=f"• {item['jenis_pakaian']} - Berat: {item['berat']}kg",
                font=("Helvetica", 12),
                anchor="w"
            ).grid(row=idx, column=0, sticky="w", pady=2)
            tk.Label(
                frame_pesanan,
                text=f"Layanan: {item['jenis_layanan']}, Estimasi: {item['estimasi_waktu']}",
                font=("Helvetica", 12),
                anchor="w"
            ).grid(row=idx, column=1, sticky="w", padx=20, pady=2)

    # Tombol kembali ke menu
    frame_tombol = tk.Frame(frame_scrollable, pady=20)
    frame_tombol.pack(fill=tk.X)
    tk.Button(
        frame_tombol,
        text="Kembali ke Menu",
        font=("Helvetica", 14),
        command=menu_admin 
    ).pack(anchor="center")
    
    
from PIL import Image, ImageDraw, ImageFont

def buat_gambar_struk(nama_file, id_pesanan, nama_pelanggan, tanggal_str, tanggal_estimasi, tagihan_text, total_tagihan):
    width, height = 500, 800
    img = Image.new("RGB", (width, height), "white")

    draw = ImageDraw.Draw(img)
        
    # Font
    font_path = "C:/Windows/Fonts/consola.ttf"  # Courier New atau Consolas
    font_header = ImageFont.truetype(font_path, 18)
    font_body = ImageFont.truetype(font_path, 14)
    
    # Header
    y = 40  # Awal posisi Y
    header_text = "Swift Clean Laundry"
    sub_header_text = "Struk Resmi Layanan Laundry"

    # Hitung posisi X agar teks benar-benar berada di tengah
    header_width = draw.textlength(header_text, font=font_header)
    sub_header_width = draw.textlength(sub_header_text, font=font_body)

    draw.text(((width - header_width) // 2, y), header_text, font=font_header, fill="black")
    y += 30  # Jarak antar teks
    draw.text(((width - sub_header_width) // 2, y), sub_header_text, font=font_body, fill="black")

    # Garis pemisah atas (tebal)
    y += 30
    draw.line((20, y, width - 20, y), fill="black", width=2)

    # Informasi pelanggan
    y += 20
    draw.text((20, y), f"ID Pesanan      : {id_pesanan}", font=font_body, fill="black")
    y += 20
    draw.text((20, y), f"Nama Pelanggan  : {nama_pelanggan}", font=font_body, fill="black")
    y += 20
    draw.text((20, y), f"Tanggal Tagihan : {tanggal_str}", font=font_body, fill="black")
    y += 20
    draw.text((20, y), f"Estimasi Selesai: {tanggal_estimasi}", font=font_body, fill="black")

    # Garis pemisah sebelum tabel (tebal)
    y += 30
    draw.line((20, y, width - 20, y), fill="black", width=2)

    # Header tabel
    y += 20
    draw.text((20, y), "|  Jenis Pakaian  |  Berat   |  Layanan |     Biaya    |", font=font_body, fill="black")
    
    # Garis pemisah tabel (biasa)
    y += 20
    draw.line((20, y, width - 20, y), fill="black", width=1)

    # Isi tabel
    y += 10  # Jarak kecil sebelum isi tabel
    for line in tagihan_text.splitlines():
        draw.text((20, y), line, font=font_body, fill="black")
        y += 20  # Tambahkan jarak antar baris

    # Garis pemisah sebelum total tagihan (panjang penuh)
    y += 10
    draw.line((20, y, width - 20, y), fill="black", width=1)

    # Total tagihan
    y += 20
    draw.text((20, y), f"Total Tagihan   :                         Rp  {total_tagihan:,}", font=font_body, fill="black")

    # Garis pemisah bawah (tebal)
    y += 30
    draw.line((20, y, width - 20, y), fill="black", width=2)

    # Footer
    y += 20
    draw.text((width // 2 - 110, y), "Terima Kasih telah menggunakan", font=font_body, fill="black")
    y += 20
    draw.text((width // 2 - 80, y), "Swift Clean Laundry!", font=font_body, fill="black")

    # Menyimpan gambar
    img.save(nama_file)
    print(f"Struk berhasil dibuat: {nama_file}")

# Fungsi untuk mengirim email dengan lampiran gambar
def kirim_email_dengan_gambar(nama_file, email_pelanggan):
    msg = MIMEMultipart()
    msg["From"] = "gajello66@gmail.com"
    msg["To"] = email_pelanggan
    msg["Subject"] = "Struk Laundry Anda"

    # Tambahkan pesan teks
    body = "Berikut adalah struk laundry Anda dalam format gambar."
    msg.attach(MIMEText(body, "plain"))

    # Lampirkan file gambar
    with open(nama_file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={nama_file}")
        msg.attach(part)

    # Kirim email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("gajello66@gmail.com", "ogcz xnuk wwwc uecc")
        server.sendmail(msg["From"], msg["To"], msg.as_string())

# Modifikasi fungsi tampilkan_tagihan
def tampilkan_tagihan():
    clear_window(root)
    
    bg_image = Image.open(r"C:\Users\listi\OneDrive\Desktop\anaa\Images\cetak_tagihan.png")
    bg_image = ImageTk.PhotoImage(bg_image)
    
    background_label = tk.Label(root, image=bg_image)
    background_label.place(relwidth=1, relheight=1)
    
    id_pesanan_entry = tk.Entry(root, font=("Helvetica", 14))
    id_pesanan_entry.pack(pady=10)
    id_pesanan_entry.place(relx=0.5, rely=0.254, anchor="center")
    
    background_label.image = bg_image
    
    def hitung_tagihan(event=None): 
        id_pesanan = id_pesanan_entry.get().strip()  # Ambil ID Pesanan dan hilangkan spasi
        pesanan = muat_data()  # Muat data pesanan dari sumber data
        harga_per_kg = {
            "Baju": {"Normal": 4000, "Express": 5000},
            "Selimut/Seprai": {"Normal": 6000, "Express": 8000},
            "Karpet": {"Normal": 8000, "Express": 12000}
        }
    
        # Cari pesanan berdasarkan ID Pesanan (sebagai kunci dictionary)
        if id_pesanan in pesanan:
            # Ambil data pelanggan berdasarkan ID pesanan
            data_pesanan = pesanan[id_pesanan]
            nama_pelanggan = data_pesanan['nama_pelanggan']
            email_pelanggan = data_pesanan['email']

            # Hitung total tagihan
            total_tagihan = 0
            tagihan_text = ""
            
            for item in data_pesanan['items']:
                jenis = item["jenis_pakaian"]
                layanan = item["jenis_layanan"]
                berat = item["berat"]
                biaya = berat * harga_per_kg[jenis][layanan]
                total_tagihan += biaya
                tagihan_text += f"| {jenis:<15} | {berat:<6}kg | {layanan:<8} | Rp{biaya:>10,} |\n"

            # Ambil tanggal estimasi dari data pesanan
            tanggal_estimasi = data_pesanan['items'][0]["estimasi_waktu"]
            tanggal_estimasi = datetime.strptime(tanggal_estimasi, "%m/%d/%y").strftime("%d/%m/%Y")
            
            # Buat struk menggunakan data estimasi selesai
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
Total Tagihan   :                         Rp  {total_tagihan:,.1f}
========================================================
              Terima Kasih telah menggunakan
                  Swift Clean Laundry!
========================================================
"""

            # Menampilkan tagihan di GUI
            clear_window(root)
            
            tk.Label(root, text="Struk Tagihan", font=("Helvetica", 24, "bold")).pack(pady=10)
            tk.Label(root, text=struk, font=("Courier", 12), justify="left").pack(pady=10)

            # Simpan struk sebagai gambar
            nama_file = f"struk_{id_pesanan}.png"  # Ganti nama file dengan ID pesanan
            buat_gambar_struk(nama_file, id_pesanan, nama_pelanggan, tanggal_str, tanggal_estimasi, tagihan_text, total_tagihan)
            
            # Fungsi kirim email
            def kirim_tagihan():
                kirim_email_dengan_gambar(nama_file, email_pelanggan)
                messagebox.showinfo("Email Dikirim", "Struk berhasil dikirim ke email pelanggan!")

            # Menampilkan tombol
            tk.Button(root, text="Kirim Tagihan via Email", font=("Helvetica", 16), command=kirim_tagihan).pack(pady=5)
            tk.Button(root, text="Kembali ke Menu", font=("Helvetica", 16), command=menu_admin).pack(side=tk.BOTTOM, pady=10)
            
        else:
            messagebox.showerror("Error", "ID Pesanan tidak ditemukan!")

    tk.Button(root, text="Cari Tagihan", font=("Helvetica", 16), command=hitung_tagihan).place(relx=0.5, rely=0.4, anchor="center")
    tk.Button(root, text="Kembali ke Menu", font=("Helvetica", 16), command=menu_admin).place(relx=0.5, rely=0.53, anchor="center")
    root.bind('<Return>', hitung_tagihan)