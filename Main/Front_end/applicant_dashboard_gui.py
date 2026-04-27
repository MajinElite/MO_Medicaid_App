# Front_end/applicant_dashboard_gui.py

import customtkinter as ctk

PRIMARY_BLUE = "#3b82f6"
PRIMARY_BLUE_HOVER = "#2563eb"

CARD_BG = "#1f1f1f"
HOVER_BG = "#2a2a2a"
TEXT_GRAY = "#b0b0b0"
SECTION_BG = "#2b2b2b"


class ApplicantDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        user = controller.current_user or {}
        name = user.get("name") or "Applicant"

        # ================= HEADER =================
        ctk.CTkLabel(
            self,
            text="Missouri Medicaid Applicant Portal",
            font=("Helvetica", 24, "bold"),
            fg_color=PRIMARY_BLUE,
            text_color="white",
            corner_radius=0
        ).pack(fill="x", ipady=15)

        # ================= MAIN WRAPPER =================
        wrapper = ctk.CTkFrame(self, fg_color="transparent")
        wrapper.pack(expand=True)

        main_card = ctk.CTkFrame(
            wrapper,
            fg_color="transparent",
            corner_radius=18,
            width=900,
            height=540
        )
        main_card.pack(pady=10)
        main_card.pack_propagate(False)

        # ================= WELCOME =================
        welcome_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        welcome_frame.pack(pady=(5, 20))

        ctk.CTkLabel(
            welcome_frame,
            text=f"Welcome, {name}",
            font=("Helvetica", 22, "bold"),
            text_color="white"
        ).pack()

        ctk.CTkLabel(
            welcome_frame,
            text=(
                "Manage your Medicaid application below.\n"
                "Select a section to review requirements, submit forms, or track your status."
            ),
            font=("Helvetica", 13),
            text_color=TEXT_GRAY,
            justify="center",
            wraplength=600
        ).pack(pady=8)

        # ================= GRID =================
        grid = ctk.CTkFrame(main_card, fg_color="transparent")
        grid.pack(pady=5)

        for i in range(3):
            grid.grid_columnconfigure(i, weight=1)

        # ================= CARD CREATOR =================
        def create_card(parent, row, col, icon, title, desc, command):
            card = ctk.CTkFrame(
                parent,
                width=245,
                height=170,
                corner_radius=18,
                fg_color=CARD_BG
            )
            card.grid(row=row, column=col, padx=18, pady=18)
            card.grid_propagate(False)

            icon_label = ctk.CTkLabel(
                card,
                text=icon,
                font=("Segoe UI Emoji", 26),
                text_color="white"
            )
            icon_label.pack(pady=(18, 8))

            title_label = ctk.CTkLabel(
                card,
                text=title,
                font=("Helvetica", 15, "bold"),
                text_color="white"
            )
            title_label.pack(pady=(4, 8))

            desc_label = ctk.CTkLabel(
                card,
                text=desc,
                font=("Helvetica", 12),
                text_color=TEXT_GRAY,
                wraplength=190,
                justify="center"
            )
            desc_label.pack(pady=(4, 10), padx=10)

            def on_enter(event):
                card.configure(
                    fg_color=HOVER_BG,
                    border_color=PRIMARY_BLUE,
                    border_width=2
                )

            def on_leave(event):
                card.configure(
                    fg_color=CARD_BG,
                    border_width=0
                )

            def on_click(event=None):
                command()

            for widget in [card, icon_label, title_label, desc_label]:
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
                widget.bind("<Button-1>", on_click)

            return card

        # ================= TOP ROW =================
        create_card(
            grid, 0, 0,
            "📄",
            "Review Requirements",
            "View eligibility rules and required documents.",
            controller.show_review_program_requirements
        )

        create_card(
            grid, 0, 1,
            "✓",
            "Check Eligibility",
            "Estimate eligibility based on household and income.",
            controller.show_eligibility
        )

        create_card(
            grid, 0, 2,
            "🧾",
            "Employment Verification",
            "Submit employment details and supporting documents.",
            controller.show_verification
        )

        # ================= BOTTOM ROW =================
        bottom_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        bottom_frame.pack(pady=(0, 5))

        create_card(
            bottom_frame, 0, 0,
            "⚠️",
            "Exemption Request",
            "Request review for special circumstances.",
            controller.show_exemption
        )

        create_card(
            bottom_frame, 0, 1,
            "📊",
            "Application Status",
            "Track review progress and caseworker updates.",
            controller.show_status
        )

        # ================= LOGOUT =================
        ctk.CTkButton(
            main_card,
            text="Logout",
            width=160,
            height=36,
            fg_color="gray",
            hover_color="#666666",
            command=controller.logout
        ).pack(pady=(10, 0))