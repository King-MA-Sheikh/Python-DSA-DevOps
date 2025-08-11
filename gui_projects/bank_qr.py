import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import qrcode
import os
import urllib.parse

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    win.geometry(f"{width}x{height}+{x}+{y}")

def generate_qr():
    bank_name = entry_bank.get().strip()
    account_name = entry_name.get().strip()
    account_number = entry_account.get().strip()
    ifsc_code = entry_ifsc.get().strip()
    upi_id = entry_upi.get().strip()

    # --- Validation ---
    if not bank_name.isalpha():
        messagebox.showerror("Error", "Bank Name must contain only letters.")
        return
    if not account_number.isdigit():
        messagebox.showerror("Error", "Account Number must contain only numbers.")
        return
    if not ifsc_code.isalnum():
        messagebox.showerror("Error", "IFSC Code must be alphanumeric.")
        return
    if not upi_id or "@" not in upi_id:
        messagebox.showerror("Error", "Enter a valid UPI ID (e.g. name@bank).")
        return
    if not account_name:
        messagebox.showerror("Error", "Please enter the Account Holder Name.")
        return

    # Encode account holder name for URL
    encoded_name = urllib.parse.quote(account_name)

    # --- UPI Payment QR Format ---
    qr_data = f"upi://pay?pa={upi_id}&pn={encoded_name}&cu=INR"

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_path = "payment_qr.png"
    img.save(img_path)

    img_open = Image.open(img_path)
    img_open = img_open.resize((200, 200), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_open)
    label_qr.config(image=img_tk)
    label_qr.image = img_tk

    messagebox.showinfo("Success", f"Payment QR Code saved as {os.path.abspath(img_path)}")

# GUI Setup
root = tk.Tk()
root.title("UPI Payment QR Code Generator")
center_window(root, 400, 600)
root.resizable(False, False)

tk.Label(root, text="Bank Name:").pack(pady=5)
entry_bank = tk.Entry(root, width=40)
entry_bank.pack()

tk.Label(root, text="Account Holder Name:").pack(pady=5)
entry_name = tk.Entry(root, width=40)
entry_name.pack()

tk.Label(root, text="Account Number:").pack(pady=5)
entry_account = tk.Entry(root, width=40)
entry_account.pack()

tk.Label(root, text="IFSC Code:").pack(pady=5)
entry_ifsc = tk.Entry(root, width=40)
entry_ifsc.pack()

tk.Label(root, text="UPI ID:").pack(pady=5)
entry_upi = tk.Entry(root, width=40)
entry_upi.pack()

tk.Button(root, text="Generate Payment QR", command=generate_qr, bg="blue", fg="white").pack(pady=15)

label_qr = tk.Label(root)
label_qr.pack(pady=10)

root.mainloop()
