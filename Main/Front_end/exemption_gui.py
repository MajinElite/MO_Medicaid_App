# Fallback import in case Tommy hasn't pushed the backend update yet: UPDATED
# Ammar: Fixed to work with SQLite Database
# Front_end/exemption_gui.py

import customtkinter as ctk
from tkinter import messagebox

from Back_end.application_logic import submit_employment_verification

HEADER_BLUE = "#5b9bd5"
BTN_GREEN = "#7dd169"
CARD_BG = "#2b2b2b"


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

        # ================= FORM =================
        form = ctk.CTkFrame(self, corner_radius=10, fg_color=CARD_BG)
        form.pack(pady=30, padx=60, fill="x")

        # Exemption Type
        ctk.CTkLabel(
            form,
            text="Select Exemption Type:",
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
            ]
        )
        self.exemption_type.pack(pady=5, padx=20, anchor="w")

        # Details
        ctk.CTkLabel(
            form,
            text="Reasoning / Details:",
            font=("Helvetica", 14, "bold"),
            text_color="white"
        ).pack(pady=(15, 5), padx=20, anchor="w")

        self.details = ctk.CTkTextbox(form, height=120)
        self.details.pack(pady=5, padx=20, fill="x")

        # ================= BUTTONS =================
        self.submit_btn = ctk.CTkButton(
            self,
            text="Submit Exemption",
            fg_color=BTN_GREEN,
            command=self.submit
        )
        self.submit_btn.pack(pady=15)

        ctk.CTkButton(
            self,
            text="Back",
            fg_color="gray",
            command=controller.show_applicant_dashboard
        ).pack(pady=5)

    # ================= SUBMIT =================
    def submit(self):
        details_text = self.details.get("1.0", "end").strip()

        if not details_text:
            messagebox.showwarning(
                "Missing Information",
                "Please provide details for your exemption."
            )
            return

        # Disable button to prevent spam clicks
        self.submit_btn.configure(state="disabled", text="Processing...")
        self.update()

        try:
            payload = {
                # Normal fields (left empty intentionally)
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

                # 🔥 IMPORTANT FIELDS
                "exemption_requested": "Yes",
                "exemption_reason": f"{self.exemption_type.get()} - {details_text}"
            }

            ok = submit_employment_verification(
                self.controller.current_user,
                payload
            )

            if ok:
                messagebox.showinfo(
                    "Success",
                    "Exemption request submitted successfully."
                )
                self.controller.show_status()
            else:
                raise Exception("Submission failed")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit exemption: {e}")
            self.submit_btn.configure(state="normal", text="Submit Exemption")