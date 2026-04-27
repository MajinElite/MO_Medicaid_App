# Front_end/caseworker_view_popup.py

import customtkinter as ctk
from datetime import datetime
import base64
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk
import io

# ================= CASEWORKER THEME =================
HEADER_ORANGE = "#f97316"
HEADER_ORANGE_HOVER = "#ea580c"
SECTION_ORANGE = "#c2410c"

CARD_BG = "#2b2b2b"
BODY_BG = "#343638"
ROW_BG = "#2f3133"
TEXT_MUTED = "#b0b0b0"

BTN_BLUE = "#17a2b8"


def format_datetime(dt_string):
    try:
        dt = datetime.fromisoformat(dt_string)
        return dt.strftime("%B %d, %Y  %I:%M %p")
    except Exception:
        return dt_string if dt_string else "Not Available"


def safe_value(value):
    if value is None or value == "":
        return "Not Provided"
    return str(value)


def open_view_popup(parent, app_data: dict):
    popup = ctk.CTkToplevel(parent)
    popup.title("Application Details")
    popup.geometry("760x720")
    popup.configure(fg_color=BODY_BG)
    popup.grab_set()

    # ================= HEADER =================
    ctk.CTkLabel(
        popup,
        text="Full Application Details",
        font=("Helvetica", 22, "bold"),
        fg_color=HEADER_ORANGE,
        text_color="white"
    ).pack(fill="x", ipady=14)

    ctk.CTkLabel(
        popup,
        text="Review applicant information, employment details, uploaded documents, and caseworker notes.",
        font=("Helvetica", 13),
        text_color=TEXT_MUTED,
        wraplength=680,
        justify="center"
    ).pack(pady=(12, 5))

    box = ctk.CTkScrollableFrame(popup, fg_color=BODY_BG)
    box.pack(fill="both", expand=True, padx=18, pady=10)

    # ================= HELPERS =================
    def section(title):
        frame = ctk.CTkFrame(box, fg_color=CARD_BG, corner_radius=10)
        frame.pack(fill="x", pady=10)

        header = ctk.CTkFrame(frame, fg_color=SECTION_ORANGE, corner_radius=8)
        header.pack(fill="x")

        ctk.CTkLabel(
            header,
            text=title,
            font=("Helvetica", 15, "bold"),
            text_color="white"
        ).pack(anchor="w", padx=14, pady=8)

        body = ctk.CTkFrame(frame, fg_color=CARD_BG)
        body.pack(fill="x", padx=12, pady=12)

        return body

    def add_row(parent_frame, label, value):
        row = ctk.CTkFrame(parent_frame, fg_color=ROW_BG, corner_radius=6)
        row.pack(fill="x", pady=4)

        ctk.CTkLabel(
            row,
            text=label,
            width=190,
            anchor="w",
            font=("Helvetica", 12, "bold"),
            text_color="white"
        ).pack(side="left", padx=(12, 8), pady=8)

        ctk.CTkLabel(
            row,
            text=safe_value(value),
            anchor="w",
            font=("Helvetica", 12),
            text_color="white",
            wraplength=430,
            justify="left"
        ).pack(side="left", padx=(0, 12), pady=8, fill="x", expand=True)

    def download_file(file_name, file_data, success_message="File downloaded successfully."):
        try:
            file_bytes = base64.b64decode(file_data)

            ext = ""
            if "." in file_name:
                ext = file_name.split(".")[-1]

            save_path = filedialog.asksaveasfilename(
                defaultextension=f".{ext}" if ext else "",
                initialfile=file_name,
                filetypes=[
                    ("PDF files", "*.pdf"),
                    ("Image files", "*.png *.jpg *.jpeg"),
                    ("All files", "*.*")
                ]
            )

            if not save_path:
                return

            if ext and not save_path.lower().endswith(f".{ext}"):
                save_path += f".{ext}"

            with open(save_path, "wb") as f:
                f.write(file_bytes)

            messagebox.showinfo("Download Complete", success_message)

        except Exception as e:
            messagebox.showerror(
                "Download Failed",
                f"The file could not be downloaded.\n\nDetails: {e}"
            )

    # ================= BASIC INFO =================
    basic = section("Application Summary")

    add_row(basic, "Application ID:", app_data.get("app_id", ""))
    add_row(basic, "Applicant Email:", app_data.get("applicant_email", ""))
    add_row(basic, "Status:", app_data.get("status", ""))
    add_row(basic, "Created:", format_datetime(app_data.get("created_at", "")))
    add_row(basic, "Updated:", format_datetime(app_data.get("updated_at", "")))

    deny_reason = app_data.get("deny_reason", "")
    request_reason = app_data.get("request_reason", "")

    if deny_reason:
        add_row(basic, "Decision Reason:", deny_reason)

    if request_reason:
        add_row(basic, "Information Request:", request_reason)

    # ================= FORM =================
    form = app_data.get("form", {}) if isinstance(app_data.get("form"), dict) else {}

    employment = section("Employment Details")

    add_row(employment, "Applicant Name:", form.get("applicant_name", ""))
    add_row(employment, "Employer Name:", form.get("employer_name", ""))
    add_row(employment, "Employee ID:", form.get("employee_id", ""))
    add_row(employment, "Employment Status:", form.get("employment_status", ""))
    add_row(employment, "Start Date:", form.get("start_date", ""))
    add_row(employment, "Hours Per Week:", form.get("hours_per_week", ""))
    add_row(employment, "Monthly Gross Income:", form.get("monthly_income", ""))
    add_row(employment, "Additional Information:", form.get("additional_information", ""))

    # ================= EXEMPTION =================
    exemption = section("Exemption Request")

    exemption_requested = form.get("exemption_requested", "No")
    add_row(exemption, "Requested:", exemption_requested)

    if exemption_requested == "Yes":
        add_row(exemption, "Reason:", form.get("exemption_reason", ""))

    # ================= APPLICANT DOCUMENT =================
    document = section("Applicant Uploaded Document")

    document_name = form.get("document_name", "")
    document_data = form.get("document_data_base64", "")

    if document_name and document_data:
        add_row(document, "File Name:", document_name)
        add_row(document, "Document Status:", "Document Uploaded")

        try:
            file_bytes = base64.b64decode(document_data)

            image = Image.open(io.BytesIO(file_bytes))
            image.thumbnail((420, 420))

            tk_image = ImageTk.PhotoImage(image)

            img_label = ctk.CTkLabel(document, image=tk_image, text="")
            img_label.image = tk_image
            img_label.pack(pady=10)

        except Exception:
            ctk.CTkButton(
                document,
                text=f"Download Document: {document_name}",
                fg_color=BTN_BLUE,
                command=lambda: download_file(
                    document_name,
                    document_data,
                    "Applicant document downloaded successfully."
                )
            ).pack(pady=10)

    else:
        add_row(document, "Document Status:", "No document uploaded.")

    # ================= CASEWORKER REQUEST FILE =================
    request_file_name = form.get("request_file_name", "")
    request_file_data = form.get("request_file_data_base64", "")

    if request_file_name and request_file_data:
        request_file = section("Requested Information Attachment")

        add_row(request_file, "File Name:", request_file_name)
        add_row(request_file, "Attachment Status:", "Caseworker request attachment available.")

        ctk.CTkButton(
            request_file,
            text=f"Download Request File: {request_file_name}",
            fg_color=BTN_BLUE,
            command=lambda: download_file(
                request_file_name,
                request_file_data,
                "Request attachment downloaded successfully."
            )
        ).pack(pady=10)

    # ================= CLOSE =================
    ctk.CTkButton(
        popup,
        text="Close",
        fg_color="gray",
        hover_color="#666666",
        width=150,
        command=popup.destroy
    ).pack(pady=15)