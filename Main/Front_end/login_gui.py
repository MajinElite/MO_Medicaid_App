# Front_end/login_gui.py
import customtkinter as ctk
from tkinter import messagebox

from Back_end.auth import authenticate_user

# --- BRAND COLORS ---
HEADER_BLUE = "#5b9bd5"
BTN_GREEN = "#7dd169"

class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Header
        ctk.CTkLabel(
            self,
            text="Missouri Medicaid",
            font=("Helvetica", 24, "bold"),
            fg_color=HEADER_BLUE,
            text_color="white",
            corner_radius=0
        ).pack(fill="x", ipady=15)

        ctk.CTkLabel(self, text="Login", font=("Helvetica", 20, "bold")).pack(pady=(25, 10))

        form = ctk.CTkFrame(self, fg_color="transparent")
        form.pack(pady=10)

        # Email
        ctk.CTkLabel(form, text="Email").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.email_entry = ctk.CTkEntry(form, width=280)
        self.email_entry.grid(row=0, column=1, pady=10)

        # Password
        ctk.CTkLabel(form, text="Password").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.password_entry = ctk.CTkEntry(form, width=280, show="*")
        self.password_entry.grid(row=1, column=1, pady=10)

        # Button
        ctk.CTkButton(
            self,
            text="Login",
            font=("Helvetica", 14, "bold"),
            fg_color=BTN_GREEN,
            command=self.login
        ).pack(pady=20, ipadx=12, ipady=6)

        ctk.CTkLabel(
            self,
            text="Credentials come from database.json (backend).",
            text_color="gray"
        ).pack(pady=5)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showerror("Error", "Please enter email and password.")
            return

        user = authenticate_user(email, password)

        if not user:
            messagebox.showerror("Error", "Invalid credentials.")
            return

        # normalize role so we never mis-route because of casing/spaces
        role = (user.get("role") or "").strip().lower()

        # store session in a consistent shape for the rest of the app
        self.controller.set_user({
            "email": user.get("email"),
            "role": role
        })

        # route correctly
        if role == "applicant":
            self.controller.show_applicant_dashboard()
        elif role == "caseworker":
            self.controller.show_caseworker_dashboard()
        else:
            messagebox.showerror("Error", f"Unknown role in database.json: {user.get('role')}")