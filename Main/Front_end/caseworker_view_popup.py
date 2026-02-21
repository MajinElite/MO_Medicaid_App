# Front_end/caseworker_view_popup.py
import customtkinter as ctk

def open_view_popup(parent, app_data: dict):
    popup = ctk.CTkToplevel(parent)
    popup.title("Application Details")
    popup.geometry("520x420")

    ctk.CTkLabel(popup, text="Full Application Details", font=("Helvetica", 18, "bold")).pack(pady=15)

    box = ctk.CTkScrollableFrame(popup, width=480, height=280)
    box.pack(padx=15, pady=10, fill="both", expand=True)

    for k, v in app_data.items():
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=8, pady=6)
        ctk.CTkLabel(row, text=f"{k}:", font=("Helvetica", 12, "bold"), width=180, anchor="w").pack(side="left")
        ctk.CTkLabel(row, text=str(v), anchor="w").pack(side="left")

    ctk.CTkButton(popup, text="Close", fg_color="gray", command=popup.destroy).pack(pady=15)