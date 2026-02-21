# Main.py
import customtkinter as ctk

from Front_end.login_gui import LoginScreen
from Front_end.applicant_dashboard_gui import ApplicantDashboard
from Front_end.eligibility_gui import EligibilityScreen
from Front_end.verification_gui import VerificationScreen
from Front_end.status_gui import StatusScreen
from Front_end.caseworker_dashboard_gui import CaseworkerDashboard

# --- CUSTOMTKINTER SETUP ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Missouri Medicaid Portal")
        self.geometry("900x650")

        self.current_user = None  # {"username": "", "role": "Applicant|Caseworker", "name": ""}

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.show_login()

    def clear_window(self):
        for w in self.container.winfo_children():
            w.destroy()

    def set_user(self, user_dict):
        self.current_user = user_dict

    def logout(self):
        self.current_user = None
        self.show_login()

    # ----- ROUTES -----
    def show_login(self):
        self.clear_window()
        LoginScreen(self.container, self).pack(fill="both", expand=True)

    def show_applicant_dashboard(self):
        self.clear_window()
        ApplicantDashboard(self.container, self).pack(fill="both", expand=True)

    def show_caseworker_dashboard(self):
        self.clear_window()
        CaseworkerDashboard(self.container, self).pack(fill="both", expand=True)

    def show_eligibility(self):
        self.clear_window()
        EligibilityScreen(self.container, self).pack(fill="both", expand=True)

    def show_verification(self):
        self.clear_window()
        VerificationScreen(self.container, self).pack(fill="both", expand=True)

    def show_status(self):
        self.clear_window()
        StatusScreen(self.container, self).pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()