'''
DEVELOPER: Duy Huynh, Ammar Osmun
TASK: Sprint 2
STORIES: Home, Requirements, Eligibility Check, & Employment Verification

'''

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser

# --- CUSTOMTKINTER SETUP ---
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# --- BRAND COLORS ---
HEADER_BLUE = "#5b9bd5"
BTN_GREEN = "#7dd169"
TEXT_BLUE = "#3b82f6"
DIVIDER_COLOR = "#e0e0e0"

def clear_window():
    """Removes all current widgets so we can load a new page."""
    for widget in app.winfo_children():
        widget.destroy()

def open_requirements(event=None):
    """Opens the official Missouri Medicaid requirements page."""
    webbrowser.open("https://mydss.mo.gov/healthcare/apply")

# ==========================================
# PAGE 1: HOME PAGE
# ==========================================
def show_home():
    clear_window()
    
    ctk.CTkLabel(app, text="Missouri Medicaid", font=("Helvetica", 24, "bold"), 
                 fg_color=HEADER_BLUE, text_color="white", corner_radius=0).pack(fill="x", ipady=15)
    
    ctk.CTkLabel(app, text="Welcome to the Medicaid Portal", font=("Helvetica", 18)).pack(pady=30)
    
    ctk.CTkButton(app, text="Review Program Requirements", font=("Helvetica", 14, "bold"), 
                  fg_color=BTN_GREEN, text_color="white", corner_radius=8, command=show_requirements).pack(pady=10, ipadx=10, ipady=5)
    
    ctk.CTkButton(app, text="Check Medicaid Eligibility", font=("Helvetica", 14, "bold"), 
                  fg_color=BTN_GREEN, text_color="white", corner_radius=8, command=show_eligibility).pack(pady=10, ipadx=10, ipady=5)
    
    ctk.CTkButton(app, text="Submit Employment Verification", font=("Helvetica", 14, "bold"), 
                  fg_color=BTN_GREEN, text_color="white", corner_radius=8, command=show_verification).pack(pady=10, ipadx=10, ipady=5)

# ==========================================
# PAGE 2: PROGRAM REQUIREMENTS 
# ==========================================
def show_requirements():
    clear_window()
    
    ctk.CTkLabel(app, text="Missouri Medicaid", font=("Helvetica", 24, "bold"), 
                 fg_color=HEADER_BLUE, text_color="white", corner_radius=0).pack(fill="x", ipady=15)
    
    content_frame = ctk.CTkFrame(app, fg_color="transparent")
    content_frame.pack(pady=20, fill="x", padx=60)
    
    ctk.CTkLabel(content_frame, text="Medicaid Program Requirements", font=("Helvetica", 22, "bold"), text_color=TEXT_BLUE).pack(pady=(0, 10))
    ctk.CTkFrame(content_frame, height=2, fg_color=DIVIDER_COLOR).pack(fill="x", pady=5)
    
    ctk.CTkLabel(content_frame, text="Eligibility Criteria", font=("Helvetica", 18, "bold"), text_color=TEXT_BLUE).pack(anchor="w", pady=(10, 5))
    ctk.CTkLabel(content_frame, text="- Missouri Residency\n- Income Limits\n- Employment Requirements", font=("Helvetica", 15), justify="left").pack(anchor="w", padx=10)
    
    ctk.CTkFrame(content_frame, height=2, fg_color=DIVIDER_COLOR).pack(fill="x", pady=15)
    
    ctk.CTkLabel(content_frame, text="Documents Needed", font=("Helvetica", 18, "bold"), text_color=TEXT_BLUE).pack(anchor="w", pady=(0, 5))
    ctk.CTkLabel(content_frame, text="- Proof of Income\n- Employment Verification\n- ID/SSN", font=("Helvetica", 15), justify="left").pack(anchor="w", padx=10)
    
    ctk.CTkFrame(content_frame, height=2, fg_color=DIVIDER_COLOR).pack(fill="x", pady=15)
    
    ctk.CTkButton(app, text="Learn More About Applying", font=("Helvetica", 16, "bold"), fg_color=BTN_GREEN, text_color="white", command=open_requirements).pack(pady=10, ipadx=20, ipady=5)
    
    back_link = ctk.CTkLabel(app, text="Back To Home", font=("Helvetica", 12, "bold", "underline"), text_color=TEXT_BLUE, cursor="hand2")
    back_link.pack(pady=5)
    back_link.bind("<Button-1>", lambda e: show_home())

# ==========================================
# PAGE 3: ELIGIBILITY CHECK (UPDATED 2026 LOGIC)
# ==========================================
def check_logic(age_entry, size_entry, income_entry):
    # Validation check
    if not age_entry.get().strip() or not size_entry.get().strip() or not income_entry.get().strip():
        messagebox.showwarning("Validation Error", "Please fill out all fields before checking eligibility.")
        return
    try:
        age = int(age_entry.get())
        hh_size = int(size_entry.get())
        income = float(income_entry.get())
        
        # 2026 FPL Base calculation (Annual)
        fpl_annual = 15960 + (hh_size - 1) * 5680
        
        # Determine FPL percentage based on Age
        if age <= 18:
            multiplier = 1.55 # 155% for children
        elif age <= 64:
            multiplier = 1.38 # 138% for expansion adults
        else:
            multiplier = 1.00 # Approximating standard older adult limits
            
        monthly_limit = (fpl_annual * multiplier) / 12

        if income <= monthly_limit:
            messagebox.showinfo("Result", f"Eligible! Your income is below the estimated ${monthly_limit:,.2f}/mo threshold.")
        else:
            messagebox.showwarning("Result", f"Ineligible. Your income exceeds the estimated ${monthly_limit:,.2f}/mo threshold.")
            
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

def show_eligibility():
    clear_window()
    ctk.CTkLabel(app, text="Medicaid Eligibility Check", font=("Helvetica", 24, "bold"), fg_color=HEADER_BLUE, text_color="white", corner_radius=0).pack(fill="x", ipady=15)
    
    form_frame = ctk.CTkFrame(app, fg_color="transparent")
    form_frame.pack(pady=30, padx=40, fill="x")
    form_frame.grid_columnconfigure(1, weight=1)
    
    def add_divider(row_idx):
        ctk.CTkFrame(form_frame, height=1, fg_color=DIVIDER_COLOR).grid(row=row_idx, column=0, columnspan=2, sticky="ew", pady=10)

    ctk.CTkLabel(form_frame, text="Age:", font=("Helvetica", 16)).grid(row=0, column=0, sticky="w", padx=10)
    age_entry = ctk.CTkEntry(form_frame, width=250)
    age_entry.grid(row=0, column=1, sticky="w")
    add_divider(1)
    
    ctk.CTkLabel(form_frame, text="Household Size:", font=("Helvetica", 16)).grid(row=2, column=0, sticky="w", padx=10)
    size_entry = ctk.CTkEntry(form_frame, width=250)
    size_entry.grid(row=2, column=1, sticky="w")
    add_divider(3)
    
    ctk.CTkLabel(form_frame, text="Monthly Income:", font=("Helvetica", 16)).grid(row=4, column=0, sticky="w", padx=10)
    income_entry = ctk.CTkEntry(form_frame, width=250)
    income_entry.grid(row=4, column=1, sticky="w")
    add_divider(5)
    
    ctk.CTkLabel(form_frame, text="Are You Currently Employed?", font=("Helvetica", 16)).grid(row=6, column=0, sticky="w", padx=10)
    radio_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    radio_frame.grid(row=6, column=1, sticky="w")
    emp_var = tk.IntVar(value=1)
    ctk.CTkRadioButton(radio_frame, text="Yes", variable=emp_var, value=1).pack(side="left", padx=(0, 20))
    ctk.CTkRadioButton(radio_frame, text="No", variable=emp_var, value=2).pack(side="left")
    add_divider(7)
    
    # Passing the age_entry variable into the check_logic function
    ctk.CTkButton(app, text="Check Eligibility", font=("Helvetica", 18, "bold"), fg_color=BTN_GREEN, text_color="white", command=lambda: check_logic(age_entry, size_entry, income_entry)).pack(pady=20, ipadx=30, ipady=5)
    
    back_link = ctk.CTkLabel(app, text="Back To Home", font=("Helvetica", 12, "bold", "underline"), text_color=TEXT_BLUE, cursor="hand2")
    back_link.pack()
    back_link.bind("<Button-1>", lambda e: show_home())

# ==========================================
# PAGE 4: EMPLOYMENT VERIFICATION 
# ==========================================
def upload_file(doc_entry):
    filename = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if filename:
        doc_entry.delete(0, tk.END)
        doc_entry.insert(0, filename.split("/")[-1])

def show_verification():
    clear_window()
    ctk.CTkLabel(app, text="Employment Verification Form", font=("Helvetica", 24, "bold"), fg_color=HEADER_BLUE, text_color="white", corner_radius=0).pack(fill="x", ipady=15)
    
    form_frame = ctk.CTkFrame(app, fg_color="transparent")
    form_frame.pack(pady=20, padx=40, fill="x")
    form_frame.grid_columnconfigure(1, weight=1)
    
    def add_divider(row_idx):
        ctk.CTkFrame(form_frame, height=1, fg_color=DIVIDER_COLOR).grid(row=row_idx, column=0, columnspan=3, sticky="ew", pady=10)

    ctk.CTkLabel(form_frame, text="Applicant’s Name:", font=("Helvetica", 16)).grid(row=0, column=0, sticky="w", padx=10)
    name_entry = ctk.CTkEntry(form_frame, width=350)
    name_entry.grid(row=0, column=1, columnspan=2, sticky="w")
    add_divider(1)

    ctk.CTkLabel(form_frame, text="Employer Name:", font=("Helvetica", 16)).grid(row=2, column=0, sticky="w", padx=10)
    employer_entry = ctk.CTkEntry(form_frame, width=350)
    employer_entry.grid(row=2, column=1, columnspan=2, sticky="w")
    add_divider(3)

    ctk.CTkLabel(form_frame, text="Employee ID:", font=("Helvetica", 16)).grid(row=4, column=0, sticky="w", padx=10)
    id_entry = ctk.CTkEntry(form_frame, width=350)
    id_entry.grid(row=4, column=1, columnspan=2, sticky="w")
    add_divider(5)

    ctk.CTkLabel(form_frame, text="Employment Status:", font=("Helvetica", 16)).grid(row=6, column=0, sticky="w", padx=10)
    radio_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    radio_frame.grid(row=6, column=1, columnspan=2, sticky="w")
    status_var = tk.IntVar(value=1)
    ctk.CTkRadioButton(radio_frame, text="Full-Time", variable=status_var, value=1).pack(side="left", padx=(0, 15))
    ctk.CTkRadioButton(radio_frame, text="Part-Time", variable=status_var, value=2).pack(side="left", padx=(0, 15))
    ctk.CTkRadioButton(radio_frame, text="Other", variable=status_var, value=3).pack(side="left")
    add_divider(7)

    ctk.CTkLabel(form_frame, text="Start Date:", font=("Helvetica", 16)).grid(row=8, column=0, sticky="w", padx=10, pady=5)
    start_entry = ctk.CTkEntry(form_frame, width=200)
    start_entry.grid(row=8, column=1, columnspan=2, sticky="w", pady=5)
    
    ctk.CTkLabel(form_frame, text="Hours Per Week:", font=("Helvetica", 16)).grid(row=9, column=0, sticky="w", padx=10, pady=5)
    hours_entry = ctk.CTkEntry(form_frame, width=200)
    hours_entry.grid(row=9, column=1, columnspan=2, sticky="w", pady=5)

    ctk.CTkLabel(form_frame, text="Documents:", font=("Helvetica", 16)).grid(row=10, column=0, sticky="w", padx=10, pady=5)
    
    doc_container = ctk.CTkFrame(form_frame, fg_color="transparent")
    doc_container.grid(row=10, column=1, columnspan=2, sticky="w", pady=5)
    
    doc_entry = ctk.CTkEntry(doc_container, width=200)
    doc_entry.pack(side="left", padx=(0, 10))
    
    ctk.CTkButton(doc_container, text="➕ Upload File", fg_color="#d1d5db", text_color="#374151", font=("Helvetica", 14, "bold"), width=120, command=lambda: upload_file(doc_entry)).pack(side="left")
    
    def validate_and_submit():
        if not name_entry.get().strip() or not employer_entry.get().strip() or not id_entry.get().strip() or not start_entry.get().strip() or not hours_entry.get().strip():
            messagebox.showwarning("Validation Error", "Please fill out all fields before submitting.")
            return
        
        messagebox.showinfo("Success", "Form submitted.")
        show_home()

    ctk.CTkButton(app, text="Submit Verification Form", font=("Helvetica", 18, "bold"), fg_color=BTN_GREEN, text_color="white", command=validate_and_submit).pack(pady=20, ipadx=30, ipady=5)
    
    back_link = ctk.CTkLabel(app, text="Back To Home", font=("Helvetica", 12, "bold", "underline"), text_color=TEXT_BLUE, cursor="hand2")
    back_link.pack()
    back_link.bind("<Button-1>", lambda e: show_home())

# --- APP INITIALIZATION ---
app = ctk.CTk()
app.title("Missouri Medicaid Portal")
app.geometry("800x750")

show_home()
app.mainloop()
