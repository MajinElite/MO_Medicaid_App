# Front_end/applicant_dashboard_gui.py

import customtkinter as ctk

PRIMARY_BLUE = "#3b82f6"
CARD_BG = "#1f1f1f"
HOVER_BG = "#2a2a2a"
TEXT_GRAY = "#a1a1aa"

class ApplicantDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        name = (controller.current_user or {}).get("name", "Applicant")

        # ================= HEADER =================
        ctk.CTkLabel(
            self,
            text="Missouri Medicaid",
            font=("Helvetica", 24, "bold"),
            fg_color=PRIMARY_BLUE,
            text_color="white",
            corner_radius=0
        ).pack(fill="x", ipady=15)

        # ================= WELCOME =================
        welcome_frame = ctk.CTkFrame(self, fg_color="transparent")
        welcome_frame.pack(pady=20)

        ctk.CTkLabel(
            welcome_frame,
            text=f"Welcome, {name}",
            font=("Helvetica", 20, "bold"),
            text_color="white"
        ).pack()

        ctk.CTkLabel(
            welcome_frame,
            text="Manage your Medicaid application below.\nSelect a section to continue.",
            font=("Helvetica", 13),
            text_color=TEXT_GRAY,
            justify="center"
        ).pack(pady=6)

        # ================= GRID =================
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(pady=10)

        # Keep columns balanced
        for i in range(3):
            grid.grid_columnconfigure(i, weight=1)

        # ================= CARD CREATOR =================
        def create_card(parent, row, col, icon, title, desc, command):
            card = ctk.CTkFrame(
                parent,
                width=320,
                height=210,
                corner_radius=18,
                fg_color=CARD_BG
            )
            card.grid(row=row, column=col, padx=20, pady=20)
            card.grid_propagate(False)

            # ICON (fixed size consistency)
            icon_label = ctk.CTkLabel(
                card,
                text=icon,
                font=("Segoe UI Emoji", 24)
            )
            icon_label.pack(pady=(22, 10))

            # TITLE
            title_label = ctk.CTkLabel(
                card,
                text=title,
                font=("Helvetica", 15, "bold"),
                text_color="white"
            )
            title_label.pack(pady=15)

            # DESCRIPTION
            desc_label = ctk.CTkLabel(
                card,
                text=desc,
                font=("Helvetica", 12),
                text_color=TEXT_GRAY,
                wraplength=200,
                justify="center"
            )
            desc_label.pack(pady=10, padx=10)

            # ================= HOVER =================
            def on_enter(e):
                card.configure(
                    fg_color=HOVER_BG,
                    border_color=PRIMARY_BLUE,
                    border_width=2
                )

            def on_leave(e):
                card.configure(
                    fg_color=CARD_BG,
                    border_width=0
                )

            # Bind to entire card
            for widget in [card, icon_label, title_label, desc_label]:
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
                widget.bind("<Button-1>", lambda e: command())

            return card

        # ================= TOP ROW =================
        create_card(
            grid, 0, 0,
            "📄",
            "Review Requirements",
            "View eligibility rules and required documents",
            controller.show_review_program_requirements
        )

        create_card(
            grid, 0, 1,
            "✓",  # FIXED smaller check
            "Check Eligibility",
            "Estimate your qualification based on income",
            controller.show_eligibility
        )

        create_card(
            grid, 0, 2,
            "🧾",
            "Employment Verification",
            "Submit employment details and documents",
            controller.show_verification
        )

        # ================= CENTERED BOTTOM ROW =================
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack()

        create_card(
            bottom_frame, 0, 0,
            "⚠️",
            "Exemption Request",
            "Request exemption for special circumstances",
            controller.show_exemption
        )

        create_card(
            bottom_frame, 0, 1,
            "📊",
            "Application Status",
            "Track your application progress",
            controller.show_status
        )

        # ================= LOGOUT =================
        ctk.CTkButton(
            self,
            text="Logout",
            fg_color="gray",
            command=controller.logout
        ).pack(pady=25)