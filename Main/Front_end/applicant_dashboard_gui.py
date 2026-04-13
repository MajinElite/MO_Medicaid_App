# Front_end/applicant_dashboard_gui.py

import customtkinter as ctk

HEADER_BLUE = "#5b9bd5"
BTN_GREEN = "#7dd169"

class ApplicantDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        name = (controller.current_user or {}).get("name", "Applicant")

        # Header
        ctk.CTkLabel(
            self,
            text="Missouri Medicaid",
            font=("Helvetica", 24, "bold"),
            fg_color=HEADER_BLUE,
            text_color="white",
            corner_radius=0
        ).pack(fill="x", ipady=15)

        # Welcome
        ctk.CTkLabel(
            self,
            text=f"Welcome, {name}",
            font=("Helvetica", 18)
        ).pack(pady=25)

        # Review Program Requirements
        ctk.CTkButton(
            self,
            text="Review Program Requirements",
            font=("Helvetica", 14, "bold"),
            fg_color=BTN_GREEN,
            command=self.controller.show_review_program_requirements
        ).pack(pady=10, ipadx=10, ipady=5)

        # Check Eligibility
        ctk.CTkButton(
            self,
            text="Check Eligibility",
            font=("Helvetica", 14, "bold"),
            fg_color=BTN_GREEN,
            command=controller.show_eligibility
        ).pack(pady=10, ipadx=10, ipady=5)

        # Submit Employment Verification
        ctk.CTkButton(
            self,
            text="Submit Employment Verification",
            font=("Helvetica", 14, "bold"),
            fg_color=BTN_GREEN,
            command=controller.show_verification
        ).pack(pady=10, ipadx=10, ipady=5)
        # Submit Exemption
        ctk.CTkButton(
            self,
            text="File Exemption Request",
            font=("Helvetica", 14, "bold"),
            fg_color=BTN_GREEN, # Using standard green to match the rest
            command=controller.show_exemption
        ).pack(pady=10, ipadx=10, ipady=5)
        # Check Application Status
        ctk.CTkButton(
            self,
            text="Check Application Status",
            font=("Helvetica", 14, "bold"),
            fg_color=BTN_GREEN,
            command=controller.show_status
        ).pack(pady=10, ipadx=10, ipady=5)

        # Logout
        ctk.CTkButton(
            self,
            text="Logout",
            font=("Helvetica", 14, "bold"),
            fg_color="gray",
            command=controller.logout
        ).pack(pady=20, ipadx=10, ipady=5)
