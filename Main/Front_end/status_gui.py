# Front_end/status_gui.py

import customtkinter as ctk

HEADER_BLUE = "#5b9bd5"
BTN_GREEN = "#7dd169"

try:
    from Back_end.application_logic import get_application_status
except Exception:
    def get_application_status(user):
        return {"status": "None", "reason": ""}


class StatusScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # ================= HEADER =================
        ctk.CTkLabel(
            self,
            text="Application Status",
            font=("Helvetica", 24, "bold"),
            fg_color=HEADER_BLUE,
            text_color="white"
        ).pack(fill="x", ipady=15)

        # ================= CONTEXT =================
        context_frame = ctk.CTkFrame(self, corner_radius=10)
        context_frame.pack(pady=20, padx=40, fill="x")

        ctk.CTkLabel(
            context_frame,
            text=(
                "This page shows the current status of your submitted application.\n"
                "Updates occur after caseworker review."
            ),
            font=("Helvetica", 13),
            justify="center"
        ).pack(pady=15)

        # ================= STATUS CARD =================
        self.status_card = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.status_card.pack(pady=10, padx=60, fill="x")

        self.status_label = ctk.CTkLabel(
            self.status_card,
            text="",
            font=("Helvetica", 18, "bold"),
            text_color="white",
            wraplength=600,
            justify="center"
        )
        self.status_label.pack(pady=15)

        # ================= REASON =================
        self.reason_frame = ctk.CTkFrame(self, corner_radius=10)

        self.reason_label_title = ctk.CTkLabel(
            self.reason_frame,
            text="",
            font=("Helvetica", 14, "bold")
        )

        self.reason_label = ctk.CTkLabel(
            self.reason_frame,
            text="",
            font=("Helvetica", 13),
            wraplength=600,
            justify="center"
        )

        # ================= BUTTONS =================
        ctk.CTkButton(
            self,
            text="Refresh",
            fg_color=BTN_GREEN,
            command=self.refresh
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Back",
            fg_color="gray",
            command=controller.show_applicant_dashboard
        ).pack(pady=5)

        self.refresh()

    # ================= STATUS LOGIC =================
    def refresh(self):
        user = self.controller.current_user
        info = get_application_status(user)

        status = info.get("status", "None")
        reason = info.get("reason", "")
        file_name = info.get("request_file_name", "")
        file_data = info.get("request_file_data_base64", "")

        self.reason_frame.pack_forget()

        # ================= NONE =================
        if status == "None":
            self.status_card.configure(fg_color="#6c757d")
            self.status_label.configure(
                text="No Application Submitted\nYou have not submitted an application yet."
            )

        # ================= PENDING =================
        elif status in ["Pending", "Under Review", "Exemption Pending"]:
            self.status_card.configure(fg_color="#f0ad4e")
            self.status_label.configure(
                text=(
                    "Status: Pending Review \n"
                    "Your application has been submitted and is waiting for a caseworker to review it."
                )
            )

        # ================= MORE INFO =================
        elif status == "More Info Required":
            self.status_card.configure(fg_color="#17a2b8")
            self.status_label.configure(
                text=(
                    "Status: More Information Required (Blue)\n"
                    "A caseworker needs additional information to continue your review."
                )
            )

            self.reason_frame.pack(pady=15, padx=60, fill="x")

            self.reason_label_title.configure(text="Caseworker Notes")
            self.reason_label_title.pack(pady=(10, 5))

            self.reason_label.pack(pady=(0, 10))
            self.reason_label.configure(
                text=reason if reason else "Please provide the requested information."
            )

            # File download
            if file_name and file_data:
                import base64
                from tkinter import filedialog, messagebox

                def download_file():
                    try:
                        file_bytes = base64.b64decode(file_data)

                        save_path = filedialog.asksaveasfilename(
                            initialfile=file_name
                        )

                        if not save_path:
                            return

                        with open(save_path, "wb") as f:
                            f.write(file_bytes)

                        messagebox.showinfo("Download Complete", "File downloaded successfully.")

                    except Exception as e:
                        messagebox.showerror("Error", str(e))

                ctk.CTkButton(
                    self.reason_frame,
                    text=f"Download Attachment: {file_name}",
                    command=download_file
                ).pack(pady=(0, 15))

        # ================= APPROVED =================
        elif status == "Approved":
            self.status_card.configure(fg_color="#3cb371")
            self.status_label.configure(
                text=(
                    "Status: Approved \n"
                    "Your application has been approved based on the information provided."
                )
            )

        # ================= DENIED =================
        elif status == "Denied":
            self.status_card.configure(fg_color="#dc3545")
            self.status_label.configure(
                text=(
                    "Status: Denied \n"
                    "Your application was not approved based on the submitted information."
                )
            )

            self.reason_frame.pack(pady=15, padx=60, fill="x")

            self.reason_label_title.configure(text="Reason for Decision")
            self.reason_label_title.pack(pady=(10, 5))

            self.reason_label.pack(pady=(0, 15))
            self.reason_label.configure(
                text=reason if reason else "No specific reason was provided."
            )

        # ================= DEFAULT =================
        else:
            self.status_card.configure(fg_color="#6c757d")
            self.status_label.configure(text=f"Status: {status}")