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

        ctk.CTkLabel(
            self,
            text="Application Status",
            font=("Helvetica", 24, "bold"),
            fg_color=HEADER_BLUE,
            text_color="white",
            corner_radius=0
        ).pack(fill="x", ipady=15)

        self.status_label = ctk.CTkLabel(self, text="", font=("Helvetica", 18))
        self.status_label.pack(pady=25)

        self.reason_label = ctk.CTkLabel(self, text="", font=("Helvetica", 14), text_color="red")
        self.reason_label.pack(pady=5)

        ctk.CTkButton(self, text="Refresh", fg_color=BTN_GREEN, command=self.refresh).pack(pady=10)
        ctk.CTkButton(self, text="Back", fg_color="gray", command=controller.show_applicant_dashboard).pack(pady=5)

        self.refresh()

    def refresh(self):
        user = self.controller.current_user
        info = get_application_status(user)

        status = info.get("status", "None")
        reason = info.get("reason", "")

        if status == "None":
            self.status_label.configure(text="No application submitted", text_color="gray")
            self.reason_label.configure(text="")
        elif status in ["Pending", "Under Review"]:
            self.status_label.configure(text="Under Review", text_color="orange")
            self.reason_label.configure(text="")
        elif status == "Approved":
            self.status_label.configure(text="Approved", text_color="green")
            self.reason_label.configure(text="")
        elif status == "Denied":
            self.status_label.configure(text="Denied", text_color="red")
            self.reason_label.configure(text=reason if reason else "No reason provided.")
        else:
            self.status_label.configure(text=status, text_color="black")
            self.reason_label.configure(text=reason)