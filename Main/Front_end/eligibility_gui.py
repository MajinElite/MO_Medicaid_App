# Front_end/eligibility_gui.py
import customtkinter as ctk
from tkinter import messagebox

HEADER_BLUE = "#5b9bd5"
BTN_GREEN = "#7dd169"

try:
    from Back_end.application_logic import check_eligibility
except Exception:
    def check_eligibility(household_size, monthly_income):
        # simple placeholder rule
        try:
            hh = int(household_size)
            inc = float(monthly_income)
        except Exception:
            return None
        limit = 2500 + max(0, hh - 4) * 150
        return inc <= limit

class EligibilityScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        ctk.CTkLabel(
            self,
            text="Medicaid Eligibility Check",
            font=("Helvetica", 24, "bold"),
            fg_color=HEADER_BLUE,
            text_color="white",
            corner_radius=0
        ).pack(fill="x", ipady=15)

        form = ctk.CTkFrame(self, fg_color="transparent")
        form.pack(pady=30)

        ctk.CTkLabel(form, text="Household Size:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.size_entry = ctk.CTkEntry(form, width=220)
        self.size_entry.grid(row=0, column=1, pady=10)

        ctk.CTkLabel(form, text="Monthly Income ($):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.income_entry = ctk.CTkEntry(form, width=220)
        self.income_entry.grid(row=1, column=1, pady=10)

        self.result_label = ctk.CTkLabel(self, text="", font=("Helvetica", 16))
        self.result_label.pack(pady=15)

        ctk.CTkButton(self, text="Check Eligibility", fg_color=BTN_GREEN, command=self.run_check).pack(pady=10)
        ctk.CTkButton(self, text="Back", fg_color="gray", command=controller.show_applicant_dashboard).pack(pady=5)

        ctk.CTkLabel(self, text="Not a guarantee.", text_color="gray").pack(pady=10)

    def run_check(self):
        result = check_eligibility(self.size_entry.get().strip(), self.income_entry.get().strip())
        if result is None:
            messagebox.showerror("Error", "Enter valid numbers.")
            return

        if result:
            self.result_label.configure(text="You may be eligible", text_color="green")
        else:
            self.result_label.configure(text="You may not be eligible", text_color="red")