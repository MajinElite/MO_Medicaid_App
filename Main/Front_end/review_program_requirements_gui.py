# Front_end/review_program_requirements_gui.py

import customtkinter as ctk
import webbrowser

HEADER_BLUE = "#5b9bd5"
SECTION_BLUE = "#3b6ea5"
CARD_BG = "#2b2b2b"
BODY_BG = "#343638"
BTN_GREEN = "#7dd169"

class ReviewProgramRequirementsScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")

        self.app = app

        # ================= MAIN HEADER =================
        header = ctk.CTkFrame(self, fg_color=HEADER_BLUE, corner_radius=0)
        header.pack(fill="x")

        ctk.CTkLabel(
            header,
            text="Missouri Medicaid",
            font=("Helvetica", 24, "bold"),
            text_color="white"
        ).pack(pady=15)

        # ================= PAGE TITLE =================
        ctk.CTkLabel(
            self,
            text="Missouri Medicaid Program Requirements",
            font=("Helvetica", 20, "bold"),
            text_color="white"
        ).pack(pady=25)

        # ================= SECTIONS =================
        self.create_section(
            title="Basic Eligibility",
            content=(
                "• Missouri resident\n"
                "• Meet income guidelines\n"
                "• Meet employment verification requirements (if applicable)"
            )
        )

        self.create_section(
            title="Employment Requirements",
            content=(
                "• Recent pay stubs (last 30 days)\n"
                "• Employer contact information\n"
                "• Hours worked per week\n"
                "• Self-employment documentation (if applicable)"
            )
        )

        self.create_section(
            title="Documents You May Need",
            content=(
                "• Government-issued ID\n"
                "• Social Security Number\n"
                "• Proof of Missouri residency\n"
                "• Proof of income\n"
                "• Employer verification form (if required)"
            )
        )

        # ================= OFFICIAL WEBSITE LINK =================
        official_link = ctk.CTkLabel(
            self,
            text="Click here to visit the official Missouri Medicaid website",
            text_color="#4da6ff",
            cursor="hand2",
            font=("Helvetica", 13, "underline")
        )
        official_link.pack(pady=20)

        official_link.bind(
            "<Button-1>",
            lambda e: webbrowser.open("https://mydss.mo.gov/healthcare/apply")
        )

        # ================= BACK BUTTON =================
        ctk.CTkButton(
            self,
            text="Back",
            fg_color=BTN_GREEN,
            command=self.app.show_applicant_dashboard
        ).pack(pady=10)


    def create_section(self, title, content):
        # Outer card container
        section_frame = ctk.CTkFrame(
            self,
            corner_radius=10,
            fg_color=CARD_BG
        )
        section_frame.pack(pady=12, padx=80, fill="x")

        # Blue section header bar
        top_bar = ctk.CTkFrame(
            section_frame,
            fg_color=SECTION_BLUE,
            corner_radius=0
        )
        top_bar.pack(fill="x")

        ctk.CTkLabel(
            top_bar,
            text=title,
            font=("Helvetica", 14, "bold"),
            text_color="white"
        ).pack(pady=8, padx=15, anchor="w")

        # Body content area
        body = ctk.CTkFrame(
            section_frame,
            fg_color=BODY_BG,
            corner_radius=0
        )
        body.pack(fill="x")

        ctk.CTkLabel(
            body,
            text=content,
            font=("Helvetica", 13),
            text_color="white",
            justify="left"
        ).pack(pady=15, padx=20, anchor="w")