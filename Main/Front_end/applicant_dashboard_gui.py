# Front_end/applicant_dashboard_gui.py
import customtkinter as ctk
import webbrowser

HEADER_BLUE = "#5b9bd5"
BTN_GREEN = "#7dd169"
TEXT_BLUE = "#3b82f6"

class ApplicantDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        name = (controller.current_user or {}).get("name", "Applicant")

        ctk.CTkLabel(
            self,
            text="Missouri Medicaid",
            font=("Helvetica", 24, "bold"),
            fg_color=HEADER_BLUE,
            text_color="white",
            corner_radius=0
        ).pack(fill="x", ipady=15)

        ctk.CTkLabel(self, text=f"Welcome, {name}", font=("Helvetica", 18)).pack(pady=25)

        ctk.CTkButton(
            self, text="Review Program Requirements",
            font=("Helvetica", 14, "bold"),
            fg_color=BTN_GREEN,
            command=self.open_requirements
        ).pack(pady=10, ipadx=10, ipady=5)

        ctk.CTkButton(
            self, text="Check Eligibility",
            font=("Helvetica", 14, "bold"),
            fg_color=BTN_GREEN,
            command=controller.show_eligibility
        ).pack(pady=10, ipadx=10, ipady=5)

        ctk.CTkButton(
            self, text="Submit Employment Verification",
            font=("Helvetica", 14, "bold"),
            fg_color=BTN_GREEN,
            command=controller.show_verification
        ).pack(pady=10, ipadx=10, ipady=5)

        ctk.CTkButton(
            self, text="Check Application Status",
            font=("Helvetica", 14, "bold"),
            fg_color=BTN_GREEN,
            command=controller.show_status
        ).pack(pady=10, ipadx=10, ipady=5)

        ctk.CTkButton(
            self, text="Logout",
            font=("Helvetica", 14, "bold"),
            fg_color="gray",
            command=controller.logout
        ).pack(pady=20, ipadx=10, ipady=5)

        link = ctk.CTkLabel(
            self,
            text="For more info on Program Requirements, click here.",
            font=("Helvetica", 12, "underline"),
            text_color=TEXT_BLUE,
            cursor="hand2"
        )
        link.pack(side="bottom", pady=20)
        link.bind("<Button-1>", lambda e: webbrowser.open("https://mydss.mo.gov/healthcare/apply"))

    def open_requirements(self):
        self.controller.clear_window()
        # If you want a separate requirements page later, we can add it.
        # For now it opens the official website:
        webbrowser.open("https://mydss.mo.gov/healthcare/apply")
        self.controller.show_applicant_dashboard()