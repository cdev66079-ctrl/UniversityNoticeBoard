import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

from models.notice import Notice
from utils.image_handler import ImageHandler


class AdminDashboard(ctk.CTkFrame):

    def __init__(self, parent, back_to_board, current_user=None,toggle_dark_mode=None):

        super().__init__(parent)

        self.back_to_board = back_to_board
        self.current_user = current_user
        self.toggle_dark_mode = toggle_dark_mode
        self.selected_image = None

        self.configure(
            fg_color="#F2F2F2"
        )

        self.create_interface()

    # =====================================================
    # MAIN ADMIN INTERFACE
    # =====================================================

    def create_interface(self):

        header = ctk.CTkFrame(
            self,
            height=70,
            corner_radius=0
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        # =================================================
        # HEADER TITLE
        # =================================================

        title = ctk.CTkLabel(
            header,
            text="University Notice Board — Admin",
            font=("Arial", 24, "bold")
        )

        title.pack(
            side="left",
            padx=25
        )

        # =================================================
        # BACK BUTTON
        # =================================================

        back_button = ctk.CTkButton(
            header,
            text="← Notice Board",
            command=self.back_to_board
        )

        back_button.pack(
            side="right",
            padx=25
        )
        dark_button = ctk.CTkButton(
            header,
            text="🌙 Dark Mode",
             width=130,
             height=38,
             command=self.toggle_dark_mode
            ) 

        dark_button.pack(
            side="right",
             padx=10
            ) 

        # =================================================
        # CONTENT
        # =================================================

        content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=40
        )

        # =================================================
        # ADD NOTICE
        # =================================================

        add_notice = ctk.CTkButton(
            content,
            text="📌 Add Notice",
            width=300,
            height=60,
            font=("Arial", 20, "bold"),
            command=self.add_notice
        )

        add_notice.pack(
            pady=20
        )

        # =================================================
        # IMPORT NOTICE
        # =================================================

        import_notice = ctk.CTkButton(
            content,
            text="🖼️ Import Notice From Gallery",
            width=300,
            height=60,
            font=("Arial", 18),
            command=self.import_notice
        )

        import_notice.pack(
            pady=20
        )

        # =================================================
        # REMOVE NOTICE
        # =================================================

        remove_notice = ctk.CTkButton(
            content,
            text="🗑️ Remove Notice",
            width=300,
            height=60,
            font=("Arial", 18),
            fg_color="#B22222",
            hover_color="#8B0000",
            command=self.remove_notice
        )

        remove_notice.pack(
            pady=20
        )

    # =====================================================
    # ADD NOTICE MANUALLY
    # =====================================================

    def add_notice(self):

        self.selected_image = None

        dialog = ctk.CTkToplevel(
            self.winfo_toplevel()
        )

        dialog.title(
            "Add Notice"
        )

        dialog.geometry(
            "600x750"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.transient(
            self.winfo_toplevel()
        )

        # =================================================
        # SCROLLING AREA
        # =================================================

        content = ctk.CTkScrollableFrame(
            dialog,
            fg_color="#F2F2F2"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # =================================================
        # HEADER
        # =================================================

        heading = ctk.CTkLabel(
            content,
            text="📌 Create University Notice",
            font=("Arial", 24, "bold")
        )

        heading.pack(
            pady=(10, 25)
        )

        # =================================================
        # TITLE
        # =================================================

        ctk.CTkLabel(
            content,
            text="Notice Title",
            font=("Arial", 15, "bold")
        ).pack(
            pady=(5, 5)
        )

        title_entry = ctk.CTkEntry(
            content,
            width=480,
            height=42,
            placeholder_text="Enter notice title"
        )

        title_entry.pack()

        # =================================================
        # DESCRIPTION
        # =================================================

        ctk.CTkLabel(
            content,
            text="Description",
            font=("Arial", 15, "bold")
        ).pack(
            pady=(18, 5)
        )

        description_entry = ctk.CTkTextbox(
            content,
            width=480,
            height=120
        )

        description_entry.pack()

        # =================================================
        # CATEGORY
        # =================================================

        ctk.CTkLabel(
            content,
            text="Category",
            font=("Arial", 15, "bold")
        ).pack(
            pady=(18, 5)
        )

        category_box = ctk.CTkComboBox(
            content,
            width=350,
            height=40,
            values=[
                "Official Notice",
                "Examination",
                "Event",
                "Club",
                "Achievement",
                "Quote",
                "Student Announcement",
                "General"
            ]
        )

        category_box.set(
            "Official Notice"
        )

        category_box.pack()

        # =================================================
        # AUDIENCE
        # =================================================

        ctk.CTkLabel(
            content,
            text="Who is this notice for?",
            font=("Arial", 15, "bold")
        ).pack(
            pady=(18, 5)
        )

        audience_entry = ctk.CTkEntry(
            content,
            width=480,
            height=42,
            placeholder_text="Example: BCA 3rd Semester / BTech AI / Teachers"
        )

        audience_entry.pack()

        audience_info = ctk.CTkLabel(
            content,
            text="Leave blank if this notice is for Everyone.",
            font=("Arial", 11),
            text_color="#777777"
        )

        audience_info.pack(
            pady=(4, 5)
        )

        # =================================================
        # PRIORITY
        # =================================================

        ctk.CTkLabel(
            content,
            text="Priority",
            font=("Arial", 15, "bold")
        ).pack(
            pady=(18, 5)
        )

        priority_box = ctk.CTkComboBox(
            content,
            width=250,
            height=40,
            values=[
                "normal",
                "important"
            ]
        )

        priority_box.set(
            "normal"
        )

        priority_box.pack()

        # =================================================
        # EXPIRY DATE
        # =================================================

        ctk.CTkLabel(
            content,
            text="Expiry Date",
            font=("Arial", 15, "bold")
        ).pack(
            pady=(18, 5)
        )

        expiry_entry = ctk.CTkEntry(
            content,
            width=300,
            height=42,
            placeholder_text="YYYY-MM-DD  (optional)"
        )

        expiry_entry.pack()

        expiry_info = ctk.CTkLabel(
            content,
            text="Leave blank if the notice should not automatically expire.",
            font=("Arial", 11),
            text_color="#777777"
        )

        expiry_info.pack(
            pady=(4, 5)
        )

        # =================================================
        # ATTACHMENT
        # =================================================

        ctk.CTkLabel(
            content,
            text="Notice Image",
            font=("Arial", 15, "bold")
        ).pack(
            pady=(18, 5)
        )

        file_label = ctk.CTkLabel(
            content,
            text="No image selected",
            font=("Arial", 12),
            text_color="#777777"
        )

        file_label.pack(
            pady=5
        )

        def choose_image():

            file_path = filedialog.askopenfilename(
                parent=dialog,
                title="Select Notice Image",
                initialdir=os.path.expanduser(
                    "~/Downloads"
                ),
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

            file_label.configure(
                text=(
                    "Selected: "
                    + os.path.basename(file_path)
                )
            )

        ctk.CTkButton(
            content,
            text="🖼️ Choose Image",
            width=220,
            height=42,
            command=choose_image
        ).pack(
            pady=8
        )

        # =================================================
        # SAVE NOTICE
        # =================================================

        save_button = ctk.CTkButton(
            content,
            text="📌 PIN NOTICE TO BOARD",
            width=300,
            height=52,
            font=("Arial", 16, "bold"),
            command=lambda: self.save_manual_notice(
                title_entry,
                description_entry,
                category_box,
                audience_entry,
                priority_box,
                expiry_entry,
                dialog
            )
        )

        save_button.pack(
            pady=(25, 10)
        )

        # =================================================
        # CANCEL
        # =================================================

        ctk.CTkButton(
            content,
            text="Cancel",
            width=150,
            command=dialog.destroy
        ).pack(
            pady=(5, 20)
        )

    # =====================================================
    # SAVE MANUAL NOTICE
    # =====================================================

    def save_manual_notice(
        self,
        title_entry,
        description_entry,
        category_box,
        audience_entry,
        priority_box,
        expiry_entry,
        dialog
    ):

        title = title_entry.get().strip()

        description = (
            description_entry
            .get("1.0", "end")
            .strip()
        )

        category_name = category_box.get().strip()

        audience = audience_entry.get().strip()

        priority = priority_box.get().strip()

        expiry_date = expiry_entry.get().strip()

        # =================================================
        # VALIDATION
        # =================================================

        if not title:

            messagebox.showwarning(
                "Missing Title",
                "Please enter a notice title.",
                parent=dialog
            )

            return

        # =================================================
        # AUDIENCE
        # =================================================

        if not audience:

            audience = "Everyone"

        # =================================================
        # EXPIRY DATE VALIDATION
        # =================================================

        if expiry_date:

            import datetime

            try:

                datetime.datetime.strptime(
                    expiry_date,
                    "%Y-%m-%d"
                )

            except ValueError:

                messagebox.showwarning(
                    "Invalid Date",
                    "Expiry date must be in YYYY-MM-DD format.\n\n"
                    "Example: 2026-12-31",
                    parent=dialog
                )

                return

        # =================================================
        # CATEGORY MAP
        # =================================================

        category_map = {

            "Official Notice": 1,
            "Examination": 2,
            "Event": 3,
            "Club": 4,
            "Achievement": 5,
            "Quote": 6,
            "Student Announcement": 7,
            "General": 8

        }

        category_id = category_map.get(
            category_name,
            1
        )

        # =================================================
        # ATTACHMENT
        # =================================================

        attachment = None
        attachment_type = "none"

        if self.selected_image:

            try:

                attachment = ImageHandler.save_image(
                    self.selected_image
                )

                attachment_type = "image"

            except Exception as e:

                messagebox.showerror(
                    "Image Error",
                    str(e),
                    parent=dialog
                )

                return

        # =================================================
        # CREATE NOTICE
        # =================================================

        notice = Notice(
            title=title,
            description=description,
            category_id=category_id,
            audience=audience,
            attachment=attachment,
            attachment_type=attachment_type,
            posted_by=(
                self.current_user.get("user_id")
                if self.current_user
                else 1
            )
        )

        # =================================================
        # SAVE
        # =================================================

        if notice.save():

            # Save priority and expiry separately
            # because the current Notice constructor
            # does not contain these fields.

            self.update_notice_extra_fields(
                title,
                priority,
                expiry_date
            )

            messagebox.showinfo(
                "Success",
                (
                    "📌 Notice pinned successfully!\n\n"
                    f"Audience: {audience}"
                ),
                parent=dialog
            )

            self.selected_image = None

            dialog.destroy()

            self.back_to_board()

        else:

            messagebox.showerror(
                "Error",
                "Could not save the notice.",
                parent=dialog
            )

    # =====================================================
    # UPDATE PRIORITY / EXPIRY
    # =====================================================

    def update_notice_extra_fields(
        self,
        title,
        priority,
        expiry_date
    ):

        from database import Database

        db = Database()

        if not db.connect():
            return False

        try:

            cursor = db.connection.cursor()

            # Get newest notice with this title
            cursor.execute(
                """
                SELECT notice_id
                FROM notices
                WHERE title = %s
                ORDER BY notice_id DESC
                LIMIT 1
                """,
                (title,)
            )

            result = cursor.fetchone()

            if not result:

                cursor.close()
                db.close()

                return False

            notice_id = result[0]

            cursor.execute(
                """
                UPDATE notices
                SET priority = %s,
                    expiry_date = %s
                WHERE notice_id = %s
                """,
                (
                    priority,
                    expiry_date if expiry_date else None,
                    notice_id
                )
            )

            db.connection.commit()

            cursor.close()
            db.close()

            return True

        except Exception as e:

            print(
                "Notice extra field error:",
                e
            )

            try:
                db.connection.rollback()
                db.close()
            except Exception:
                pass

            return False

    # =====================================================
    # IMPORT NOTICE FROM GALLERY
    # =====================================================

    def import_notice(self):

        file_path = filedialog.askopenfilename(
            parent=self,
            title="Select Notice",
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

        print(
            "Selected file:",
            file_path
        )

        self.selected_image = file_path

        self.show_notice_details()

    # =====================================================
    # IMPORT NOTICE DETAILS
    # =====================================================

    def show_notice_details(self):

        dialog = ctk.CTkToplevel(
            self.winfo_toplevel()
        )

        dialog.title(
            "Import Notice"
        )

        dialog.geometry(
            "500x650"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.transient(
            self.winfo_toplevel()
        )

        # =================================================
        # TITLE
        # =================================================

        ctk.CTkLabel(
            dialog,
            text="Notice Title",
            font=("Arial", 16, "bold")
        ).pack(
            pady=(25, 5)
        )

        title_entry = ctk.CTkEntry(
            dialog,
            width=350,
            height=40,
            placeholder_text="Enter notice title"
        )

        title_entry.pack()

        # =================================================
        # DESCRIPTION
        # =================================================

        ctk.CTkLabel(
            dialog,
            text="Description (optional)",
            font=("Arial", 16, "bold")
        ).pack(
            pady=(18, 5)
        )

        description_entry = ctk.CTkTextbox(
            dialog,
            width=350,
            height=90
        )

        description_entry.pack()

        # =================================================
        # AUDIENCE
        # =================================================

        ctk.CTkLabel(
            dialog,
            text="Who is this notice for?",
            font=("Arial", 16, "bold")
        ).pack(
            pady=(18, 5)
        )

        audience_entry = ctk.CTkEntry(
            dialog,
            width=350,
            height=40,
            placeholder_text="Leave blank for Everyone"
        )

        audience_entry.pack()

        # =================================================
        # FILE
        # =================================================

        ctk.CTkLabel(
            dialog,
            text=(
                "Selected:\n"
                + os.path.basename(
                    self.selected_image
                )
            ),
            font=("Arial", 13)
        ).pack(
            pady=15
        )

        # =================================================
        # SAVE
        # =================================================

        ctk.CTkButton(
            dialog,
            text="📌 PIN NOTICE TO BOARD",
            width=250,
            height=50,
            font=("Arial", 16, "bold"),
            command=lambda: self.save_imported_notice(
                title_entry,
                description_entry,
                audience_entry,
                dialog
            )
        ).pack(
            pady=20
        )

        # =================================================
        # CANCEL
        # =================================================

        ctk.CTkButton(
            dialog,
            text="Cancel",
            width=150,
            command=dialog.destroy
        ).pack(
            pady=5
        )

    # =====================================================
    # SAVE IMPORTED NOTICE
    # =====================================================

    def save_imported_notice(
        self,
        title_entry,
        description_entry,
        audience_entry,
        dialog
    ):

        title = title_entry.get().strip()

        description = (
            description_entry
            .get("1.0", "end")
            .strip()
        )

        audience = audience_entry.get().strip()

        if not audience:

            audience = "Everyone"

        if not title:

            messagebox.showwarning(
                "Missing Title",
                "Please enter a notice title.",
                parent=dialog
            )

            return

        if not self.selected_image:

            messagebox.showwarning(
                "Missing Notice",
                "Please select a notice image.",
                parent=dialog
            )

            return

        try:

            saved_path = ImageHandler.save_image(
                self.selected_image
            )

            notice = Notice(
                title=title,
                description=description,
                category_id=1,
                audience=audience,
                attachment=saved_path,
                attachment_type="image",
                posted_by=(
                    self.current_user.get("user_id")
                    if self.current_user
                    else 1
                )
            )

            if notice.save():

                messagebox.showinfo(
                    "Success",
                    (
                        "📌 Notice pinned successfully!\n\n"
                        f"Audience: {audience}"
                    ),
                    parent=dialog
                )

                self.selected_image = None

                dialog.destroy()

                self.back_to_board()

            else:

                messagebox.showerror(
                    "Error",
                    "Could not save the notice.",
                    parent=dialog
                )

        except Exception as e:

            print(
                "SAVE ERROR:",
                e
            )

            messagebox.showerror(
                "Error",
                f"Something went wrong:\n\n{e}",
                parent=dialog
            )

    # =====================================================
    # REMOVE NOTICE
    # =====================================================

    def remove_notice(self):

        notices = Notice.get_all()

        if not notices:

            messagebox.showinfo(
                "No Notices",
                "There are no notices to remove.",
                parent=self
            )

            return

        dialog = ctk.CTkToplevel(
            self.winfo_toplevel()
        )

        dialog.title(
            "Remove Notice"
        )

        dialog.geometry(
            "550x550"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.transient(
            self.winfo_toplevel()
        )

        heading = ctk.CTkLabel(
            dialog,
            text="🗑️ Remove Notice",
            font=("Arial", 24, "bold")
        )

        heading.pack(
            pady=(25, 10)
        )

        instruction = ctk.CTkLabel(
            dialog,
            text="Select the notice you want to remove:",
            font=("Arial", 14)
        )

        instruction.pack(
            pady=(0, 15)
        )

        notice_frame = ctk.CTkScrollableFrame(
            dialog,
            width=450,
            height=300
        )

        notice_frame.pack(
            padx=25,
            pady=10,
            fill="both",
            expand=True
        )

        selected_notice = {
            "id": None
        }

        for notice in notices:

            notice_id = notice["notice_id"]

            notice_title = notice["title"]

            button = ctk.CTkButton(
                notice_frame,
                text=f"📌  {notice_title}",
                height=45,
                anchor="w",
                font=("Arial", 14),
                command=lambda n_id=notice_id:
                    self.select_notice(
                        n_id,
                        selected_notice
                    )
            )

            button.pack(
                fill="x",
                padx=10,
                pady=5
            )

        delete_button = ctk.CTkButton(
            dialog,
            text="🗑️ DELETE SELECTED NOTICE",
            width=280,
            height=50,
            font=("Arial", 15, "bold"),
            fg_color="#B22222",
            hover_color="#8B0000",
            command=lambda: self.confirm_delete(
                selected_notice,
                dialog
            )
        )

        delete_button.pack(
            pady=15
        )

        ctk.CTkButton(
            dialog,
            text="Cancel",
            width=130,
            command=dialog.destroy
        ).pack(
            pady=(0, 20)
        )

    # =====================================================
    # SELECT NOTICE
    # =====================================================

    def select_notice(
        self,
        notice_id,
        selected_notice
    ):

        selected_notice["id"] = notice_id

        print(
            "Selected notice:",
            notice_id
        )

    # =====================================================
    # CONFIRM DELETE
    # =====================================================

    def confirm_delete(
        self,
        selected_notice,
        dialog
    ):

        notice_id = selected_notice["id"]

        if not notice_id:

            messagebox.showwarning(
                "Select Notice",
                "Please select a notice first.",
                parent=dialog
            )

            return

        notices = Notice.get_all()

        selected_title = "this notice"

        for notice in notices:

            if notice["notice_id"] == notice_id:

                selected_title = notice["title"]

                break

        answer = messagebox.askyesno(
            "Confirm Delete",
            (
                "Are you sure you want to remove:\n\n"
                f"📌 {selected_title}\n\n"
                "This will permanently remove the notice."
            ),
            parent=dialog
        )

        if not answer:
            return

        if Notice.delete(notice_id):

            messagebox.showinfo(
                "Removed",
                "🗑️ Notice removed successfully!",
                parent=dialog
            )

            dialog.destroy()

            self.back_to_board()

        else:

            messagebox.showerror(
                "Error",
                "Could not remove the notice.",
                parent=dialog
            )