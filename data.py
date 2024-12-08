import json
import os

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
        
current_user = None
        
def muat_data_pesanan(current_user):
    pesanan_file = f"user_data/{current_user}/{current_user}_pesanan.json"
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


        