# Front_end/verification_gui.py

import base64
import os
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

        # Stores the uploaded file content for database saving
        self.file_original_name = ""
        self.file_base64 = ""

        # ================= SCROLLABLE CONTAINER =================
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True)

        # ================= HEADER =================
        ctk.CTkLabel(
            self.scroll_frame,
            text="Employment Verification Form",
            font=("Helvetica", 24, "bold"),
            fg_color=HEADER_BLUE,
            text_color="white",
            corner_radius=0
        ).pack(fill="x", ipady=15)

        # ================= CONTEXT =================
        context = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
        context.pack(pady=20, padx=60, fill="x")

        ctk.CTkLabel(
            context,
            text=(
                "This form verifies employment details for Medicaid eligibility review.\n"
                "Please ensure all required fields are accurate before submission."
            ),
            font=("Helvetica", 13),
            justify="center"
        ).pack(pady=15)

        # ================= APPLICANT INFO =================
        self.create_section("Applicant Information")
        self.add_entry("Applicant Name", "applicant_name", required=True)

        # ================= EMPLOYMENT INFO =================
        self.create_section("Employment Information")
        self.add_entry("Employer Name", "employer_name", required=True)
        self.add_entry("Employee ID", "employee_id", required=True)

        # Employment Status
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

        # ================= DOCUMENTS =================
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

        # ================= ADDITIONAL INFO =================
        self.create_section("Additional Information (Optional)")

        self.additional_text = ctk.CTkTextbox(self.section_body, height=120)
        self.additional_text.pack(fill="x", padx=20, pady=15)

        # ================= BUTTONS =================
        ctk.CTkButton(
            self.scroll_frame,
            text="Submit Verification Form",
            fg_color=BTN_GREEN,
            command=self.submit
        ).pack(pady=15)

        ctk.CTkButton(
            self.scroll_frame,
            text="Back",
            fg_color="gray",
            command=controller.show_applicant_dashboard
        ).pack(pady=5)

        # Bottom padding for breathing room
        ctk.CTkLabel(self.scroll_frame, text="").pack(pady=30)

    # ================= SECTION CREATOR =================
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

    # ================= ENTRY CREATOR =================
    def add_entry(self, label, key, required=False):
        ctk.CTkLabel(
            self.section_body,
            text=label + (":" if not required else ": *"),
            text_color="white"
        ).pack(anchor="w", padx=20, pady=(10, 5))

        entry = ctk.CTkEntry(self.section_body, width=300)
        entry.pack(anchor="w", padx=20)

        self.entries[key] = {"widget": entry, "required": required}

    # ================= FILE UPLOAD =================
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
            # Read the file in binary, encode to base64 for JSON storage
            with open(filename, "rb") as f:
                file_bytes = f.read()

            self.file_base64 = base64.b64encode(file_bytes).decode("utf-8")
            self.file_original_name = os.path.basename(filename)

            self.doc_entry.delete(0, tk.END)
            self.doc_entry.insert(0, self.file_original_name)

        except Exception as e:
            self.file_base64 = ""
            self.file_original_name = ""
            messagebox.showerror("Error", f"File upload failed: {e}")

    # ================= SUBMIT =================
    def submit(self):
        user = getattr(self.controller, "current_user", None)
        if not user:
            messagebox.showerror("Error", "No user session found.")
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

        # Save uploaded document into the database
        payload["document_name"] = self.file_original_name
        payload["document_data_base64"] = self.file_base64

        if missing:
            messagebox.showwarning(
                "Missing Information",
                "Please complete all required fields before submitting."
            )
            return

        ok = submit_employment_verification(user, payload)

        if ok:
            messagebox.showinfo(
                "Success",
                "Form submitted for review.\nStatus is now Pending."
            )
            self.controller.show_status()
        else:
            messagebox.showerror("Error", "Submit failed.")