# Front_end/login_gui.py

import json
import os
import re
import customtkinter as ctk
from tkinter import messagebox

from Back_end.auth import authenticate_user

# Applicant theme
APPLICANT_BLUE = "#3b82f6"
APPLICANT_BLUE_HOVER = "#2563eb"

# Staff theme (caseworker + admin)
STAFF_ORANGE = "#f97316"
STAFF_ORANGE_HOVER = "#ea580c"

# Shared colors
CARD_BG = "#ffffff"
TEXT_GRAY = "#4b5563"
LIGHT_GRAY = "#e5e7eb"
LIGHT_GRAY_HOVER = "#d1d5db"
ERROR_RED = "#b91c1c"
SUCCESS_GREEN = "#15803d"

REMEMBER_ME_FILE = "remember_me.json"


class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # 🔥 important change
        self.selected_mode = "applicant"

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True)

        self.show_login_form("applicant")

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # ================= LOGIN FORM =================
    def show_login_form(self, mode):
        self.clear_container()
        self.selected_mode = mode

        if mode == "applicant":
            title = "Applicant Login"
            subtitle = "Log in to submit verification and check your application status."
            active_color = APPLICANT_BLUE
            hover_color = APPLICANT_BLUE_HOVER
            bottom_button_text = "Staff Access"
            bottom_button_command = lambda: self.show_login_form("staff")
        else:
            title = "Staff Login"
            subtitle = "Authorized staff can review applications or manage users."
            active_color = STAFF_ORANGE
            hover_color = STAFF_ORANGE_HOVER
            bottom_button_text = "Back to Applicant Login"
            bottom_button_command = lambda: self.show_login_form("applicant")

        self.active_color = active_color
        self.hover_color = hover_color

        card = ctk.CTkFrame(
            self.container,
            width=420,
            height=540,
            corner_radius=20,
            fg_color=CARD_BG
        )
        card.pack(pady=40)
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Helvetica", 24, "bold"),
            text_color="black"
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            card,
            text=subtitle,
            font=("Helvetica", 13),
            text_color=TEXT_GRAY,
            wraplength=320
        ).pack(pady=(0, 15))

        # ================= EMAIL =================
        self.email_entry = ctk.CTkEntry(
            card,
            width=260,
            height=40,
            placeholder_text="Email",
            border_color=active_color
        )
        self.email_entry.pack(pady=8)

        # ================= PASSWORD =================
        self.password_entry = ctk.CTkEntry(
            card,
            width=260,
            height=40,
            placeholder_text="Password",
            show="*",
            border_color=active_color
        )
        self.password_entry.pack(pady=8)

        # ================= REMEMBER =================
        self.remember_var = ctk.BooleanVar()
        ctk.CTkCheckBox(
            card,
            text="Remember email",
            variable=self.remember_var,
            fg_color=active_color
        ).pack(pady=5)

        # ================= FEEDBACK =================
        self.feedback_label = ctk.CTkLabel(
            card,
            text="",
            text_color=TEXT_GRAY
        )
        self.feedback_label.pack(pady=5)

        # ================= LOGIN =================
        ctk.CTkButton(
            card,
            text="Log In",
            fg_color=active_color,
            hover_color=hover_color,
            command=self.login
        ).pack(pady=10)

        # ================= SWITCH =================
        ctk.CTkButton(
            card,
            text=bottom_button_text,
            fg_color=LIGHT_GRAY,
            hover_color=LIGHT_GRAY_HOVER,
            text_color="black",
            command=bottom_button_command
        ).pack(pady=5)

        self.load_remembered_email()

    # ================= REMEMBER =================
    def load_remembered_email(self):
        if not os.path.exists(REMEMBER_ME_FILE):
            return

        try:
            with open(REMEMBER_ME_FILE, "r") as f:
                data = json.load(f)
                email = data.get("email", "")
                if email:
                    self.email_entry.insert(0, email)
                    self.remember_var.set(True)
        except:
            pass

    def save_remembered_email(self, email):
        with open(REMEMBER_ME_FILE, "w") as f:
            json.dump({"email": email}, f)

    # ================= LOGIN =================
    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            self.feedback_label.configure(
                text="Please enter both email and password.",
                text_color=ERROR_RED
            )
            return

        user = authenticate_user(email, password)

        if not user:
            self.feedback_label.configure(
                text="Invalid email or password.",
                text_color=ERROR_RED
            )
            return

        # 🔒 Locked user check
        if user.get("status") == "locked":
            self.feedback_label.configure(
                text="This account has been locked. Please contact an administrator.",
                text_color=ERROR_RED
            )
            return

        role = user.get("role")

        # 🔥 MODE CHECK (IMPORTANT)
        if self.selected_mode == "applicant":
            if role != "applicant":
                self.feedback_label.configure(
                    text="This account is not an applicant account.",
                    text_color=ERROR_RED
                )
                return

        elif self.selected_mode == "staff":
            if role not in ["caseworker", "admin"]:
                self.feedback_label.configure(
                    text="This account is not authorized for staff access.",
                    text_color=ERROR_RED
                )
                return

        # Remember email
        if self.remember_var.get():
            self.save_remembered_email(email)

        self.controller.set_user(user)

        # 🔥 ROUTING
        if role == "applicant":
            self.controller.show_applicant_dashboard()

        elif role == "caseworker":
            self.controller.show_caseworker_dashboard()

        elif role == "admin":
            self.controller.show_admin_user_management()