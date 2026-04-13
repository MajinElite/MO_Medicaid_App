# Front_end/caseworker_view_popup.py

import customtkinter as ctk
from datetime import datetime
import base64
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk
import io


def format_datetime(dt_string):
    try:
        dt = datetime.fromisoformat(dt_string)
        return dt.strftime("%B %d, %Y  %I:%M %p")
    except Exception:
        return dt_string


def open_view_popup(parent, app_data: dict):

    popup = ctk.CTkToplevel(parent)
    popup.title("Application Details")
    popup.geometry("650x650")

    ctk.CTkLabel(
        popup,
        text="Full Application Details",
        font=("Helvetica", 20, "bold")
    ).pack(pady=15)

    box = ctk.CTkScrollableFrame(popup)
    box.pack(fill="both", expand=True, padx=15, pady=10)

    def add_row(label, value):
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", pady=4)

        ctk.CTkLabel(
            row,
            text=label,
            width=170,
            anchor="w",
            font=("Helvetica", 12, "bold")
        ).pack(side="left")

        ctk.CTkLabel(
            row,
            text=str(value),
            anchor="w"
        ).pack(side="left")

    # ================= BASIC INFO =================
    add_row("Application ID:", app_data.get("app_id", ""))
    add_row("Applicant Email:", app_data.get("applicant_email", ""))
    add_row("Status:", app_data.get("status", ""))
    add_row("Created:", format_datetime(app_data.get("created_at", "")))
    add_row("Updated:", format_datetime(app_data.get("updated_at", "")))

    if app_data.get("deny_reason"):
        add_row("Reason / Notes:", app_data.get("deny_reason"))

    # ================= FORM =================
    form = app_data.get("form", {})

    ctk.CTkLabel(
        box,
        text="Employment Details",
        font=("Helvetica", 16, "bold")
    ).pack(anchor="w", pady=(15, 5))

    add_row("Applicant Name:", form.get("applicant_name", ""))
    add_row("Employer Name:", form.get("employer_name", ""))
    add_row("Employee ID:", form.get("employee_id", ""))
    add_row("Employment Status:", form.get("employment_status", ""))
    add_row("Start Date:", form.get("start_date", ""))
    add_row("Hours Per Week:", form.get("hours_per_week", ""))
    add_row("Monthly Income:", form.get("monthly_income", ""))

    # ================= EXEMPTION =================
    ctk.CTkLabel(
        box,
        text="Exemption Request",
        font=("Helvetica", 16, "bold")
    ).pack(anchor="w", pady=(15, 5))

    add_row("Requested:", form.get("exemption_requested", "No"))

    if form.get("exemption_requested") == "Yes":
        add_row("Reason:", form.get("exemption_reason", ""))

    # ================= APPLICANT DOCUMENT =================
    document_name = form.get("document_name", "")
    document_data = form.get("document_data_base64", "")

    ctk.CTkLabel(
        box,
        text="Applicant Uploaded Document",
        font=("Helvetica", 16, "bold")
    ).pack(anchor="w", pady=(15, 5))

    if document_name and document_data:
        try:
            file_bytes = base64.b64decode(document_data)

            image = Image.open(io.BytesIO(file_bytes))
            image.thumbnail((400, 400))

            tk_image = ImageTk.PhotoImage(image)

            img_label = ctk.CTkLabel(box, image=tk_image, text="")
            img_label.image = tk_image
            img_label.pack(pady=10)

        except Exception:
            def download_document():
                try:
                    file_bytes = base64.b64decode(document_data)

                    ext = ""
                    if "." in document_name:
                        ext = document_name.split(".")[-1]

                    save_path = filedialog.asksaveasfilename(
                        defaultextension=f".{ext}" if ext else "",
                        initialfile=document_name,
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

                    messagebox.showinfo("Success", "Document downloaded.")

                except Exception as e:
                    messagebox.showerror("Error", str(e))

            ctk.CTkButton(
                box,
                text=f"Download: {document_name}",
                command=download_document
            ).pack(pady=10)

    else:
        ctk.CTkLabel(box, text="No document uploaded.", text_color="gray").pack(pady=10)

    # ================= CASEWORKER REQUEST FILE =================
    request_file_name = form.get("request_file_name", "")
    request_file_data = form.get("request_file_data_base64", "")

    if request_file_name and request_file_data:

        ctk.CTkLabel(
            box,
            text="Requested Information Attachment",
            font=("Helvetica", 16, "bold")
        ).pack(anchor="w", pady=(15, 5))

        def download_request_file():
            try:
                file_bytes = base64.b64decode(request_file_data)

                ext = ""
                if "." in request_file_name:
                    ext = request_file_name.split(".")[-1]

                save_path = filedialog.asksaveasfilename(
                    defaultextension=f".{ext}" if ext else "",
                    initialfile=request_file_name
                )

                if not save_path:
                    return

                if ext and not save_path.lower().endswith(f".{ext}"):
                    save_path += f".{ext}"

                with open(save_path, "wb") as f:
                    f.write(file_bytes)

                messagebox.showinfo("Success", "File downloaded.")

            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(
            box,
            text=f"Download Request File: {request_file_name}",
            command=download_request_file
        ).pack(pady=10)

    # ================= CLOSE =================
    ctk.CTkButton(
        popup,
        text="Close",
        fg_color="gray",
        command=popup.destroy
    ).pack(pady=15)