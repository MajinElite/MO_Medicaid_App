# Front_end/login_gui.py
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from Back_end.auth import authenticate_user

# --- BRAND COLORS ---
PRIMARY_BLUE = "#3b82f6"
LIGHT_GRAY = "#f5f5f5"
CARD_BG = "#ffffff"
TEXT_GRAY = "#6b7280"

class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Center container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True)

        # ================= CARD =================
        card = ctk.CTkFrame(
            container,
            width=380,
            height=440,  # slightly taller for spacing
            corner_radius=20,
            fg_color=CARD_BG
        )
        card.pack(pady=40)
        card.pack_propagate(False)

        # ================= LOGO IMAGE =================
        try:
            self.logo_image = ctk.CTkImage(
                light_image=Image.open("momedicom.png"),
                size=(70, 70)
            )

            ctk.CTkLabel(
                card,
                image=self.logo_image,
                text=""
            ).pack(pady=(25, 15))

        except:
            ctk.CTkLabel(
                card,
                text="LOGO",
                text_color="white",
                fg_color=PRIMARY_BLUE,
                width=60,
                height=60,
                corner_radius=10
            ).pack(pady=(25, 15))

        # ================= TITLE =================
        ctk.CTkLabel(
            card,
            text="Login",
            font=("Helvetica", 20, "bold"),
            text_color="black"
        ).pack(pady=(0, 15))

        # ================= EMAIL =================
        email_frame = ctk.CTkFrame(card, fg_color="transparent", width=300)
        email_frame.pack(pady=8, anchor="center")

        ctk.CTkLabel(
            email_frame,
            text="👤",
            font=("Segoe UI Emoji", 16)
        ).pack(side="left", padx=(0, 10))

        self.email_entry = ctk.CTkEntry(
            email_frame,
            width=250,
            height=40,
            placeholder_text="Email"
        )
        self.email_entry.pack(side="left", expand=True)

        # ================= PASSWORD =================
        password_frame = ctk.CTkFrame(card, fg_color="transparent", width=300)
        password_frame.pack(pady=8, anchor="center")

        ctk.CTkLabel(
            password_frame,
            text="🔒",
            font=("Segoe UI Emoji", 16)
        ).pack(side="left", padx=(0, 10))

        self.password_entry = ctk.CTkEntry(
            password_frame,
            width=250,
            height=40,
            placeholder_text="Password",
            show="*"
        )
        self.password_entry.pack(side="left")

        # ================= REMEMBER ME =================
        remember_frame = ctk.CTkFrame(card, fg_color="transparent")
        remember_frame.pack(fill="x", padx=60, pady=(5, 10))

        self.remember_var = ctk.BooleanVar()
        ctk.CTkCheckBox(
            remember_frame,
            text="Remember me",
            variable=self.remember_var
        ).pack(anchor="w")

        # ================= FEEDBACK =================
        self.feedback_label = ctk.CTkLabel(
            card,
            text="",
            text_color="red",
            font=("Helvetica", 12)
        )
        self.feedback_label.pack(pady=(0, 5))

        # ================= LOGIN BUTTON =================
        ctk.CTkButton(
            card,
            text="Log In",
            height=40,
            corner_radius=20,
            fg_color=PRIMARY_BLUE,
            hover_color="#2563eb",
            command=self.login
        ).pack(pady=10, ipadx=10)

        # ================= EXTRA =================
        ctk.CTkLabel(
            card,
            text="Test credentials in database.db",
            text_color=TEXT_GRAY,
            font=("Helvetica", 11)
        ).pack(pady=(10, 5))

    # ================= LOGIN FUNCTION =================
    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            self.feedback_label.configure(
                text="Please enter email and password.",
                text_color="red"
            )
            return

        user = authenticate_user(email, password)

        if not user:
            self.feedback_label.configure(
                text="Invalid credentials.",
                text_color="red"
            )
            return

        role = (user.get("role") or "").strip().lower()

        self.controller.set_user({
            "email": user.get("email"),
            "role": role
        })

        self.feedback_label.configure(
            text="Login successful!",
            text_color="green"
        )

        if role == "applicant":
            self.controller.show_applicant_dashboard()
        elif role == "caseworker":
            self.controller.show_caseworker_dashboard()
        else:
            messagebox.showerror("Error", f"Unknown role: {user.get('role')}")