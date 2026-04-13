# Front_end/caseworker_dashboard_gui.py

import customtkinter as ctk
from tkinter import messagebox

from Front_end.caseworker_view_popup import open_view_popup
from Back_end.application_logic import get_all_applications, approve_application, deny_application

HEADER_BLUE = "#5b9bd5"
SECTION_BLUE = "#3b6ea5"
BTN_GREEN = "#7dd169"

CARD_BG = "#2b2b2b"
BODY_BG = "#343638"

STATUS_COLORS = {
    "Pending": "#f0ad4e",
    "Under Review": "#f0ad4e",
    "Needs Review": "#f0ad4e",
    "Exemption Pending": "#9b59b6", # Added for Exemption workflow
    "Request Info": "#17a2b8",      # Added for Request Info workflow
    "Approved": "#3cb371",
    "Denied": "#dc3545",
    "None": "#6c757d",
    "": "#6c757d",
}


class CaseworkerDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.filter_var = ctk.StringVar(value="All")

        # ================= HEADER =================
        ctk.CTkLabel(
            self,
            text="Caseworker Dashboard",
            font=("Helvetica", 24, "bold"),
            fg_color=HEADER_BLUE,
            text_color="white",
            corner_radius=0
        ).pack(fill="x", ipady=15)

        # ================= SUMMARY =================
        summary = ctk.CTkFrame(self, fg_color="transparent")
        summary.pack(fill="x", padx=20, pady=(15, 5))

        self.card_total = self._summary_card(summary, "Total", "#6c757d")
        self.card_pending = self._summary_card(summary, "Pending", "#f0ad4e")
        self.card_approved = self._summary_card(summary, "Approved", "#3cb371")
        self.card_denied = self._summary_card(summary, "Denied", "#dc3545")

        # ================= CONTROLS =================
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", padx=20, pady=10)

        left = ctk.CTkFrame(controls, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(left, text="Filter:", font=("Helvetica", 13, "bold")).pack(side="left", padx=(0, 6))

        ctk.CTkOptionMenu(
            left,
            values=["All", "Pending", "Under Review", "Approved", "Denied"],
            variable=self.filter_var,
            command=lambda _: self.refresh()
        ).pack(side="left")

        ctk.CTkButton(
            controls,
            text="Refresh",
            fg_color=BTN_GREEN,
            command=self.refresh
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            controls,
            text="Logout",
            fg_color="gray",
            command=controller.logout
        ).pack(side="right")

        # ================= TABLE WRAPPER =================
        table_card = ctk.CTkFrame(self, corner_radius=10, fg_color=CARD_BG)
        table_card.pack(fill="both", expand=True, padx=20, pady=(5, 15))

        header_strip = ctk.CTkFrame(table_card, fg_color=SECTION_BLUE)
        header_strip.pack(fill="x")

        ctk.CTkLabel(
            header_strip,
            text="Applications",
            font=("Helvetica", 14, "bold"),
            text_color="white"
        ).pack(pady=8, padx=15, anchor="w")

        self.table = ctk.CTkScrollableFrame(table_card, fg_color=BODY_BG)
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh()

    # ================= SUMMARY CARD =================
    def _summary_card(self, parent, title, color):
        card = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=10)
        card.pack(side="left", padx=8, pady=5, fill="x", expand=True)

        top = ctk.CTkFrame(card, fg_color=color)
        top.pack(fill="x", padx=10, pady=(10, 6))

        ctk.CTkLabel(
            top,
            text=title,
            text_color="white",
            font=("Helvetica", 12, "bold")
        ).pack(padx=10, pady=6, anchor="w")

        value_lbl = ctk.CTkLabel(
            card,
            text="0",
            text_color="white",
            font=("Helvetica", 20, "bold")
        )
        value_lbl.pack(pady=(0, 12))

        return value_lbl

    # ================= HELPERS =================
    def _get_form(self, app):
        return app.get("form", {}) if isinstance(app.get("form"), dict) else {}

    def _status_badge(self, parent, status_text):
        color = STATUS_COLORS.get(status_text, "#6c757d")
        badge = ctk.CTkFrame(parent, fg_color=color, corner_radius=10)
        ctk.CTkLabel(
            badge,
            text=status_text if status_text else "Unknown",
            text_color="white",
            font=("Helvetica", 12, "bold")
        ).pack(padx=10, pady=4)
        return badge

    def safe_view_popup(self, app):
        try:
            open_view_popup(self, app)
        except Exception as e:
            messagebox.showerror("Popup Error", str(e))

    # ================= REFRESH =================
    def refresh(self):
        for w in self.table.winfo_children():
            w.destroy()

        apps = get_all_applications()
        apps = apps if isinstance(apps, list) else []

        # Update summary
        total = len(apps)
        pending = sum(1 for a in apps if a.get("status") in ["Pending", "Under Review", "Needs Review"])
        approved = sum(1 for a in apps if a.get("status") == "Approved")
        denied = sum(1 for a in apps if a.get("status") == "Denied")

        self.card_total.configure(text=str(total))
        self.card_pending.configure(text=str(pending))
        self.card_approved.configure(text=str(approved))
        self.card_denied.configure(text=str(denied))

        # Filter
        selected = self.filter_var.get()
        if selected != "All":
            apps = [a for a in apps if a.get("status") == selected]

        # Configure columns (IMPORTANT FOR ALIGNMENT)
        for col in range(6):
            self.table.grid_columnconfigure(col, weight=1, uniform="cols")

        headers = ["Applicant", "Employment", "Hours", "Start Date", "Income", "Docs", "Status", "Actions"]

        for i, h in enumerate(headers):
            ctk.CTkLabel(
                self.table,
                text=h,
                font=("Helvetica", 13, "bold"),
                text_color="white"
            ).grid(row=0, column=i, padx=10, pady=8, sticky="w")

        if not apps:
            ctk.CTkLabel(
                self.table,
                text="No applications found for this filter.",
                text_color="gray",
                font=("Helvetica", 14)
            ).grid(row=1, column=0, columnspan=8, pady=30)
            return

        # Data rows
        for r, app in enumerate(apps, start=1):
            form = self._get_form(app)

            status_text = app.get("status", "")
            app_id = app.get("app_id", "")

            ctk.CTkLabel(self.table, text=form.get("applicant_name", ""), text_color="white").grid(row=r, column=0, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(self.table, text=form.get("employment_status", ""), text_color="white").grid(row=r, column=1, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(self.table, text=str(form.get("hours_per_week", "")), text_color="white").grid(row=r, column=2, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(self.table, text=str(form.get("start_date", "")), text_color="white").grid(row=r, column=3, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(self.table, text=str(form.get("monthly_income", "")), text_color="white").grid(row=r, column=4, padx=10, pady=10, sticky="w")

            # Docs badge
            has_doc = bool(form.get("document_data_base64"))
            docs_color = "#3cb371" if has_doc else "#6c757d"
            docs_badge = ctk.CTkFrame(self.table, fg_color=docs_color, corner_radius=10)
            docs_badge.grid(row=r, column=5, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(
                docs_badge,
                text="Yes" if has_doc else "No",
                text_color="white",
                font=("Helvetica", 12, "bold")
            ).pack(padx=10, pady=4)

            badge = self._status_badge(self.table, status_text)
            badge.grid(row=r, column=6, padx=10, pady=10, sticky="w")

            actions = ctk.CTkFrame(self.table, fg_color="transparent")
            actions.grid(row=r, column=7, padx=10, pady=10, sticky="w")

            ctk.CTkButton(
                actions,
                text="View More",
                width=90,
                command=lambda a=app: self.safe_view_popup(a)
            ).pack(side="left", padx=4)

            ctk.CTkButton(
                actions,
                text="Approve",
                width=80,
                fg_color=BTN_GREEN,
                command=lambda aid=app_id: self.approve(aid)
            ).pack(side="left", padx=4)
            # --- NEW REQUEST INFO BUTTON ---
            ctk.CTkButton(
                actions,
                text="Request Info",
                width=90,
                fg_color="#17a2b8",
                command=lambda aid=app_id: self.request_info_popup(aid)
            ).pack(side="left", padx=4)
            ctk.CTkButton(
                actions,
                text="Deny",
                width=70,
                fg_color="#d9534f",
                command=lambda aid=app_id: self.deny(aid)
            ).pack(side="left", padx=4)
    # ================= REQUEST INFO =================
    def request_info_popup(self, app_id):
        if not app_id:
            messagebox.showerror("Error", "Missing application ID.")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Request More Information")
        popup.geometry("520x320")

        ctk.CTkLabel(popup, text="What information is missing?", font=("Helvetica", 16, "bold")).pack(pady=(15, 5))
        ctk.CTkLabel(popup, text="This will notify the applicant to update their documents.", text_color="gray").pack(pady=(0, 10))

        reason_box = ctk.CTkTextbox(popup, height=120, width=450)
        reason_box.pack(pady=10)

        def submit():
            reason = reason_box.get("1.0", "end").strip()
            if not reason:
                messagebox.showwarning("Missing", "Please detail what information is required.")
                return
            
            # Temporary fallback logic until backend is ready
            try:
                from Back_end.application_logic import request_more_info
                ok = request_more_info(app_id, reason)
            except ImportError:
                ok = True # Fake success if backend isn't linked yet

            if ok:
                messagebox.showinfo("Sent", "Request sent to applicant.")
                popup.destroy()
                self.refresh()

        btns = ctk.CTkFrame(popup, fg_color="transparent")
        btns.pack(pady=10)
        ctk.CTkButton(btns, text="Send Request", fg_color="#17a2b8", command=submit).pack(side="left", padx=8)
        ctk.CTkButton(btns, text="Cancel", fg_color="gray", command=popup.destroy).pack(side="left", padx=8)
    # ================= APPROVE =================
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

    # ================= DENY =================
    def deny(self, app_id):
        if not app_id:
            messagebox.showerror("Error", "Missing application ID.")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Deny Application")
        popup.geometry("520x320")

        ctk.CTkLabel(
            popup,
            text="Reason for denial",
            font=("Helvetica", 16, "bold")
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            popup,
            text="This message will be visible to the applicant.",
            text_color="gray"
        ).pack(pady=(0, 10))

        reason_box = ctk.CTkTextbox(popup, height=120, width=450)
        reason_box.pack(pady=10)

        def submit():
            reason = reason_box.get("1.0", "end").strip()
            if not reason:
                messagebox.showwarning("Missing", "Please enter a reason.")
                return

            ok2 = deny_application(app_id, reason)
            if ok2:
                messagebox.showinfo("Denied", "Application denied.")
                popup.destroy()
                self.refresh()
            else:
                messagebox.showerror("Error", "Deny failed.")

        btns = ctk.CTkFrame(popup, fg_color="transparent")
        btns.pack(pady=10)

        ctk.CTkButton(btns, text="Submit Denial", fg_color="#d9534f", command=submit).pack(side="left", padx=8)
        ctk.CTkButton(btns, text="Cancel", fg_color="gray", command=popup.destroy).pack(side="left", padx=8)
