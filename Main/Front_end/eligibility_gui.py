# Front_end/eligibility_gui.py

import customtkinter as ctk
from tkinter import messagebox

HEADER_BLUE = "#5b9bd5"
BTN_GREEN = "#7dd169"
ERROR_RED = "#dc3545"
DEFAULT_BORDER = "#565b5e"


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
            text=(
                "This tool provides a preliminary estimate based on key factors.\n"
                "Final eligibility is determined after full application review.\n"
                "Required fields are marked with *."
            ),
            font=("Helvetica", 13),
            justify="center"
        ).pack(pady=15)

        # ================= FORM SECTION =================
        form = ctk.CTkFrame(self, corner_radius=10)
        form.pack(pady=10)

        ctk.CTkLabel(form, text="Household Size *:").grid(
            row=0, column=0, padx=15, pady=10, sticky="w"
        )
        self.size_entry = ctk.CTkEntry(
            form,
            width=220,
            placeholder_text="Example: 3"
        )
        self.size_entry.grid(row=0, column=1, pady=10)

        ctk.CTkLabel(form, text="Monthly Income ($) *:").grid(
            row=1, column=0, padx=15, pady=10, sticky="w"
        )
        self.income_entry = ctk.CTkEntry(
            form,
            width=220,
            placeholder_text="Example: 2500"
        )
        self.income_entry.grid(row=1, column=1, pady=10)

        ctk.CTkLabel(form, text="Missouri Resident *:").grid(
            row=2, column=0, padx=15, pady=10, sticky="w"
        )
        self.resident_option = ctk.CTkOptionMenu(form, values=["Yes", "No"])
        self.resident_option.set("Yes")
        self.resident_option.grid(row=2, column=1, pady=10)

        # ================= FEEDBACK LABEL =================
        self.feedback_label = ctk.CTkLabel(
            self,
            text="Enter your household size and monthly income, then click Check Eligibility.",
            font=("Helvetica", 12),
            text_color="gray",
            wraplength=500
        )
        self.feedback_label.pack(pady=(10, 0))

        # ================= INCOME THRESHOLD DISPLAY =================
        self.threshold_label = ctk.CTkLabel(self, text="", font=("Helvetica", 13))
        self.threshold_label.pack(pady=10)

        # ================= RESULT BOX =================
        self.result_box = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.result_box.pack(pady=10, padx=60, fill="x")

        self.result_text = ctk.CTkLabel(
            self.result_box,
            text="",
            font=("Helvetica", 15, "bold"),
            wraplength=600
        )
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
            text="Clear Form",
            fg_color="gray",
            command=self.clear_form
        ).pack(pady=5)

        ctk.CTkButton(
            self,
            text="Back",
            fg_color="gray",
            command=controller.show_applicant_dashboard
        ).pack(pady=5)

        # Keyboard support
        self.size_entry.bind("<Return>", self.run_check_event)
        self.income_entry.bind("<Return>", self.run_check_event)

    # ================= HELPERS =================
    def run_check_event(self, event=None):
        self.run_check()

    def reset_entry_borders(self):
        self.size_entry.configure(border_color=DEFAULT_BORDER)
        self.income_entry.configure(border_color=DEFAULT_BORDER)

    def clear_form(self):
        self.size_entry.delete(0, "end")
        self.income_entry.delete(0, "end")
        self.resident_option.set("Yes")

        self.reset_entry_borders()

        self.feedback_label.configure(
            text="Form cleared. Enter new information to check eligibility.",
            text_color="gray"
        )
        self.threshold_label.configure(text="")
        self.result_box.configure(fg_color="transparent")
        self.result_text.configure(text="", text_color="white")

    def validate_inputs(self):
        self.reset_entry_borders()

        household_text = self.size_entry.get().strip()
        income_text = self.income_entry.get().strip()

        if not household_text and not income_text:
            self.size_entry.configure(border_color=ERROR_RED)
            self.income_entry.configure(border_color=ERROR_RED)
            messagebox.showerror(
                "Missing Required Information",
                "Please enter Household Size and Monthly Income before checking eligibility."
            )
            return None, None

        if not household_text:
            self.size_entry.configure(border_color=ERROR_RED)
            messagebox.showerror(
                "Missing Household Size",
                "Household Size is required.\nExample: 3"
            )
            return None, None

        if not income_text:
            self.income_entry.configure(border_color=ERROR_RED)
            messagebox.showerror(
                "Missing Monthly Income",
                "Monthly Income is required.\nExample: 2500"
            )
            return None, None

        try:
            household_size = int(household_text)
        except ValueError:
            self.size_entry.configure(border_color=ERROR_RED)
            messagebox.showerror(
                "Invalid Household Size",
                "Household Size must be a whole number.\nExample: 1, 2, 3, or 4"
            )
            return None, None

        try:
            monthly_income = float(income_text)
        except ValueError:
            self.income_entry.configure(border_color=ERROR_RED)
            messagebox.showerror(
                "Invalid Monthly Income",
                "Monthly Income must be entered as a number.\nExample: 2500"
            )
            return None, None

        if household_size <= 0:
            self.size_entry.configure(border_color=ERROR_RED)
            messagebox.showerror(
                "Invalid Household Size",
                "Household Size must be greater than 0.\nExample: 3"
            )
            return None, None

        if monthly_income < 0:
            self.income_entry.configure(border_color=ERROR_RED)
            messagebox.showerror(
                "Invalid Monthly Income",
                "Monthly Income cannot be negative.\nExample: 2500"
            )
            return None, None

        return household_size, monthly_income

    # ================= ELIGIBILITY CHECK =================
    def run_check(self):
        hh, inc = self.validate_inputs()

        if hh is None or inc is None:
            return

        self.feedback_label.configure(
            text="Eligibility estimate completed. Review the result below.",
            text_color="gray"
        )

        # Simple income rule
        limit = 2500 + max(0, hh - 4) * 150
        self.threshold_label.configure(
            text=f"Income limit for household size {hh}: ${limit:,.2f}"
        )

        # Resident requirement check
        if self.resident_option.get() == "No":
            self.result_box.configure(fg_color="#ff4d4d")
            self.result_text.configure(
                text=(
                    "Result: May Not Be Eligible (Red)\n"
                    "Reason: Applicant must be a Missouri resident."
                ),
                text_color="white"
            )
            return

        # Income-based decision
        if inc <= limit * 0.9:
            self.result_box.configure(fg_color="#3cb371")
            self.result_text.configure(
                text=(
                    "Result: Likely Eligible (Green)\n"
                    "Based on the information provided, you may qualify for Medicaid coverage."
                ),
                text_color="white"
            )

        elif inc <= limit:
            self.result_box.configure(fg_color="#f0ad4e")
            self.result_text.configure(
                text=(
                    "Result: Further Review Required (Yellow)\n"
                    "You may qualify under certain programs, but a caseworker review is needed."
                ),
                text_color="black"
            )

        else:
            self.result_box.configure(fg_color="#ff4d4d")
            self.result_text.configure(
                text=(
                    "Result: May Not Be Eligible (Red)\n"
                    "Based on the information provided, your income may exceed the current estimate."
                ),
                text_color="white"
            )