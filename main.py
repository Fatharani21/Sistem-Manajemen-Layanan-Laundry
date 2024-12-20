from user_interface import tampilkan_halaman_awal
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Swift Clean")
    root.state('zoomed')  
    root.resizable(True, True)  

    tampilkan_halaman_awal(root)  
    root.mainloop()

