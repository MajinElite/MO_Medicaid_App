# Front_end/verification_gui.py
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox

HEADER_BLUE = "#5b9bd5"
BTN_GREEN = "#7dd169"

try:
    from Back_end.application_logic import submit_employment_verification
except Exception:
    def submit_employment_verification(user, payload):
        # placeholder: pretend saved and status set to Pending
        return True

class VerificationScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        ctk.CTkLabel(
            self,
            text="Employment Verification Form",
            font=("Helvetica", 24, "bold"),
            fg_color=HEADER_BLUE,
            text_color="white",
            corner_radius=0
        ).pack(fill="x", ipady=15)

        form = ctk.CTkFrame(self, fg_color="transparent")
        form.pack(pady=20)

        self.entries = {}

        def add_row(r, label, key, width=300):
            ctk.CTkLabel(form, text=label).grid(row=r, column=0, sticky="w", pady=10, padx=10)
            e = ctk.CTkEntry(form, width=width)
            e.grid(row=r, column=1, columnspan=2, sticky="w", pady=10)
            self.entries[key] = e

        add_row(0, "Applicant's Name:", "applicant_name")
        add_row(1, "Employer Name:", "employer_name")
        add_row(2, "Employee ID:", "employee_id")

        ctk.CTkLabel(form, text="Employment Status:").grid(row=3, column=0, sticky="w", pady=10, padx=10)
        self.status_var = tk.StringVar(value="Full-Time")
        ctk.CTkRadioButton(form, text="Full-Time", variable=self.status_var, value="Full-Time").grid(row=3, column=1, sticky="w")
        ctk.CTkRadioButton(form, text="Part-Time", variable=self.status_var, value="Part-Time").grid(row=3, column=2, sticky="w")

        add_row(4, "Start Date:", "start_date", width=150)
        add_row(5, "Hours Per Week:", "hours_per_week", width=150)

        ctk.CTkLabel(form, text="Documents:").grid(row=6, column=0, sticky="w", pady=10, padx=10)
        self.doc_entry = ctk.CTkEntry(form, width=150)
        self.doc_entry.grid(row=6, column=1, sticky="w")

        ctk.CTkButton(
            form, text="Upload File", width=120, fg_color="gray",
            command=self.upload_file
        ).grid(row=6, column=2, padx=10, sticky="w")

        ctk.CTkButton(
            self, text="Submit Verification Form",
            fg_color=BTN_GREEN,
            command=self.submit
        ).pack(pady=15, ipadx=10, ipady=5)

        ctk.CTkButton(
            self, text="Back",
            fg_color="gray",
            command=controller.show_applicant_dashboard
        ).pack(pady=5)

    def upload_file(self):
        filename = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if filename:
            self.doc_entry.delete(0, tk.END)
            self.doc_entry.insert(0, filename.split("/")[-1])

    def submit(self):
        user = self.controller.current_user
        if not user:
            messagebox.showerror("Error", "No user session found.")
            return

        payload = {k: e.get().strip() for k, e in self.entries.items()}
        payload["employment_status"] = self.status_var.get().strip()
        payload["document_name"] = self.doc_entry.get().strip()

        required = ["applicant_name", "employer_name", "employee_id", "start_date", "hours_per_week", "employment_status"]
        missing = [k for k in required if not payload.get(k)]
        if missing:
            messagebox.showwarning("Missing Information", "Please fill out all required fields before submitting.")
            return

        ok = submit_employment_verification(user, payload)
        if ok:
            messagebox.showinfo("Success", "Form submitted for review.\nStatus is now Pending.")
            self.controller.show_status()
        else:
            messagebox.showerror("Error", "Submit failed.")