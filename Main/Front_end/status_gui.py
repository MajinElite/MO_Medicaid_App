# Front_end/status_gui.py

import customtkinter as ctk

HEADER_BLUE = "#5b9bd5"
BTN_GREEN = "#7dd169"

try:
    from Back_end.application_logic import get_application_status
except Exception:
    def get_application_status(user):
        if not user or user.get("role") != "Applicant":
            return {"status": "None", "reason": ""}
        if user.get("username") == "applicant1":
            return {"status": "Pending", "reason": ""}
        return {"status": "None", "reason": ""}


class StatusScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # ================= HEADER =================
        ctk.CTkLabel(
            self,
            text="Application Status",
            font=("Helvetica", 24, "bold"),
            fg_color=HEADER_BLUE,
            text_color="white",
            corner_radius=0
        ).pack(fill="x", ipady=15)

        # ================= CONTEXT SECTION =================
        context_frame = ctk.CTkFrame(self, corner_radius=10)
        context_frame.pack(pady=20, padx=40, fill="x")

        ctk.CTkLabel(
            context_frame,
            text="This page shows the current status of your submitted application.\n"
                 "Updates occur after caseworker review.",
            font=("Helvetica", 13),
            justify="center"
        ).pack(pady=15)

        # ================= STATUS CARD =================
        self.status_card = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.status_card.pack(pady=10, padx=60, fill="x")

        self.status_label = ctk.CTkLabel(
            self.status_card,
            text="",
            font=("Helvetica", 18, "bold"),
            text_color="white"
        )
        self.status_label.pack(pady=15)

        # ================= DENIAL REASON SECTION =================
        self.reason_frame = ctk.CTkFrame(self, corner_radius=10)
        self.reason_label_title = ctk.CTkLabel(
            self.reason_frame,
            text="Reason for Denial",
            font=("Helvetica", 14, "bold")
        )

        self.reason_label = ctk.CTkLabel(
            self.reason_frame,
            text="",
            font=("Helvetica", 13),
            wraplength=600,
            justify="center"
        )

        # ================= BUTTONS =================
        ctk.CTkButton(
            self,
            text="Refresh",
            fg_color=BTN_GREEN,
            command=self.refresh
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Back",
            fg_color="gray",
            command=controller.show_applicant_dashboard
        ).pack(pady=5)

        self.refresh()

    def refresh(self):
        user = self.controller.current_user
        info = get_application_status(user)

        status = info.get("status", "None")
        reason = info.get("reason", "")

        # Hide reason section by default
        self.reason_frame.pack_forget()

        if status == "None":
            self.status_card.configure(fg_color="#6c757d")  # gray
            self.status_label.configure(text="No Application Submitted")

        elif status in ["Pending", "Under Review", "Exemption Pending"]:
            self.status_card.configure(fg_color="#f0ad4e")  # yellow
            self.status_label.configure(text=f"Application Under Review ({status})")
            
        elif status == "Request Info":
            self.status_card.configure(fg_color="#17a2b8")  # teal
            self.status_label.configure(text="Action Required: More Information Needed")
            
            # Show the reason frame so they know what to fix
            self.reason_frame.pack(pady=15, padx=60, fill="x")
            self.reason_label_title.configure(text="Caseworker Notes")
            self.reason_label_title.pack(pady=(10, 5))
            self.reason_label.pack(pady=(0, 15))
            self.reason_label.configure(text=reason if reason else "Please contact your caseworker.")
        
        elif status == "Approved":
            self.status_card.configure(fg_color="#3cb371")  # green
            self.status_label.configure(text="Application Approved")

        elif status == "Denied":
            self.status_card.configure(fg_color="#dc3545")  # red
            self.status_label.configure(text="Application Denied")

            # Show denial reason section
            self.reason_frame.pack(pady=15, padx=60, fill="x")
            self.reason_label_title.pack(pady=(10, 5))
            self.reason_label.pack(pady=(0, 15))

            self.reason_label.configure(
                text=reason if reason else "No reason provided."
            )

        else:
            self.status_card.configure(fg_color="#6c757d")
            self.status_label.configure(text=status)
