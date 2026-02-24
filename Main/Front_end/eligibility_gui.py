# Front_end/eligibility_gui.py

import customtkinter as ctk
from tkinter import messagebox

HEADER_BLUE = "#5b9bd5"
BTN_GREEN = "#7dd169"

class EligibilityScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # ================= HEADER =================
        ctk.CTkLabel(
            self,
            text="Medicaid Eligibility Check",
            font=("Helvetica", 24, "bold"),
            fg_color=HEADER_BLUE,
            text_color="white",
            corner_radius=0
        ).pack(fill="x", ipady=15)

        # ================= CONTEXT SECTION =================
        context_box = ctk.CTkFrame(self, corner_radius=10)
        context_box.pack(pady=20, padx=40, fill="x")

        ctk.CTkLabel(
            context_box,
            text="This tool provides a preliminary estimate based on key factors.\n"
                 "Final eligibility is determined after full application review.",
            font=("Helvetica", 13),
            justify="center"
        ).pack(pady=15)

        # ================= FORM SECTION =================
        form = ctk.CTkFrame(self, corner_radius=10)
        form.pack(pady=10)

        ctk.CTkLabel(form, text="Household Size:").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.size_entry = ctk.CTkEntry(form, width=220)
        self.size_entry.grid(row=0, column=1, pady=10)

        ctk.CTkLabel(form, text="Monthly Income ($):").grid(row=1, column=0, padx=15, pady=10, sticky="w")
        self.income_entry = ctk.CTkEntry(form, width=220)
        self.income_entry.grid(row=1, column=1, pady=10)

        # Basic additional requirement
        ctk.CTkLabel(form, text="Missouri Resident:").grid(row=2, column=0, padx=15, pady=10, sticky="w")
        self.resident_option = ctk.CTkOptionMenu(form, values=["Yes", "No"])
        self.resident_option.set("Yes")
        self.resident_option.grid(row=2, column=1, pady=10)

        # Income Threshold Display
        self.threshold_label = ctk.CTkLabel(self, text="", font=("Helvetica", 13))
        self.threshold_label.pack(pady=10)

        # ================= RESULT BOX =================
        self.result_box = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.result_box.pack(pady=10, padx=60, fill="x")

        self.result_text = ctk.CTkLabel(self.result_box, text="", font=("Helvetica", 15, "bold"))
        self.result_text.pack(pady=10)

        # ================= BUTTONS =================
        ctk.CTkButton(
            self,
            text="Check Eligibility",
            fg_color=BTN_GREEN,
            command=self.run_check
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Back",
            fg_color="gray",
            command=controller.show_applicant_dashboard
        ).pack(pady=5)

    def run_check(self):
        try:
            hh = int(self.size_entry.get().strip())
            inc = float(self.income_entry.get().strip())
        except:
            messagebox.showerror("Error", "Enter valid numbers.")
            return

        if hh <= 0 or inc < 0:
            messagebox.showerror("Error", "Enter realistic values.")
            return

        # Simple income rule
        limit = 2500 + max(0, hh - 4) * 150
        self.threshold_label.configure(
            text=f"Income limit for household size {hh}: ${limit:,.2f}"
        )

        # Resident requirement check
        if self.resident_option.get() == "No":
            self.result_box.configure(fg_color="#ff4d4d")
            self.result_text.configure(
                text="You may not be eligible.\nApplicant must be a Missouri resident.",
                text_color="white"
            )
            return

        # Income-based decision
        if inc <= limit * 0.9:
            # Strong eligible
            self.result_box.configure(fg_color="#3cb371")  # green
            self.result_text.configure(
                text="You may qualify for Medicaid coverage.",
                text_color="white"
            )

        elif inc <= limit:
            # Borderline case
            self.result_box.configure(fg_color="#f0ad4e")  # yellow
            self.result_text.configure(
                text="You may qualify under certain programs.\nFurther review required.",
                text_color="white"
            )

        else:
            # Not eligible
            self.result_box.configure(fg_color="#ff4d4d")  # red
            self.result_text.configure(
                text="Based on the information provided,\nyou may not be eligible.",
                text_color="white"
            )