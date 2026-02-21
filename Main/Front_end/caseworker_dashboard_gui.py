# Front_end/caseworker_dashboard_gui.py
import customtkinter as ctk
from tkinter import messagebox

from Front_end.caseworker_view_popup import open_view_popup
from Back_end.application_logic import get_all_applications, approve_application, deny_application

HEADER_BLUE = "#5b9bd5"
BTN_GREEN = "#7dd169"

class CaseworkerDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        ctk.CTkLabel(
            self,
            text="Caseworker Dashboard",
            font=("Helvetica", 24, "bold"),
            fg_color=HEADER_BLUE,
            text_color="white",
            corner_radius=0
        ).pack(fill="x", ipady=15)

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(top, text="Refresh", fg_color=BTN_GREEN, command=self.refresh).pack(side="left")
        ctk.CTkButton(top, text="Logout", fg_color="gray", command=controller.logout).pack(side="right")

        self.table = ctk.CTkScrollableFrame(self, height=420)
        self.table.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh()

    def _summary_income(self, app: dict):
        # If your verification form stores income in the future, it can appear here.
        form = app.get("form", {}) if isinstance(app.get("form"), dict) else {}
        income = form.get("income", "")
        return str(income) if income is not None else ""

    def _employment_status(self, app: dict):
        form = app.get("form", {}) if isinstance(app.get("form"), dict) else {}
        return form.get("employment_status", "")

    def _applicant_name(self, app: dict):
        form = app.get("form", {}) if isinstance(app.get("form"), dict) else {}
        # Prefer the submitted applicant name, fallback to email if missing
        return form.get("applicant_name") or app.get("applicant_email", "")

    def refresh(self):
        for w in self.table.winfo_children():
            w.destroy()

        headers = ["Applicant", "Employment Status", "Income", "Status", "Actions"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(
                self.table,
                text=h,
                font=("Helvetica", 13, "bold")
            ).grid(row=0, column=i, padx=8, pady=8, sticky="w")

        apps = get_all_applications()

        # Empty state
        if not apps:
            ctk.CTkLabel(
                self.table,
                text="No applications submitted yet.",
                text_color="gray",
                font=("Helvetica", 13)
            ).grid(row=1, column=0, columnspan=5, padx=8, pady=20, sticky="w")
            return

        for r, app in enumerate(apps, start=1):
            applicant_text = self._applicant_name(app)
            status_text = app.get("status", "")

            ctk.CTkLabel(self.table, text=applicant_text).grid(row=r, column=0, padx=8, pady=8, sticky="w")
            ctk.CTkLabel(self.table, text=self._employment_status(app)).grid(row=r, column=1, padx=8, pady=8, sticky="w")
            ctk.CTkLabel(self.table, text=self._summary_income(app)).grid(row=r, column=2, padx=8, pady=8, sticky="w")
            ctk.CTkLabel(self.table, text=status_text).grid(row=r, column=3, padx=8, pady=8, sticky="w")

            actions = ctk.CTkFrame(self.table, fg_color="transparent")
            actions.grid(row=r, column=4, padx=8, pady=8, sticky="w")

            app_id = app.get("app_id", "")

            ctk.CTkButton(
                actions,
                text="View",
                width=70,
                command=lambda a=app: open_view_popup(self, a)
            ).pack(side="left", padx=4)

            ctk.CTkButton(
                actions,
                text="Approve",
                width=80,
                fg_color=BTN_GREEN,
                command=lambda aid=app_id: self.approve(aid)
            ).pack(side="left", padx=4)

            ctk.CTkButton(
                actions,
                text="Deny",
                width=70,
                fg_color="#d9534f",
                command=lambda aid=app_id: self.deny(aid)
            ).pack(side="left", padx=4)

    def approve(self, app_id):
        if not app_id:
            messagebox.showerror("Error", "Missing application ID.")
            return

        ok = approve_application(app_id)
        if ok:
            messagebox.showinfo("Approved", "Application approved.")
            self.refresh()
        else:
            messagebox.showerror("Error", "Approve failed.")

    def deny(self, app_id):
        if not app_id:
            messagebox.showerror("Error", "Missing application ID.")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Deny Application")
        popup.geometry("420x220")

        ctk.CTkLabel(popup, text="Reason for denial:", font=("Helvetica", 14, "bold")).pack(pady=15)
        reason_entry = ctk.CTkEntry(popup, width=320)
        reason_entry.pack(pady=10)

        def submit():
            reason = reason_entry.get().strip()
            if not reason:
                messagebox.showwarning("Missing", "Please enter a reason.")
                return

            ok = deny_application(app_id, reason)
            if ok:
                messagebox.showinfo("Denied", "Application denied.")
                popup.destroy()
                self.refresh()
            else:
                messagebox.showerror("Error", "Deny failed.")

        ctk.CTkButton(popup, text="Submit Denial", fg_color="#d9534f", command=submit).pack(pady=10)
        ctk.CTkButton(popup, text="Cancel", fg_color="gray", command=popup.destroy).pack(pady=5)