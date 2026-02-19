'''
DEVELOPER: Duy Huynh
TASK: Sprint 2
STORIES: Home, Requirements, Eligibility Check, & Employment Verification

'''

import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser

# --- COLORS & FONTS TO MATCH MOCKUPS ---
BG_COLOR = "#ffffff"
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
    
    # Blue Header
    tk.Label(app, text="Missouri Medicaid", font=("Helvetica", 24, "bold"), bg=HEADER_BLUE, fg="white", pady=15).pack(fill="x")
    tk.Label(app, text="Welcome to the Medicaid Portal", font=("Helvetica", 18), bg=BG_COLOR, pady=20).pack()
    
    # Navigation Buttons
    req_btn = tk.Button(app, text="Review Program Requirements", font=("Helvetica", 14, "bold"), bg=BTN_GREEN, fg="white", relief="flat", command=show_requirements)
    req_btn.pack(pady=10, ipadx=20, ipady=10)
    
    elig_btn = tk.Button(app, text="Check Medicaid Eligibility", font=("Helvetica", 14, "bold"), bg=BTN_GREEN, fg="white", relief="flat", command=show_eligibility)
    elig_btn.pack(pady=10, ipadx=20, ipady=10)
    
    verif_btn = tk.Button(app, text="Submit Employment Verification", font=("Helvetica", 14, "bold"), bg=BTN_GREEN, fg="white", relief="flat", command=show_verification)
    verif_btn.pack(pady=10, ipadx=20, ipady=10)

# ==========================================
# PAGE 2: PROGRAM REQUIREMENTS
# ==========================================
def show_requirements():
    clear_window()
    
    tk.Label(app, text="Program Requirements", font=("Helvetica", 24, "bold"), bg=HEADER_BLUE, fg="white", pady=15).pack(fill="x")
    
    content_frame = tk.Frame(app, bg=BG_COLOR)
    content_frame.pack(pady=20, fill="x", padx=40)
    
    # Factual Missouri Medicaid text pulled from search
    info_text = (
        "To qualify for Missouri Medicaid (MO HealthNet), applicants generally must meet the following criteria:\n\n"
        "• Residency: Must be a current resident of Missouri.\n"
        "• Citizenship: Must be a U.S. citizen or an eligible non-citizen.\n"
        "• Expansion Adults (Age 19-64): Income must be at or below 138% of the Federal Poverty Level.\n"
        "• Children & Pregnant Women: Eligible at higher income thresholds (up to 305% FPL for children).\n"
        "• Seniors & Disabled: Additional asset and resource limits may apply.\n\n"
        "Eligibility is based on your specific household size and total monthly income."
    )
    
    # Wraplength ensures the text doesn't run off the sides of the window
    tk.Label(content_frame, text=info_text, font=("Helvetica", 14), bg=BG_COLOR, justify="left", wraplength=700).pack(anchor="w")
    
    # Navigation back to home
    tk.Button(app, text="Back To Home", font=("Helvetica", 12, "bold"), bg="#e0e0e0", relief="raised", command=show_home).pack(pady=20, ipadx=20, ipady=5)
    
    # The clickable link moved to the bottom of this page
    link = tk.Label(app, text="For more info on Program Requirements, click here.", font=("Helvetica", 12, "underline"), fg=TEXT_BLUE, bg=BG_COLOR, cursor="hand2")
    link.pack(side="bottom", pady=30)
    link.bind("<Button-1>", open_requirements)

# ==========================================
# PAGE 3: ELIGIBILITY CHECK
# ==========================================
def check_logic(size_entry, income_entry):
    """Calculates eligibility based on actual 2026 MO 138% FPG Limits."""
    try:
        hh_size = int(size_entry.get())
        income = float(income_entry.get())
        
        # Real 2026 Missouri 138% FPG Limits (Annual divided by 12 for monthly)
        thresholds = {
            1: 21597 / 12,
            2: 29183 / 12,
            3: 36769 / 12,
            4: 44355 / 12
        }
        
        limit = thresholds.get(hh_size, (44355 + (hh_size - 4) * 7586) / 12)
        
        if income <= limit:
            messagebox.showinfo("Result", f"Eligible! Your income is below the ${limit:,.2f}/mo threshold.")
        else:
            messagebox.showwarning("Result", f"Your income exceeds the ${limit:,.2f}/mo threshold.")
            
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

def show_eligibility():
    clear_window()
    
    tk.Label(app, text="Medicaid Eligibility Check", font=("Helvetica", 24, "bold"), bg=HEADER_BLUE, fg="white", pady=15).pack(fill="x")
    
    form_frame = tk.Frame(app, bg=BG_COLOR)
    form_frame.pack(pady=30)
    
    tk.Label(form_frame, text="Age:", font=("Helvetica", 14), bg=BG_COLOR).grid(row=0, column=0, sticky="w", pady=10, padx=10)
    tk.Entry(form_frame, font=("Helvetica", 14), width=20).grid(row=0, column=1, pady=10)
    
    tk.Label(form_frame, text="Household Size:", font=("Helvetica", 14), bg=BG_COLOR).grid(row=1, column=0, sticky="w", pady=10, padx=10)
    size_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=20)
    size_entry.grid(row=1, column=1, pady=10)
    
    tk.Label(form_frame, text="Monthly Income:", font=("Helvetica", 14), bg=BG_COLOR).grid(row=2, column=0, sticky="w", pady=10, padx=10)
    income_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=20)
    income_entry.grid(row=2, column=1, pady=10)
    
    tk.Label(form_frame, text="Are You Currently Employed?", font=("Helvetica", 14), bg=BG_COLOR).grid(row=3, column=0, sticky="w", pady=10, padx=10)
    radio_frame = tk.Frame(form_frame, bg=BG_COLOR)
    radio_frame.grid(row=3, column=1, sticky="w")
    
    employed_var = tk.IntVar(value=2)
    tk.Radiobutton(radio_frame, text="Yes", variable=employed_var, value=1, font=("Helvetica", 12), bg=BG_COLOR).pack(side="left", padx=5)
    tk.Radiobutton(radio_frame, text="No", variable=employed_var, value=2, font=("Helvetica", 12), bg=BG_COLOR).pack(side="left", padx=5)
    
    tk.Button(app, text="Check Eligibility", font=("Helvetica", 16, "bold"), bg=BTN_GREEN, fg="white", relief="flat", command=lambda: check_logic(size_entry, income_entry)).pack(pady=20, ipadx=40, ipady=5)
    tk.Button(app, text="Back To Home", font=("Helvetica", 10, "underline"), fg=TEXT_BLUE, bg=BG_COLOR, relief="flat", command=show_home).pack()

# ==========================================
# PAGE 4: EMPLOYMENT VERIFICATION
# ==========================================
def upload_file(doc_entry):
    filename = filedialog.askopenfilename(
        title="Select a Document",
        filetypes=[("PDF Documents", "*.pdf"), ("Image Files", "*.jpg;*.jpeg;*.png"), ("All Files", "*.*")]
    )
    if filename:
        doc_entry.delete(0, tk.END)
        doc_entry.insert(0, filename.split("/")[-1])

def submit_verification():
    messagebox.showinfo("Success", "Employment Verification Form has been submitted for review.")
    show_home()

def show_verification():
    clear_window()
    
    tk.Label(app, text="Employment Verification Form", font=("Helvetica", 24, "bold"), bg=HEADER_BLUE, fg="white", pady=15).pack(fill="x")
    
    form_frame = tk.Frame(app, bg=BG_COLOR)
    form_frame.pack(pady=20)
    
    fields = ["Applicant's Name:", "Employer Name:", "Employee ID:"]
    for i, field in enumerate(fields):
        tk.Label(form_frame, text=field, font=("Helvetica", 14), bg=BG_COLOR).grid(row=i, column=0, sticky="w", pady=10, padx=10)
        tk.Entry(form_frame, font=("Helvetica", 14), width=30).grid(row=i, column=1, pady=10, sticky="w")
    
    tk.Label(form_frame, text="Employment Status:", font=("Helvetica", 14), bg=BG_COLOR).grid(row=3, column=0, sticky="w", pady=10, padx=10)
    radio_frame = tk.Frame(form_frame, bg=BG_COLOR)
    radio_frame.grid(row=3, column=1, sticky="w")
    
    status_var = tk.IntVar(value=1)
    tk.Radiobutton(radio_frame, text="Full-Time", variable=status_var, value=1, font=("Helvetica", 12), bg=BG_COLOR).pack(side="left")
    tk.Radiobutton(radio_frame, text="Part-Time", variable=status_var, value=2, font=("Helvetica", 12), bg=BG_COLOR).pack(side="left")
    tk.Radiobutton(radio_frame, text="Other", variable=status_var, value=3, font=("Helvetica", 12), bg=BG_COLOR).pack(side="left")

    tk.Label(form_frame, text="Start Date:", font=("Helvetica", 14), bg=BG_COLOR).grid(row=4, column=0, sticky="w", pady=10, padx=10)
    tk.Entry(form_frame, font=("Helvetica", 14), width=15).grid(row=4, column=1, sticky="w", pady=10)
    
    right_col = tk.Frame(form_frame, bg=BG_COLOR)
    right_col.grid(row=4, column=1, rowspan=2, sticky="e", padx=20)
    tk.Label(right_col, text="Hours Per Week:", font=("Helvetica", 12), bg=BG_COLOR).pack(anchor="w")
    
    tk.Label(form_frame, text="Documents:", font=("Helvetica", 14), bg=BG_COLOR).grid(row=5, column=0, sticky="w", pady=10, padx=10)
    doc_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=15)
    doc_entry.grid(row=5, column=1, sticky="w", pady=10)
    
    tk.Button(right_col, text="➕ Upload File", font=("Helvetica", 10, "bold"), bg="#e0e0e0", relief="raised", command=lambda: upload_file(doc_entry)).pack(pady=5)
    
    tk.Button(app, text="Submit Verification Form", font=("Helvetica", 16, "bold"), bg=BTN_GREEN, fg="white", relief="flat", command=submit_verification).pack(pady=20, ipadx=40, ipady=5)
    tk.Button(app, text="Back To Home", font=("Helvetica", 10, "underline"), fg=TEXT_BLUE, bg=BG_COLOR, relief="flat", command=show_home).pack()

# --- APP INITIALIZATION ---
app = tk.Tk()
app.title("Missouri Medicaid Portal")
app.geometry("800x650")
app.configure(bg=BG_COLOR)

# Start the app
show_home()
app.mainloop()