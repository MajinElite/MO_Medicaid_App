# Front_end/review_program_requirements_gui.py

import customtkinter as ctk
import webbrowser

HEADER_BLUE = "#5b9bd5"
BTN_GREEN = "#7dd169"

class ReviewProgramRequirementsScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")

        self.app = app

        # ================= HEADER =================
        header = ctk.CTkFrame(self, fg_color=HEADER_BLUE, corner_radius=0)
        header.pack(fill="x")

        header_label = ctk.CTkLabel(
            header,
            text="Missouri Medicaid",
            font=("Helvetica", 24, "bold"),
            text_color="white"
        )
        header_label.pack(pady=15)

        # ================= CONTENT =================
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(pady=30)

        # Page Title
        title = ctk.CTkLabel(
            content_frame,
            text="Medicaid Program Requirements",
            font=("Helvetica", 20, "bold")
        )
        title.pack(pady=(0, 20))

        # Eligibility Section
        eligibility_title = ctk.CTkLabel(
            content_frame,
            text="Eligibility Criteria",
            font=("Helvetica", 16, "bold")
        )
        eligibility_title.pack(pady=(10, 5))

        eligibility_text = ctk.CTkLabel(
            content_frame,
            text=(
                "• Must meet income limits based on household size\n"
                "• Must be a Missouri resident\n"
                "• Must provide valid identification\n"
                "• Must verify employment information"
            ),
            justify="left"
        )
        eligibility_text.pack()

        # Documents Section
        documents_title = ctk.CTkLabel(
            content_frame,
            text="Required Documents",
            font=("Helvetica", 16, "bold")
        )
        documents_title.pack(pady=(20, 5))

        documents_text = ctk.CTkLabel(
            content_frame,
            text=(
                "• Proof of income\n"
                "• Employer information\n"
                "• Identification documents\n"
                "• Any supporting documentation"
            ),
            justify="left"
        )
        documents_text.pack()

        # Official Website Link (ONLY HERE)
        official_link = ctk.CTkLabel(
            content_frame,
            text="Click here to visit the official Missouri Medicaid website",
            text_color="#3b82f6",
            cursor="hand2"
        )
        official_link.pack(pady=25)

        official_link.bind(
            "<Button-1>",
            lambda e: webbrowser.open("https://mydss.mo.gov/healthcare/apply")
        )

        # Back Button
        back_button = ctk.CTkButton(
            content_frame,
            text="Back",
            fg_color=BTN_GREEN,
            command=self.app.show_applicant_dashboard
        )
        back_button.pack(pady=10)