# Front_end/exemption_gui.py

import customtkinter as ctk
from tkinter import messagebox

from Back_end.application_logic import submit_employment_verification

HEADER_BLUE = "#5b9bd5"
BTN_GREEN = "#7dd169"
BTN_GREEN_HOVER = "#5fbd50"
CARD_BG = "#2b2b2b"
BODY_BG = "#343638"
ERROR_RED = "#dc3545"
DEFAULT_BORDER = "#565b5e"
TEXT_MUTED = "#b0b0b0"


class ExemptionScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # ================= HEADER =================
        ctk.CTkLabel(
            self,
            text="Medicaid Exemption Request",
            font=("Helvetica", 24, "bold"),
            fg_color=HEADER_BLUE,
            text_color="white",
            corner_radius=0
        ).pack(fill="x", ipady=15)

        # ================= CONTEXT =================
        context = ctk.CTkFrame(self, corner_radius=10, fg_color=CARD_BG)
        context.pack(pady=(25, 10), padx=70, fill="x")

        ctk.CTkLabel(
            context,
            text=(
                "Use this form if you believe you qualify for an exemption from the employment requirement.\n"
                "A caseworker will review your request after submission."
            ),
            font=("Helvetica", 13),
            text_color="white",
            justify="center",
            wraplength=900
        ).pack(pady=15)

        # ================= FORM =================
        form = ctk.CTkFrame(self, corner_radius=10, fg_color=CARD_BG)
        form.pack(pady=10, padx=70, fill="x")

        # Exemption Type
        ctk.CTkLabel(
            form,
            text="Select Exemption Type: *",
            font=("Helvetica", 14, "bold"),
            text_color="white"
        ).pack(pady=(20, 5), padx=20, anchor="w")

        self.exemption_type = ctk.CTkOptionMenu(
            form,
            values=[
                "Medical Hardship",
                "Caregiver Status",
                "Educational Enrollment",
                "Other"
            ],
            fg_color=HEADER_BLUE,
            button_color="#3b6ea5",
            button_hover_color="#2f5d8c"
        )
        self.exemption_type.set("Medical Hardship")
        self.exemption_type.pack(pady=5, padx=20, anchor="w")

        # Details
        ctk.CTkLabel(
            form,
            text="Reasoning / Details: *",
            font=("Helvetica", 14, "bold"),
            text_color="white"
        ).pack(pady=(15, 5), padx=20, anchor="w")

        ctk.CTkLabel(
            form,
            text="Explain why you are requesting this exemption. Include any relevant situation, dates, or documentation details.",
            font=("Helvetica", 12),
            text_color=TEXT_MUTED,
            wraplength=900,
            justify="left"
        ).pack(pady=(0, 5), padx=20, anchor="w")

        self.details = ctk.CTkTextbox(
            form,
            height=140,
            fg_color=BODY_BG,
            border_color=DEFAULT_BORDER,
            border_width=2
        )
        self.details.pack(pady=(5, 20), padx=20, fill="x")

        # ================= FEEDBACK =================
        self.feedback_label = ctk.CTkLabel(
            self,
            text="Required fields are marked with. *",
            text_color=TEXT_MUTED,
            font=("Helvetica", 12),
            wraplength=800
        )
        self.feedback_label.pack(pady=(5, 5))

        # ================= BUTTONS =================
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=10)

        self.submit_btn = ctk.CTkButton(
            button_frame,
            text="Submit Exemption",
            width=170,
            fg_color=BTN_GREEN,
            hover_color=BTN_GREEN_HOVER,
            command=self.submit
        )
        self.submit_btn.pack(side="left", padx=8)

        ctk.CTkButton(
            button_frame,
            text="Clear Form",
            width=140,
            fg_color="gray",
            hover_color="#666666",
            command=self.clear_form
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            self,
            text="Back",
            width=140,
            fg_color="gray",
            hover_color="#666666",
            command=controller.show_applicant_dashboard
        ).pack(pady=5)

    # ================= HELPERS =================
    def clear_form(self):
        self.exemption_type.set("Medical Hardship")
        self.details.delete("1.0", "end")
        self.details.configure(border_color=DEFAULT_BORDER)
        self.feedback_label.configure(
            text="Form cleared. Enter new exemption details before submitting.",
            text_color=TEXT_MUTED
        )

    def validate_form(self):
        details_text = self.details.get("1.0", "end").strip()

        self.details.configure(border_color=DEFAULT_BORDER)

        if not details_text:
            self.details.configure(border_color=ERROR_RED)
            self.feedback_label.configure(
                text="Please provide a reason for your exemption request before submitting.",
                text_color=ERROR_RED
            )
            messagebox.showwarning(
                "Missing Exemption Details",
                "Please explain why you are requesting this exemption.\nExample: Medical hardship due to a temporary health condition."
            )
            return False

        if len(details_text) < 10:
            self.details.configure(border_color=ERROR_RED)
            self.feedback_label.configure(
                text="Please provide more detail so a caseworker can review your request.",
                text_color=ERROR_RED
            )
            messagebox.showwarning(
                "More Detail Needed",
                "Your explanation is too short. Please provide at least a brief reason for the exemption request."
            )
            return False

        return True

    # ================= SUBMIT =================
    def submit(self):
        if not self.validate_form():
            return

        user = getattr(self.controller, "current_user", None)

        if not user:
            messagebox.showerror(
                "Session Error",
                "No user session was found. Please log in again before submitting an exemption request."
            )
            return

        exemption_type = self.exemption_type.get().strip()
        details_text = self.details.get("1.0", "end").strip()

        self.submit_btn.configure(state="disabled", text="Processing...")
        self.update()

        try:
            payload = {
                "applicant_name": "",
                "employer_name": "",
                "employee_id": "",
                "employment_status": "",
                "start_date": "",
                "hours_per_week": "",
                "monthly_income": "",
                "document_name": "",
                "document_data_base64": "",
                "additional_information": "",

                "exemption_requested": "Yes",
                "exemption_reason": f"{exemption_type} - {details_text}"
            }

            ok = submit_employment_verification(user, payload)

            if ok:
                messagebox.showinfo(
                    "Exemption Submitted",
                    "Your exemption request has been submitted successfully.\nStatus is now Exemption Pending."
                )
                self.controller.show_status()
            else:
                messagebox.showerror(
                    "Submission Failed",
                    "The exemption request could not be submitted. Please review the information and try again."
                )
                self.submit_btn.configure(state="normal", text="Submit Exemption")

        except Exception as e:
            messagebox.showerror(
                "Submission Error",
                f"Failed to submit exemption request.\n\nDetails: {e}"
            )
            self.submit_btn.configure(state="normal", text="Submit Exemption")