import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from Crypto.Cipher import AES, DES, Blowfish, DES3
from Crypto.Random import get_random_bytes
import pyperclip  # Required for copying text to clipboard
from ttkthemes import ThemedStyle
import os

class FileEncryptorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("File Encryptor")
        self.master.geometry("400x600")

        self.style = ThemedStyle(master)
        self.style.set_theme("plastik")  # Choose a theme, you can try "arc" or "equilux"

        self.algorithms = ["AES", "DES", "Blowfish", "Triple DES"]  # Add more algorithms as needed

        self.file_label = ttk.Label(master, text="Select File:", font=("Arial", 12))
        self.file_label.grid(row=0, column=0, padx=10, pady=5)

        self.file_entry = ttk.Entry(master, width=30, font=("Arial", 10))
        self.file_entry.grid(row=0, column=1, padx=10, pady=5)

        self.file_button = ttk.Button(master, text="Browse", command=self.browse_file, style="Accent.TButton")
        self.file_button.grid(row=0, column=2, padx=5, pady=5)

        self.dest_folder_label = ttk.Label(master, text="Destination Folder:", font=("Arial", 12))
        self.dest_folder_label.grid(row=1, column=0, padx=10, pady=5)

        self.dest_folder_entry = ttk.Entry(master, width=30, font=("Arial", 10))
        self.dest_folder_entry.grid(row=1, column=1, padx=10, pady=5)

        self.dest_folder_button = ttk.Button(master, text="Choose Folder", command=self.choose_folder, style="Accent.TButton")
        self.dest_folder_button.grid(row=1, column=2, padx=5, pady=5)

        self.password_label = ttk.Label(master, text="Password:", font=("Arial", 12))
        self.password_label.grid(row=2, column=0, padx=10, pady=5)

        self.password_entry = ttk.Entry(master, show="*", width=30, font=("Arial", 10))
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        self.algorithm_label = ttk.Label(master, text="Encryption Algorithm:", font=("Arial", 12))
        self.algorithm_label.grid(row=3, column=0, padx=10, pady=5)

        self.algorithm_combo = ttk.Combobox(master, values=self.algorithms, width=27, font=("Arial", 10))
        self.algorithm_combo.grid(row=3, column=1, padx=10, pady=5)

        self.encrypt_button = ttk.Button(master, text="Encrypt", command=self.encrypt, style="Accent.TButton")
        self.encrypt_button.grid(row=4, column=1, padx=5, pady=10)

        self.decrypt_button = ttk.Button(master, text="Decrypt", command=self.decrypt, style="Accent.TButton")
        self.decrypt_button.grid(row=4, column=2, padx=5, pady=10)

        self.key_label = ttk.Label(master, text="Encryption Key:", font=("Arial", 12))
        self.key_label.grid(row=5, column=0, padx=10, pady=5)

        self.key_display = tk.Text(master, width=30, height=2, font=("Arial", 10))
        self.key_display.grid(row=5, column=1, padx=10, pady=5)

        self.copy_button = ttk.Button(master, text="Copy Key", command=self.copy_key, style="Accent.TButton")
        self.copy_button.grid(row=6, column=1, padx=5, pady=5)

    def browse_file(self):
        filename = filedialog.askopenfilename()
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, filename)

    def choose_folder(self):
        foldername = filedialog.askdirectory()
        self.dest_folder_entry.delete(0, tk.END)
        self.dest_folder_entry.insert(0, foldername)

    def pad_data(self, data, block_size):
        pad_size = block_size - (len(data) % block_size)
        return data + bytes([pad_size] * pad_size)

    def unpad_data(self, data):
        pad_size = data[-1]
        return data[:-pad_size]

    def encrypt(self):
        input_file = self.file_entry.get()
        password = self.password_entry.get()
        algorithm = self.algorithm_combo.get()
        destination_folder = self.dest_folder_entry.get()

        try:
            with open(input_file, 'rb') as file:
                plaintext = file.read()
                if algorithm == "AES":
                    key = get_random_bytes(16)
                    cipher = AES.new(key, AES.MODE_ECB)
                elif algorithm == "DES":
                    key = get_random_bytes(8)
                    cipher = DES.new(key, DES.MODE_ECB)
                elif algorithm == "Blowfish":
                    key = get_random_bytes(16)
                    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
                elif algorithm == "Triple DES":
                    key = get_random_bytes(24)  # Generate a valid TDES key
                    cipher = DES3.new(key, DES3.MODE_ECB)

                padded_plaintext = self.pad_data(plaintext, cipher.block_size)
                ciphertext = cipher.encrypt(padded_plaintext)

            output_file = destination_folder + "/encrypted_" + os.path.basename(input_file)
            with open(output_file, 'wb') as file:
                file.write(ciphertext)

            self.key_display.insert(tk.END, key.hex())
            messagebox.showinfo("Encryption", "File encrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decrypt(self):
        input_file = self.file_entry.get()
        password = self.password_entry.get()
        algorithm = self.algorithm_combo.get()
        destination_folder = self.dest_folder_entry.get()

        try:
            with open(input_file, 'rb') as file:
                ciphertext = file.read()

            if algorithm == "AES":
                key = bytes.fromhex(self.key_display.get("1.0", "end-1c"))
                cipher = AES.new(key, AES.MODE_ECB)
            elif algorithm == "DES":
                key = bytes.fromhex(self.key_display.get("1.0", "end-1c"))
                cipher = DES.new(key, DES.MODE_ECB)
            elif algorithm == "Blowfish":
                key = bytes.fromhex(self.key_display.get("1.0", "end-1c"))
                cipher = Blowfish.new(key, Blowfish.MODE_ECB)
            elif algorithm == "Triple DES":
                key = bytes.fromhex(self.key_display.get("1.0", "end-1c"))
                cipher = DES3.new(key, DES3.MODE_ECB)

            plaintext = cipher.decrypt(ciphertext)
            unpadded_plaintext = self.unpad_data(plaintext)

            output_file = destination_folder + "/decrypted_" + os.path.basename(input_file)[10:]  # Remove "encrypted_" from filename
            with open(output_file, 'wb') as file:
                file.write(unpadded_plaintext)

            messagebox.showinfo("Decryption", "File decrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def copy_key(self):
        key = self.key_display.get("1.0", "end-1c")
        pyperclip.copy(key)
        messagebox.showinfo("Copy Key", "Key copied to clipboard!")

def main():
    root = tk.Tk()
    app = FileEncryptorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
