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
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# --- BRAND COLORS ---
HEADER_BLUE = "#5b9bd5"
BTN_GREEN = "#7dd169"
TEXT_BLUE = "#3b82f6"

def clear_window():
    """Removes all current widgets so we can load a new page."""
    for widget in app.winfo_children():
        widget.destroy()

def open_requirements(event):
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
    
    link = ctk.CTkLabel(app, text="For more info on Program Requirements, click here.", 
                        font=("Helvetica", 12, "underline"), text_color=TEXT_BLUE, cursor="hand2")
    link.pack(side="bottom", pady=30)
    link.bind("<Button-1>", open_requirements)

# ==========================================
# PAGE 2: PROGRAM REQUIREMENTS
# ==========================================
def show_requirements():
    clear_window()
    ctk.CTkLabel(app, text="Program Requirements", font=("Helvetica", 24, "bold"), 
                 fg_color=HEADER_BLUE, text_color="white", corner_radius=0).pack(fill="x", ipady=15)
    
    content_frame = ctk.CTkFrame(app, fg_color="transparent")
    content_frame.pack(pady=30, fill="x", padx=40)
    
    info_text = (
        "• Residency: Must be a current resident of Missouri.\n"
        "• Citizenship: Must be a U.S. citizen or an eligible non-citizen.\n"
        "• Expansion Adults (Age 19-64): Income <= 138% FPL.\n"
    )
    ctk.CTkLabel(content_frame, text=info_text, font=("Helvetica", 15), justify="left").pack(anchor="w")
    ctk.CTkButton(app, text="Back To Home", fg_color="gray", command=show_home).pack(pady=20)

# ==========================================
# PAGE 3: ELIGIBILITY CHECK
# ==========================================
def check_logic(size_entry, income_entry):
    try:
        hh_size = int(size_entry.get())
        income = float(income_entry.get())
        limit = (44355 + (hh_size - 4) * 7586) / 12 if hh_size > 4 else 2500 # Simplified for example
        
        if income <= limit:
            messagebox.showinfo("Result", "Eligible!")
        else:
            messagebox.showwarning("Result", "Exceeds threshold.")
    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers.")

def show_eligibility():
    clear_window()
    ctk.CTkLabel(app, text="Medicaid Eligibility Check", font=("Helvetica", 24, "bold"), 
                 fg_color=HEADER_BLUE, text_color="white").pack(fill="x", ipady=15)
    
    form_frame = ctk.CTkFrame(app, fg_color="transparent")
    form_frame.pack(pady=30)
    
    ctk.CTkLabel(form_frame, text="Household Size:").grid(row=0, column=0, padx=10, pady=10)
    size_entry = ctk.CTkEntry(form_frame)
    size_entry.grid(row=0, column=1)
    
    ctk.CTkLabel(form_frame, text="Monthly Income:").grid(row=1, column=0, padx=10, pady=10)
    income_entry = ctk.CTkEntry(form_frame)
    income_entry.grid(row=1, column=1)
    
    ctk.CTkButton(app, text="Check Eligibility", fg_color=BTN_GREEN, 
                  command=lambda: check_logic(size_entry, income_entry)).pack(pady=20)
    ctk.CTkButton(app, text="Back To Home", command=show_home).pack()

# ==========================================
# PAGE 4: EMPLOYMENT VERIFICATION (UPDATED LAYOUT & VALIDATION)
# ==========================================
def upload_file(doc_entry):
    filename = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if filename:
        doc_entry.delete(0, tk.END)
        doc_entry.insert(0, filename.split("/")[-1])

def submit_verification(app_name_entry, emp_name_entry, emp_id_entry, start_date_entry, hours_entry):
    """Validates the input fields before allowing the user to submit."""
    # .get() pulls the text, and .strip() removes any accidental spaces the user typed
    app_name = app_name_entry.get().strip()
    emp_name = emp_name_entry.get().strip()
    emp_id = emp_id_entry.get().strip()
    start_date = start_date_entry.get().strip()
    hours = hours_entry.get().strip()
    
    # Check if any of the fields are completely empty
    if not app_name or not emp_name or not emp_id or not start_date or not hours:
        messagebox.showwarning("Missing Information", "Please fill out all required fields before submitting.")
        return # Stops the function right here so it doesn't show the success message

    # If it passes the check above, show success and go home
    messagebox.showinfo("Success", "Form submitted for review.")
    show_home()

def show_verification():
    clear_window()
    ctk.CTkLabel(app, text="Employment Verification Form", font=("Helvetica", 24, "bold"), 
                 fg_color=HEADER_BLUE, text_color="white").pack(fill="x", ipady=15)
    
    form_frame = ctk.CTkFrame(app, fg_color="transparent")
    form_frame.pack(pady=20)
    
    # Explicitly creating and saving references to the entry boxes
    # Row 0: Applicant's Name
    ctk.CTkLabel(form_frame, text="Applicant's Name:").grid(row=0, column=0, sticky="w", pady=10, padx=10)
    app_name_entry = ctk.CTkEntry(form_frame, width=300)
    app_name_entry.grid(row=0, column=1, columnspan=2, pady=10, sticky="w")

    # Row 1: Employer Name
    ctk.CTkLabel(form_frame, text="Employer Name:").grid(row=1, column=0, sticky="w", pady=10, padx=10)
    emp_name_entry = ctk.CTkEntry(form_frame, width=300)
    emp_name_entry.grid(row=1, column=1, columnspan=2, pady=10, sticky="w")

    # Row 2: Employee ID
    ctk.CTkLabel(form_frame, text="Employee ID:").grid(row=2, column=0, sticky="w", pady=10, padx=10)
    emp_id_entry = ctk.CTkEntry(form_frame, width=300)
    emp_id_entry.grid(row=2, column=1, columnspan=2, pady=10, sticky="w")
    
    # Row 3: Status
    ctk.CTkLabel(form_frame, text="Employment Status:").grid(row=3, column=0, sticky="w", padx=10)
    # ... (Radio buttons can be added here)

    # Row 4: Start Date
    ctk.CTkLabel(form_frame, text="Start Date:").grid(row=4, column=0, sticky="w", pady=10, padx=10)
    start_date_entry = ctk.CTkEntry(form_frame, width=150)
    start_date_entry.grid(row=4, column=1, sticky="w")
    
    # Row 5: Hours Per Week
    ctk.CTkLabel(form_frame, text="Hours Per Week:").grid(row=5, column=0, sticky="w", pady=10, padx=10)
    hours_entry = ctk.CTkEntry(form_frame, width=150)
    hours_entry.grid(row=5, column=1, sticky="w")

    # Row 6: Documents & Upload Button (Aligned horizontally)
    ctk.CTkLabel(form_frame, text="Documents:").grid(row=6, column=0, sticky="w", pady=10, padx=10)
    doc_entry = ctk.CTkEntry(form_frame, width=150)
    doc_entry.grid(row=6, column=1, sticky="w")
    ctk.CTkButton(form_frame, text="➕ Upload File", width=120, fg_color="gray", 
                  command=lambda: upload_file(doc_entry)).grid(row=6, column=2, padx=10)
    
    # Passing the variables using a lambda function
    ctk.CTkButton(app, text="Submit Verification Form", fg_color=BTN_GREEN, 
                  command=lambda: submit_verification(app_name_entry, emp_name_entry, emp_id_entry, start_date_entry, hours_entry)).pack(pady=20)
    
    ctk.CTkButton(app, text="Back To Home", command=show_home).pack()

# --- APP INITIALIZATION ---
app = ctk.CTk()
app.title("Missouri Medicaid Portal")
app.geometry("800x750")

# Start the app
show_home()
app.mainloop()