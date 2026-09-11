import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

from models.submission import Submission
from utils.image_handler import ImageHandler


class SubmitNotice(ctk.CTkFrame):

    def __init__(self, parent, back_to_board):

        super().__init__(parent)

        self.back_to_board = back_to_board
        self.selected_image = None

        self.configure(
            fg_color="#E8D5B7"
        )

        self.create_interface()

    # =====================================================
    # INTERFACE
    # =====================================================

    def create_interface(self):

        # HEADER

        header = ctk.CTkFrame(
            self,
            height=75,
            corner_radius=0,
            fg_color="#3B2415"
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="📌 Campus Notice Submission",
            font=("Georgia", 24, "bold"),
            text_color="#FFF4D6"
        )

        title.pack(
            side="left",
            padx=25
        )

        back_button = ctk.CTkButton(
            header,
            text="← Notice Board",
            command=self.back_to_board
        )

        back_button.pack(
            side="right",
            padx=25
        )

        # MAIN AREA

        content = ctk.CTkScrollableFrame(
            self,
            fg_color="#E8D5B7"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=30
        )

        # =================================================
        # TITLE
        # =================================================

        title_label = ctk.CTkLabel(
            content,
            text="Notice Title",
            font=("Arial", 16, "bold"),
            text_color="#3B2415"
        )

        title_label.pack(
            pady=(10, 5)
        )

        self.title_entry = ctk.CTkEntry(
            content,
            width=500,
            height=42,
            placeholder_text="Example: Coding Club Meetup"
        )

        self.title_entry.pack()

        # =================================================
        # DESCRIPTION
        # =================================================

        description_label = ctk.CTkLabel(
            content,
            text="Description",
            font=("Arial", 16, "bold"),
            text_color="#3B2415"
        )

        description_label.pack(
            pady=(20, 5)
        )

        self.description_entry = ctk.CTkTextbox(
            content,
            width=500,
            height=130
        )

        self.description_entry.pack()

        # =================================================
        # SUBMITTER NAME
        # =================================================

        name_label = ctk.CTkLabel(
            content,
            text="Your Name / Club Name",
            font=("Arial", 16, "bold"),
            text_color="#3B2415"
        )

        name_label.pack(
            pady=(20, 5)
        )

        self.name_entry = ctk.CTkEntry(
            content,
            width=500,
            height=42,
            placeholder_text="Example: Ram Sharma / Coding Club"
        )

        self.name_entry.pack()

        # =================================================
        # SUBMITTER TYPE
        # =================================================

        type_label = ctk.CTkLabel(
            content,
            text="Submitting As",
            font=("Arial", 16, "bold"),
            text_color="#3B2415"
        )

        type_label.pack(
            pady=(20, 5)
        )

        self.submitter_type = ctk.CTkOptionMenu(
            content,
            width=300,
            height=40,
            values=[
                "student",
                "club",
                "teacher",
                "other"
            ]
        )

        self.submitter_type.pack()

        # =================================================
        # ATTACH IMAGE
        # =================================================

        attach_button = ctk.CTkButton(
            content,
            text="🖼️ Attach Notice Image",
            width=300,
            height=50,
            font=("Arial", 15, "bold"),
            command=self.choose_image
        )

        attach_button.pack(
            pady=(25, 10)
        )

        self.file_label = ctk.CTkLabel(
            content,
            text="No image selected",
            font=("Arial", 12),
            text_color="#765432"
        )

        self.file_label.pack()

        # =================================================
        # SUBMIT
        # =================================================

        submit_button = ctk.CTkButton(
            content,
            text="📤 SUBMIT FOR ADMIN REVIEW",
            width=350,
            height=55,
            font=("Arial", 16, "bold"),
            command=self.submit_notice
        )

        submit_button.pack(
            pady=30
        )

        # =================================================
        # INFORMATION
        # =================================================

        info = ctk.CTkLabel(
            content,
            text=(
                "ℹ Your notice will not appear immediately.\n"
                "An administrator must approve it first."
            ),
            font=("Arial", 12),
            text_color="#765432",
            justify="center"
        )

        info.pack(
            pady=(0, 20)
        )

    # =====================================================
    # CHOOSE IMAGE
    # =====================================================

    def choose_image(self):

        file_path = filedialog.askopenfilename(
            parent=self,
            title="Choose Notice Image",
            initialdir=os.path.expanduser("~/Downloads"),
            filetypes=[
                (
                    "Notice Images",
                    "*.jpg *.jpeg *.png *.webp"
                ),
                (
                    "All Files",
                    "*.*"
                )
            ]
        )

        if not file_path:
            return

        self.selected_image = file_path

        self.file_label.configure(
            text=(
                "Selected: "
                + os.path.basename(file_path)
            )
        )

    # =====================================================
    # SUBMIT NOTICE
    # =====================================================

    def submit_notice(self):

        title = self.title_entry.get().strip()

        description = (
            self.description_entry
            .get("1.0", "end")
            .strip()
        )

        submitted_by = (
            self.name_entry
            .get()
            .strip()
        )

        submitter_type = (
            self.submitter_type
            .get()
        )

        # =================================================
        # VALIDATION
        # =================================================

        if not title:

            messagebox.showwarning(
                "Missing Title",
                "Please enter a notice title.",
                parent=self
            )

            return

        if not submitted_by:

            messagebox.showwarning(
                "Missing Name",
                "Please enter your name or club name.",
                parent=self
            )

            return

        if not self.selected_image:

            messagebox.showwarning(
                "Missing Image",
                "Please attach a notice image.",
                parent=self
            )

            return

        try:

            # =================================================
            # SAVE IMAGE
            # =================================================

            saved_path = ImageHandler.save_image(
                self.selected_image
            )

            # =================================================
            # CREATE SUBMISSION
            # =================================================

            submission = Submission(
                title=title,
                description=description,
                attachment=saved_path,
                attachment_type="image",
                submitted_by=submitted_by,
                submitter_type=submitter_type
            )

            # =================================================
            # SAVE TO MYSQL
            # =================================================

            if submission.save():

                messagebox.showinfo(
                    "Submitted",
                    (
                        "📤 Notice submitted successfully!\n\n"
                        "It is now waiting for admin approval."
                    ),
                    parent=self
                )

                self.clear_form()

            else:

                messagebox.showerror(
                    "Error",
                    "Could not submit the notice.",
                    parent=self
                )

        except Exception as e:

            print(
                "SUBMISSION ERROR:",
                e
            )

            messagebox.showerror(
                "Error",
                f"Something went wrong:\n\n{e}",
                parent=self
            )

    # =====================================================
    # CLEAR FORM
    # =====================================================

    def clear_form(self):

        self.title_entry.delete(
            0,
            "end"
        )

        self.description_entry.delete(
            "1.0",
            "end"
        )

        self.name_entry.delete(
            0,
            "end"
        )

        self.submitter_type.set(
            "student"
        )

        self.selected_image = None

        self.file_label.configure(
            text="No image selected"
        )