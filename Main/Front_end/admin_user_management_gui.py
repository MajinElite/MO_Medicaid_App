import customtkinter as ctk
from tkinter import messagebox

from Back_end.storage import (
    get_all_managed_users,
    create_user,
    update_user,
    delete_user,
    lock_user,
    unlock_user,
)

HEADER_ORANGE = "#f97316"
HEADER_ORANGE_HOVER = "#ea580c"
SECTION_ORANGE = "#c2410c"

CARD_BG = "#2b2b2b"
BODY_BG = "#343638"
TEXT_MUTED = "#b0b0b0"

BTN_GREEN = "#7dd169"
BTN_RED = "#d9534f"
BTN_BLUE = "#17a2b8"


class AdminUserManagementScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.filter_var = ctk.StringVar(value="All")

        # ================= CENTER WRAPPER =================
        wrapper = ctk.CTkFrame(self, fg_color="transparent")
        wrapper.pack(expand=True)

        main_card = ctk.CTkFrame(
            wrapper,
            fg_color=CARD_BG,
            corner_radius=18,
            width=950,
            height=620
        )
        main_card.pack(pady=20)
        main_card.pack_propagate(False)

        # ================= HEADER =================
        ctk.CTkLabel(
            main_card,
            text="Admin User Management",
            font=("Helvetica", 24, "bold"),
            fg_color=HEADER_ORANGE,
            text_color="white",
        ).pack(fill="x", ipady=14)

        # ================= TOP CONTROLS =================
        controls = ctk.CTkFrame(main_card, fg_color="transparent")
        controls.pack(fill="x", padx=25, pady=18)

        ctk.CTkLabel(
            controls,
            text="Manage applicant and caseworker accounts.",
            font=("Helvetica", 14),
            text_color="white",
        ).pack(side="left")

        ctk.CTkButton(
            controls,
            text="Add User",
            width=120,
            fg_color=HEADER_ORANGE,
            hover_color=HEADER_ORANGE_HOVER,
            command=self.open_add_user_popup,
        ).pack(side="right", padx=(10, 0))

        ctk.CTkButton(
            controls,
            text="Logout",
            width=120,
            fg_color="gray",
            hover_color="#666666",
            command=self.controller.logout,
        ).pack(side="right")

        # ================= FILTER =================
        filter_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        filter_frame.pack(fill="x", padx=25, pady=(0, 12))

        ctk.CTkLabel(
            filter_frame,
            text="Filter:",
            text_color="white",
            font=("Helvetica", 13, "bold"),
        ).pack(side="left", padx=(0, 8))

        ctk.CTkOptionMenu(
            filter_frame,
            values=["All", "Applicant", "Caseworker", "Active", "Locked"],
            variable=self.filter_var,
            fg_color=HEADER_ORANGE,
            button_color=SECTION_ORANGE,
            button_hover_color=HEADER_ORANGE_HOVER,
            command=lambda _: self.refresh(),
        ).pack(side="left")

        # ================= TABLE =================
        table_card = ctk.CTkFrame(main_card, fg_color=BODY_BG, corner_radius=12)
        table_card.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        self.table = ctk.CTkScrollableFrame(table_card, fg_color=BODY_BG)
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh()

    def refresh(self):
        for widget in self.table.winfo_children():
            widget.destroy()

        users = get_all_managed_users()
        selected = self.filter_var.get().lower()

        if selected != "all":
            if selected in ["applicant", "caseworker"]:
                users = [u for u in users if (u.get("role") or "").lower() == selected]
            elif selected in ["active", "locked"]:
                users = [u for u in users if (u.get("status") or "").lower() == selected]

        headers = ["Email", "Role", "Status", "Actions"]

        column_weights = {
            0: 3,
            1: 2,
            2: 2,
            3: 3,
        }

        for col, weight in column_weights.items():
            self.table.grid_columnconfigure(col, weight=weight)

        for i, header in enumerate(headers):
            ctk.CTkLabel(
                self.table,
                text=header,
                text_color="white",
                font=("Helvetica", 13, "bold"),
            ).grid(row=0, column=i, padx=10, pady=10, sticky="w")

        if not users:
            ctk.CTkLabel(
                self.table,
                text="No users found for the selected filter.",
                text_color=TEXT_MUTED,
                font=("Helvetica", 14),
            ).grid(row=1, column=0, columnspan=4, pady=35)
            return

        for row, user in enumerate(users, start=1):
            email = user.get("email", "")
            role = (user.get("role", "") or "").title()
            status = (user.get("status", "") or "active").title()
            user_id = user.get("id")

            ctk.CTkLabel(
                self.table,
                text=email,
                text_color="white",
            ).grid(row=row, column=0, padx=10, pady=12, sticky="w")

            ctk.CTkLabel(
                self.table,
                text=role,
                text_color="white",
            ).grid(row=row, column=1, padx=10, pady=12, sticky="w")

            status_color = BTN_GREEN if status.lower() == "active" else BTN_RED

            status_badge = ctk.CTkFrame(
                self.table,
                fg_color=status_color,
                corner_radius=10
            )
            status_badge.grid(row=row, column=2, padx=10, pady=12, sticky="w")

            ctk.CTkLabel(
                status_badge,
                text=status,
                text_color="white",
                font=("Helvetica", 12, "bold"),
            ).pack(padx=12, pady=5)

            actions = ctk.CTkFrame(self.table, fg_color="transparent")
            actions.grid(row=row, column=3, padx=10, pady=12, sticky="w")

            ctk.CTkButton(
                actions,
                text="Edit",
                width=80,
                fg_color=HEADER_ORANGE,
                hover_color=HEADER_ORANGE_HOVER,
                command=lambda u=user: self.open_edit_user_popup(u),
            ).pack(side="left", padx=4)

            if status.lower() == "active":
                ctk.CTkButton(
                    actions,
                    text="Lock",
                    width=80,
                    fg_color=BTN_BLUE,
                    command=lambda uid=user_id: self.lock_selected_user(uid),
                ).pack(side="left", padx=4)
            else:
                ctk.CTkButton(
                    actions,
                    text="Unlock",
                    width=80,
                    fg_color=BTN_GREEN,
                    command=lambda uid=user_id: self.unlock_selected_user(uid),
                ).pack(side="left", padx=4)

            ctk.CTkButton(
                actions,
                text="Delete",
                width=80,
                fg_color=BTN_RED,
                command=lambda uid=user_id: self.delete_selected_user(uid),
            ).pack(side="left", padx=4)

    def open_add_user_popup(self):
        self.user_popup(title="Add User", mode="add")

    def open_edit_user_popup(self, user):
        self.user_popup(title="Edit User", mode="edit", user=user)

    def user_popup(self, title, mode, user=None):
        popup = ctk.CTkToplevel(self)
        popup.title(title)
        popup.geometry("460x420")
        popup.configure(fg_color=BODY_BG)
        popup.grab_set()

        ctk.CTkLabel(
            popup,
            text=title,
            font=("Helvetica", 20, "bold"),
            text_color="white",
        ).pack(pady=(20, 10))

        ctk.CTkLabel(popup, text="Email *", text_color="white").pack(anchor="w", padx=50)
        email_entry = ctk.CTkEntry(popup, width=340)
        email_entry.pack(pady=(5, 12))

        ctk.CTkLabel(popup, text="Password *", text_color="white").pack(anchor="w", padx=50)
        password_entry = ctk.CTkEntry(popup, width=340, show="*")
        password_entry.pack(pady=(5, 12))

        ctk.CTkLabel(
            popup,
            text="Leave password blank when editing if you do not want to change it.",
            text_color=TEXT_MUTED,
            font=("Helvetica", 11),
            wraplength=340,
        ).pack(pady=(0, 10))

        ctk.CTkLabel(popup, text="Role *", text_color="white").pack(anchor="w", padx=50)

        role_menu = ctk.CTkOptionMenu(
            popup,
            values=["applicant", "caseworker"],
            fg_color=HEADER_ORANGE,
            button_color=SECTION_ORANGE,
            button_hover_color=HEADER_ORANGE_HOVER,
        )
        role_menu.pack(pady=(5, 15))

        if user:
            email_entry.insert(0, user.get("email", ""))
            role_menu.set((user.get("role") or "applicant").lower())
        else:
            role_menu.set("applicant")

        def submit():
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            role = role_menu.get().strip().lower()

            if not email:
                messagebox.showwarning("Missing Email", "Please enter an email address.")
                return

            if mode == "add" and not password:
                messagebox.showwarning("Missing Password", "Please enter a password for the new user.")
                return

            if mode == "add":
                ok, msg = create_user(email, password, role)
            else:
                ok, msg = update_user(user.get("id"), email, password, role)

            if ok:
                messagebox.showinfo("Success", msg)
                popup.destroy()
                self.refresh()
            else:
                messagebox.showerror("Error", msg)

        btns = ctk.CTkFrame(popup, fg_color="transparent")
        btns.pack(pady=10)

        ctk.CTkButton(
            btns,
            text="Save",
            fg_color=HEADER_ORANGE,
            hover_color=HEADER_ORANGE_HOVER,
            command=submit,
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btns,
            text="Cancel",
            fg_color="gray",
            command=popup.destroy,
        ).pack(side="left", padx=8)

    def lock_selected_user(self, user_id):
        confirm = messagebox.askyesno(
            "Confirm Lock",
            "Are you sure you want to lock this account?"
        )

        if not confirm:
            return

        ok, msg = lock_user(user_id)

        if ok:
            messagebox.showinfo("Account Locked", msg)
            self.refresh()
        else:
            messagebox.showerror("Error", msg)

    def unlock_selected_user(self, user_id):
        ok, msg = unlock_user(user_id)

        if ok:
            messagebox.showinfo("Account Unlocked", msg)
            self.refresh()
        else:
            messagebox.showerror("Error", msg)

    def delete_selected_user(self, user_id):
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this user account?"
        )

        if not confirm:
            return

        ok, msg = delete_user(user_id)

        if ok:
            messagebox.showinfo("User Deleted", msg)
            self.refresh()
        else:
            messagebox.showerror("Error", msg)