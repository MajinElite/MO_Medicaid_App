# Front_end/caseworker_dashboard_gui.py

import customtkinter as ctk
from tkinter import messagebox

from Front_end.caseworker_view_popup import open_view_popup
from Back_end.application_logic import get_all_applications, approve_application, deny_application

# ================= CASEWORKER THEME =================
HEADER_ORANGE = "#f97316"
HEADER_ORANGE_HOVER = "#ea580c"
SECTION_ORANGE = "#f97316"

BTN_GREEN = "#7dd169"
BTN_BLUE = "#17a2b8"
BTN_RED = "#d9534f"

CARD_BG = "#2b2b2b"
BODY_BG = "#343638"
TEXT_MUTED = "#b0b0b0"

STATUS_COLORS = {
    "Pending": "#f0ad4e",
    "Under Review": "#f0ad4e",
    "Needs Review": "#f0ad4e",
    "Exemption Pending": "#9b59b6",
    "More Info Required": "#17a2b8",
    "Request Info": "#17a2b8",
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

        ctk.CTkLabel(
            self,
            text="Caseworker Dashboard",
            font=("Helvetica", 24, "bold"),
            fg_color=HEADER_ORANGE,
            text_color="white",
            corner_radius=0
        ).pack(fill="x", ipady=15)

        context = ctk.CTkFrame(self, corner_radius=10, fg_color=CARD_BG)
        context.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            context,
            text=(
                "Review submitted applications, request missing information, "
                "and update applicant decisions. Status labels include text and color for clarity."
            ),
            font=("Helvetica", 13),
            text_color="white",
            wraplength=1000,
            justify="center"
        ).pack(pady=12)

        summary = ctk.CTkFrame(self, fg_color="transparent")
        summary.pack(fill="x", padx=20, pady=(10, 5))

        self.card_total = self._summary_card(summary, "Total Applications", "#6c757d")
        self.card_pending = self._summary_card(summary, "Pending Review", "#f0ad4e")
        self.card_approved = self._summary_card(summary, "Approved", "#3cb371")
        self.card_denied = self._summary_card(summary, "Denied", "#dc3545")

        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", padx=20, pady=10)

        left = ctk.CTkFrame(controls, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left,
            text="Filter Applications:",
            font=("Helvetica", 13, "bold"),
            text_color="white"
        ).pack(side="left", padx=(0, 6))

        ctk.CTkOptionMenu(
            left,
            values=["All", "Pending", "Approved", "Denied", "More Info Required", "Exemption Requests"],
            variable=self.filter_var,
            fg_color=HEADER_ORANGE,
            button_color=SECTION_ORANGE,
            button_hover_color=HEADER_ORANGE_HOVER,
            command=lambda _: self.refresh()
        ).pack(side="left")

        ctk.CTkButton(
            controls,
            text="Refresh Dashboard",
            fg_color=HEADER_ORANGE,
            hover_color=HEADER_ORANGE_HOVER,
            command=self.refresh
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            controls,
            text="Logout",
            fg_color="gray",
            hover_color="#666666",
            command=self.controller.logout
        ).pack(side="right")

        table_card = ctk.CTkFrame(self, corner_radius=10, fg_color=CARD_BG)
        table_card.pack(fill="both", expand=True, padx=20, pady=(5, 15))

        header_strip = ctk.CTkFrame(table_card, fg_color=SECTION_ORANGE)
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

    def _get_form(self, app):
        return app.get("form", {}) if isinstance(app.get("form"), dict) else {}

    def _status_label_text(self, status_text):
        if status_text in ["Pending", "Under Review", "Needs Review"]:
            return "Pending Review"
        if status_text in ["More Info Required", "Request Info"]:
            return "More Info Required"
        if status_text == "Exemption Pending":
            return "Exemption Pending"
        if status_text == "Approved":
            return "Approved"
        if status_text == "Denied":
            return "Denied"
        if not status_text:
            return "Unknown"
        return status_text

    def _status_badge(self, parent, status_text):
        display_text = self._status_label_text(status_text)
        color = STATUS_COLORS.get(status_text, "#6c757d")

        badge = ctk.CTkFrame(parent, fg_color=color, corner_radius=10)

        ctk.CTkLabel(
            badge,
            text=display_text,
            text_color="white",
            font=("Helvetica", 12, "bold")
        ).pack(padx=10, pady=4)

        return badge

    def safe_view_popup(self, app):
        try:
            open_view_popup(self, app)
        except Exception as e:
            messagebox.showerror(
                "Unable to Open Details",
                f"The application details could not be opened.\n\nDetails: {e}"
            )

    def refresh(self):
        for w in self.table.winfo_children():
            w.destroy()

        apps = get_all_applications()
        apps = apps if isinstance(apps, list) else []

        total = len(apps)
        pending = sum(1 for a in apps if a.get("status") in ["Pending", "Under Review", "Needs Review"])
        approved = sum(1 for a in apps if a.get("status") == "Approved")
        denied = sum(1 for a in apps if a.get("status") == "Denied")

        self.card_total.configure(text=str(total))
        self.card_pending.configure(text=str(pending))
        self.card_approved.configure(text=str(approved))
        self.card_denied.configure(text=str(denied))

        selected = self.filter_var.get()

        if selected == "Exemption Requests":
            apps = [a for a in apps if a.get("form", {}).get("exemption_requested") == "Yes"]
        elif selected == "More Info Required":
            apps = [a for a in apps if a.get("status") in ["More Info Required", "Request Info"]]
        elif selected == "Pending":
            apps = [a for a in apps if a.get("status") in ["Pending", "Under Review", "Needs Review"]]
        elif selected != "All":
            apps = [a for a in apps if a.get("status") == selected]

        column_weights = {
            0: 2,  # Applicant
            1: 2,  # Employment
            2: 1,  # Hours
            3: 2,  # Start Date
            4: 2,  # Income
            5: 2,  # Docs
            6: 2,  # Status
            7: 2,  # Actions
        }

        for col, weight in column_weights.items():
            self.table.grid_columnconfigure(col, weight=weight)

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
                text="No applications found for the selected filter.",
                text_color=TEXT_MUTED,
                font=("Helvetica", 14)
            ).grid(row=1, column=0, columnspan=8, pady=35)
            return

        for r, app in enumerate(apps, start=1):
            form = self._get_form(app)

            status_text = app.get("status", "")
            app_id = app.get("app_id", "")

            applicant_name = form.get("applicant_name", "Not Provided")
            employment_status = form.get("employment_status", "Not Provided")
            hours = form.get("hours_per_week", "Not Provided")
            start_date = form.get("start_date", "Not Provided")
            income = form.get("monthly_income", "Not Provided")

            ctk.CTkLabel(self.table, text=applicant_name, text_color="white").grid(row=r, column=0, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(self.table, text=employment_status, text_color="white").grid(row=r, column=1, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(self.table, text=str(hours), text_color="white").grid(row=r, column=2, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(self.table, text=str(start_date), text_color="white").grid(row=r, column=3, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(self.table, text=str(income), text_color="white").grid(row=r, column=4, padx=10, pady=10, sticky="w")

            has_doc = bool(form.get("document_data_base64"))
            docs_color = "#3cb371" if has_doc else "#6c757d"
            docs_text = "Document Uploaded" if has_doc else "No Document"

            docs_badge = ctk.CTkFrame(self.table, fg_color=docs_color, corner_radius=10)
            docs_badge.grid(row=r, column=5, padx=10, pady=10, sticky="w")

            ctk.CTkLabel(
                docs_badge,
                text=docs_text,
                text_color="white",
                font=("Helvetica", 12, "bold")
            ).pack(padx=10, pady=4)

            badge = self._status_badge(self.table, status_text)
            badge.grid(row=r, column=6, padx=10, pady=10, sticky="w")

            actions = ctk.CTkFrame(self.table, fg_color="transparent")
            actions.grid(row=r, column=7, padx=10, pady=10, sticky="e")

            ctk.CTkButton(
                actions,
                text="View",
                width=120,
                fg_color=HEADER_ORANGE,
                hover_color=HEADER_ORANGE_HOVER,
                command=lambda a=app: self.safe_view_popup(a)
            ).pack(pady=2)

            ctk.CTkButton(
                actions,
                text="Approve",
                width=120,
                fg_color=BTN_GREEN,
                command=lambda aid=app_id: self.approve(aid)
            ).pack(pady=2)

            ctk.CTkButton(
                actions,
                text="Request Info",
                width=120,
                fg_color=BTN_BLUE,
                command=lambda aid=app_id: self.request_info_popup(aid)
            ).pack(pady=2)

            ctk.CTkButton(
                actions,
                text="Deny",
                width=120,
                fg_color=BTN_RED,
                command=lambda aid=app_id: self.deny(aid)
            ).pack(pady=2)

    def request_info_popup(self, app_id):
        if not app_id:
            messagebox.showerror(
                "Missing Application ID",
                "The system could not find the selected application ID."
            )
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Request More Information")
        popup.geometry("540x340")
        popup.configure(fg_color=BODY_BG)
        popup.grab_set()

        ctk.CTkLabel(
            popup,
            text="Request More Information",
            font=("Helvetica", 18, "bold"),
            text_color="white"
        ).pack(pady=(18, 5))

        ctk.CTkLabel(
            popup,
            text="Explain exactly what the applicant needs to provide.",
            text_color=TEXT_MUTED,
            wraplength=460
        ).pack(pady=(0, 10))

        reason_box = ctk.CTkTextbox(popup, height=130, width=460)
        reason_box.pack(pady=10)

        def submit():
            reason = reason_box.get("1.0", "end").strip()

            if not reason:
                messagebox.showwarning(
                    "Missing Request Details",
                    "Please explain what information is required before sending the request."
                )
                return

            confirm = messagebox.askyesno(
                "Confirm Request",
                "Send this information request to the applicant?"
            )

            if not confirm:
                return

            try:
                from Back_end.application_logic import request_more_info
                ok = request_more_info(app_id, reason)
            except ImportError:
                ok = True

            if ok:
                messagebox.showinfo(
                    "Request Sent",
                    "The information request was sent to the applicant successfully."
                )
                popup.destroy()
                self.refresh()
            else:
                messagebox.showerror(
                    "Request Failed",
                    "The information request could not be sent. Please try again."
                )

        btns = ctk.CTkFrame(popup, fg_color="transparent")
        btns.pack(pady=10)

        ctk.CTkButton(
            btns,
            text="Send Request",
            fg_color=BTN_BLUE,
            command=submit
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btns,
            text="Cancel",
            fg_color="gray",
            command=popup.destroy
        ).pack(side="left", padx=8)

    def approve(self, app_id):
        if not app_id:
            messagebox.showerror(
                "Missing Application ID",
                "The system could not find the selected application ID."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Approval",
            "Are you sure you want to approve this application?"
        )

        if not confirm:
            return

        ok = approve_application(app_id)

        if ok:
            messagebox.showinfo(
                "Application Approved",
                "The application was approved successfully."
            )
            self.refresh()
        else:
            messagebox.showerror(
                "Approval Failed",
                "The application could not be approved. Please try again."
            )

    def deny(self, app_id):
        if not app_id:
            messagebox.showerror(
                "Missing Application ID",
                "The system could not find the selected application ID."
            )
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Deny Application")
        popup.geometry("540x340")
        popup.configure(fg_color=BODY_BG)
        popup.grab_set()

        ctk.CTkLabel(
            popup,
            text="Deny Application",
            font=("Helvetica", 18, "bold"),
            text_color="white"
        ).pack(pady=(18, 5))

        ctk.CTkLabel(
            popup,
            text="Enter a clear reason. This message will be visible to the applicant.",
            text_color=TEXT_MUTED,
            wraplength=460
        ).pack(pady=(0, 10))

        reason_box = ctk.CTkTextbox(popup, height=130, width=460)
        reason_box.pack(pady=10)

        def submit():
            reason = reason_box.get("1.0", "end").strip()

            if not reason:
                messagebox.showwarning(
                    "Missing Denial Reason",
                    "Please enter a reason so the applicant understands the decision."
                )
                return

            confirm = messagebox.askyesno(
                "Confirm Denial",
                "Are you sure you want to deny this application?"
            )

            if not confirm:
                return

            ok2 = deny_application(app_id, reason)

            if ok2:
                messagebox.showinfo(
                    "Application Denied",
                    "The application was denied successfully."
                )
                popup.destroy()
                self.refresh()
            else:
                messagebox.showerror(
                    "Denial Failed",
                    "The application could not be denied. Please try again."
                )

        btns = ctk.CTkFrame(popup, fg_color="transparent")
        btns.pack(pady=10)

        ctk.CTkButton(
            btns,
            text="Submit Denial",
            fg_color=BTN_RED,
            command=submit
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btns,
            text="Cancel",
            fg_color="gray",
            command=popup.destroy
        ).pack(side="left", padx=8)