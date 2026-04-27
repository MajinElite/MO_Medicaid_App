# Front_end/verification_gui.py

import base64
import os
import re
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox

HEADER_BLUE = "#5b9bd5"
SECTION_BLUE = "#3b6ea5"
CARD_BG = "#2b2b2b"
BODY_BG = "#343638"
BTN_GREEN = "#7dd169"
ERROR_RED = "#dc3545"

try:
    from Back_end.application_logic import submit_employment_verification
except Exception:
    def submit_employment_verification(user, payload):
        return True


class VerificationScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.entries = {}

        self.file_original_name = ""
        self.file_base64 = ""

        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(
            self.scroll_frame,
            text="Employment Verification Form",
            font=("Helvetica", 24, "bold"),
            fg_color=HEADER_BLUE,
            text_color="white",
            corner_radius=0
        ).pack(fill="x", ipady=15)

        context = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
        context.pack(pady=20, padx=60, fill="x")

        ctk.CTkLabel(
            context,
            text=(
                "This form verifies employment details for Medicaid eligibility review.\n"
                "Please ensure all required fields marked with * are accurate before submission."
            ),
            font=("Helvetica", 13),
            justify="center"
        ).pack(pady=15)

        self.create_section("Applicant Information")
        self.add_entry("Applicant Name", "applicant_name", required=True)

        self.create_section("Employment Information")
        self.add_entry("Employer Name", "employer_name", required=True)
        self.add_entry("Employee ID", "employee_id", required=True)

        ctk.CTkLabel(
            self.section_body,
            text="Employment Status:",
            text_color="white"
        ).pack(anchor="w", padx=20, pady=(10, 5))

        self.status_var = tk.StringVar(value="Full-Time")
        status_frame = ctk.CTkFrame(self.section_body, fg_color="transparent")
        status_frame.pack(anchor="w", padx=20)

        for value in ["Full-Time", "Part-Time", "Self-Employed"]:
            ctk.CTkRadioButton(
                status_frame,
                text=value,
                variable=self.status_var,
                value=value
            ).pack(side="left", padx=10)

        self.add_entry("Start Date (MM/DD/YYYY)", "start_date", required=True)
        self.add_entry("Hours Per Week", "hours_per_week", required=True)
        self.add_entry("Monthly Gross Income ($)", "monthly_income", required=False)

        self.create_section("Supporting Documents")

        doc_frame = ctk.CTkFrame(self.section_body, fg_color="transparent")
        doc_frame.pack(fill="x", padx=20, pady=10)

        self.doc_entry = ctk.CTkEntry(doc_frame, width=250, placeholder_text="No file selected")
        self.doc_entry.pack(side="left")

        ctk.CTkButton(
            doc_frame,
            text="Upload File",
            width=120,
            fg_color="gray",
            command=self.upload_file
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            self.section_body,
            text="Accepted formats: PDF, JPG, JPEG, PNG",
            text_color="gray",
            font=("Helvetica", 12)
        ).pack(anchor="w", padx=20)

        self.create_section("Additional Information (Optional)")

        self.additional_text = ctk.CTkTextbox(self.section_body, height=120)
        self.additional_text.pack(fill="x", padx=20, pady=15)

        ctk.CTkButton(
            self.scroll_frame,
            text="Submit Verification Form",
            fg_color=BTN_GREEN,
            command=self.submit
        ).pack(pady=15)

        ctk.CTkButton(
            self.scroll_frame,
            text="Clear Form",
            fg_color="gray",
            command=self.clear_form
        ).pack(pady=5)

        ctk.CTkButton(
            self.scroll_frame,
            text="Back",
            fg_color="gray",
            command=controller.show_applicant_dashboard
        ).pack(pady=5)

        ctk.CTkLabel(self.scroll_frame, text="").pack(pady=30)

    def create_section(self, title):
        section_frame = ctk.CTkFrame(
            self.scroll_frame,
            corner_radius=10,
            fg_color=CARD_BG
        )
        section_frame.pack(pady=15, padx=80, fill="x")

        top_bar = ctk.CTkFrame(section_frame, fg_color=SECTION_BLUE)
        top_bar.pack(fill="x")

        ctk.CTkLabel(
            top_bar,
            text=title,
            font=("Helvetica", 14, "bold"),
            text_color="white"
        ).pack(pady=8, padx=15, anchor="w")

        self.section_body = ctk.CTkFrame(section_frame, fg_color=BODY_BG)
        self.section_body.pack(fill="x")

    def add_entry(self, label, key, required=False):
        ctk.CTkLabel(
            self.section_body,
            text=label + (": *" if required else ":"),
            text_color="white"
        ).pack(anchor="w", padx=20, pady=(10, 5))

        entry = ctk.CTkEntry(self.section_body, width=300)
        entry.pack(anchor="w", padx=20)

        self.entries[key] = {"widget": entry, "required": required}

    def upload_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[
                ("PDF Files", "*.pdf"),
                ("Image Files", "*.jpg *.jpeg *.png"),
                ("All Files", "*.*")
            ]
        )

        if not filename:
            return

        try:
            with open(filename, "rb") as f:
                file_bytes = f.read()

            self.file_base64 = base64.b64encode(file_bytes).decode("utf-8")
            self.file_original_name = os.path.basename(filename)

            self.doc_entry.delete(0, tk.END)
            self.doc_entry.insert(0, self.file_original_name)

        except Exception as e:
            self.file_base64 = ""
            self.file_original_name = ""
            messagebox.showerror(
                "File Upload Failed",
                f"The file could not be uploaded. Please try again.\n\nDetails: {e}"
            )

    def clear_form(self):
        for data in self.entries.values():
            data["widget"].delete(0, "end")
            data["widget"].configure(border_color="#565b5e")

        self.status_var.set("Full-Time")
        self.additional_text.delete("1.0", "end")

        self.doc_entry.delete(0, tk.END)
        self.file_base64 = ""
        self.file_original_name = ""

        messagebox.showinfo(
            "Form Cleared",
            "The form has been cleared. You can now enter new information."
        )

    def is_valid_date(self, value):
        return re.fullmatch(r"\d{2}/\d{2}/\d{4}", value) is not None

    def is_positive_number(self, value):
        try:
            return float(value) > 0
        except ValueError:
            return False

    def submit(self):
        user = getattr(self.controller, "current_user", None)

        if not user:
            messagebox.showerror(
                "Session Error",
                "No user session was found. Please log in again before submitting the form."
            )
            return

        payload = {}
        missing = []

        for key, data in self.entries.items():
            value = data["widget"].get().strip()
            payload[key] = value

            if data["required"] and not value:
                data["widget"].configure(border_color=ERROR_RED)
                missing.append(key)
            else:
                data["widget"].configure(border_color="#565b5e")

        payload["employment_status"] = self.status_var.get().strip()
        payload["additional_information"] = self.additional_text.get("1.0", "end").strip()
        payload["document_name"] = self.file_original_name
        payload["document_data_base64"] = self.file_base64

        if missing:
            messagebox.showwarning(
                "Missing Required Information",
                "Please complete all required fields marked with * before submitting."
            )
            return

        if not self.is_valid_date(payload["start_date"]):
            self.entries["start_date"]["widget"].configure(border_color=ERROR_RED)
            messagebox.showerror(
                "Invalid Start Date",
                "Start Date must be entered in MM/DD/YYYY format.\nExample: 04/28/2026"
            )
            return

        if not self.is_positive_number(payload["hours_per_week"]):
            self.entries["hours_per_week"]["widget"].configure(border_color=ERROR_RED)
            messagebox.showerror(
                "Invalid Hours Per Week",
                "Hours Per Week must be a number greater than 0.\nExample: 40"
            )
            return

        monthly_income = payload.get("monthly_income", "").strip()
        if monthly_income and not self.is_positive_number(monthly_income):
            self.entries["monthly_income"]["widget"].configure(border_color=ERROR_RED)
            messagebox.showerror(
                "Invalid Monthly Gross Income",
                "Monthly Gross Income must be a number greater than 0.\nExample: 2500"
            )
            return

        ok = submit_employment_verification(user, payload)

        if ok:
            messagebox.showinfo(
                "Submission Successful",
                "Employment verification submitted successfully.\nStatus is now Pending Review."
            )
            self.controller.show_status()
        else:
            messagebox.showerror(
                "Submission Failed",
                "The form could not be submitted. Please review the information and try again."
            )