import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

from models.community_post import CommunityPost
from models.community_comment import CommunityComment
from utils.image_handler import ImageHandler
from utils.nepali_date import format_bs_datetime


class CommunityBoard(ctk.CTkFrame):

    def __init__(self, parent, back_to_home, current_user=None,toggle_dark_mode=None):

        super().__init__(parent)

        self.back_to_home = back_to_home
        self.current_user = current_user
        self.toggle_dark_mode = toggle_dark_mode
        self.selected_image = None

        self.configure(
            fg_color="#E8DDC8"
        )

        self.create_interface()
        self.load_posts()

    # ==================================================
    # MAIN INTERFACE
    # ==================================================

    def create_interface(self):

        header = ctk.CTkFrame(
            self,
            height=70,
            corner_radius=0,
            fg_color="#5C4033"
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="🧑‍🤝‍🧑 COMMUNITY NOTICE BOARD",
            font=("Arial", 24, "bold"),
            text_color="#FFFFFF"
        )

        title.pack(
            side="left",
            padx=25
        )

        post_button = ctk.CTkButton(
            header,
            text="📌 Post Something",
            width=170,
            height=40,
            command=self.open_post_window
        )

        post_button.pack(
            side="right",
            padx=10
        )

        back_button = ctk.CTkButton(
            header,
            text="← Back",
            width=100,
            command=self.back_to_home
        )

        back_button.pack(
            side="right",
            padx=15
        )
        dark_mode_button = ctk.CTkButton(
            header,
            text="🌙  Dark Mode",
            width=130,
            height=40,
            command=self.toggle_dark_mode
        )   
        dark_mode_button.pack(
            side="right",
            padx=10
        )

        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#E8DDC8"
        )

        self.scroll_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )

    # ==================================================
    # LOAD POSTS
    # ==================================================

    def load_posts(self):

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Automatically archive posts older than 60 days
        CommunityPost.archive_old_posts()

        posts = CommunityPost.get_all()

        if not posts:

            label = ctk.CTkLabel(
                self.scroll_frame,
                text="📌 No community notices yet.\n\nBe the first to post!",
                font=("Arial", 20),
                text_color="#3B2F2F"
            )

            label.pack(
                pady=100
            )

            return

        for post in posts:

            self.create_post_card(post)

    # ==================================================
    # POST CARD
    # ==================================================

    def create_post_card(self, post):

        card = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="#FFF8DC",
            corner_radius=6,
            border_width=2,
            border_color="#8B7355"
        )

        card.pack(
            fill="x",
            padx=20,
            pady=12
        )

        # ==============================================
        # TITLE
        # ==============================================

        title = ctk.CTkLabel(
            card,
            text=f"📌 {post['title']}",
            font=("Arial", 22, "bold"),
            text_color="#21180F",
            anchor="w"
        )

        title.pack(
            fill="x",
            padx=20,
            pady=(15, 5)
        )

        # ==============================================
        # CATEGORY
        # ==============================================

        category = post.get(
            "category_name",
            "General"
        )

        category_label = ctk.CTkLabel(
            card,
            text=f"Category: {category}",
            font=("Arial", 14, "bold"),
            text_color="#5C4033",
            anchor="w"
        )

        category_label.pack(
            fill="x",
            padx=20,
            pady=(0, 8)
        )

        # ==============================================
        # CONTENT
        # ==============================================

        if post.get("content"):

            content = ctk.CTkLabel(
                card,
                text=post["content"],
                font=("Arial", 16),
                text_color="#21180F",
                justify="left",
                anchor="w",
                wraplength=850
            )

            content.pack(
                fill="x",
                padx=20,
                pady=10
            )

        # ==============================================
        # POSTED BY
        # ==============================================

        poster = (
            post.get("display_name")
            or post.get("poster_name")
            or "Anonymous"
        )

        posted_by = ctk.CTkLabel(
            card,
            text=f"👤 Posted by: {poster}",
            font=("Arial", 13),
            text_color="#4A3728",
            anchor="w"
        )

        posted_by.pack(
            fill="x",
            padx=20,
            pady=(5, 5)
        )

        # ==============================================
        # POSTED DATE - NEPALI
        # ==============================================

        posted_date = ctk.CTkLabel(
            card,
            text=f"📅 {format_bs_datetime(post['posted_at'])}",
            font=("Arial", 12),
            text_color="#6B5847",
            anchor="w"
        )

        posted_date.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        # ==============================================
        # ATTACHMENT
        # ==============================================

        attachment = post.get("attachment")

        if attachment:

            attachment_button = ctk.CTkButton(
                card,
                text="🖼️ View Attachment",
                width=180,
                height=35,
                command=lambda p=attachment:
                    self.open_attachment(p)
            )

            attachment_button.pack(
                pady=(0, 10)
            )

        # ==============================================
        # COMMENTS
        # ==============================================

        comments_frame = ctk.CTkFrame(
            card,
            fg_color="#F5EBD0",
            corner_radius=5
        )

        comments_frame.pack(
            fill="x",
            padx=20,
            pady=(5, 15)
        )

        comments = CommunityComment.get_by_post(
            post["post_id"]
        )

        comments_title = ctk.CTkLabel(
            comments_frame,
            text=f"💬 Comments ({len(comments)})",
            font=("Arial", 14, "bold"),
            text_color="#3B2F2F",
            anchor="w"
        )

        comments_title.pack(
            fill="x",
            padx=15,
            pady=(10, 5)
        )

        # ==============================================
        # DISPLAY COMMENTS
        # ==============================================

        for comment in comments:

            comment_box = ctk.CTkFrame(
                comments_frame,
                fg_color="#FFFDF5",
                corner_radius=4
            )

            comment_box.pack(
                fill="x",
                padx=10,
                pady=4
            )

            commenter = (
                comment.get("display_name")
                or comment.get("commenter_name")
                or "Anonymous"
            )

            # ------------------------------------------
            # COMMENTER NAME
            # ------------------------------------------

            commenter_label = ctk.CTkLabel(
                comment_box,
                text=f"👤 {commenter}",
                font=("Arial", 12, "bold"),
                text_color="#3B2F2F",
                anchor="w"
            )

            commenter_label.pack(
                fill="x",
                padx=10,
                pady=(6, 0)
            )

            # ------------------------------------------
            # COMMENT TEXT
            # ------------------------------------------

            comment_text = ctk.CTkLabel(
                comment_box,
                text=comment["comment_text"],
                font=("Arial", 13),
                text_color="#21180F",
                justify="left",
                anchor="w",
                wraplength=750
            )

            comment_text.pack(
                fill="x",
                padx=10,
                pady=(2, 3)
            )

            # ------------------------------------------
            # COMMENT DATE - NEPALI
            # ------------------------------------------

            if comment.get("commented_at"):

                comment_date = ctk.CTkLabel(
                    comment_box,
                    text=(
                        f"📅 "
                        f"{format_bs_datetime(comment['commented_at'])}"
                    ),
                    font=("Arial", 10),
                    text_color="#7A6857",
                    anchor="w"
                )

                comment_date.pack(
                    fill="x",
                    padx=10,
                    pady=(0, 7)
                )

        # ==============================================
        # COMMENT BUTTON
        # ==============================================

        comment_button = ctk.CTkButton(
            comments_frame,
            text="💬 Comment",
            width=130,
            height=35,
            command=lambda p=post["post_id"]:
                self.open_comment_window(p)
        )

        comment_button.pack(
            padx=10,
            pady=(8, 12)
        )

        # ==============================================
        # ADMIN REMOVE BUTTON
        # ==============================================

        if (
            self.current_user
            and self.current_user.get("role") == "admin"
        ):

            remove_button = ctk.CTkButton(
                card,
                text="🗑️ Remove",
                width=130,
                height=35,
                fg_color="#8B0000",
                hover_color="#B22222",
                command=lambda p=post:
                    self.remove_post(p)
            )

            remove_button.pack(
                pady=(0, 15)
            )

    # ==================================================
    # OPEN ATTACHMENT
    # ==================================================

    def open_attachment(self, path):

        try:

            if not os.path.exists(path):

                messagebox.showerror(
                    "File Not Found",
                    "The attachment file could not be found."
                )

                return

            os.system(
                f'xdg-open "{path}"'
            )

        except Exception as e:

            messagebox.showerror(
                "Attachment Error",
                str(e)
            )

    # ==================================================
    # COMMENT WINDOW
    # ==================================================

    def open_comment_window(self, post_id):

        dialog = ctk.CTkToplevel(
            self.winfo_toplevel()
        )

        dialog.title(
            "Add Comment"
        )

        dialog.geometry(
            "500x430"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.transient(
            self.winfo_toplevel()
        )

        # ==============================================
        # TITLE
        # ==============================================

        ctk.CTkLabel(
            dialog,
            text="💬 Add Comment",
            font=("Arial", 22, "bold"),
            text_color="#21180F"
        ).pack(
            pady=(25, 15)
        )

        # ==============================================
        # NAME
        # ==============================================

        ctk.CTkLabel(
            dialog,
            text="Your Name / Class / Club",
            font=("Arial", 14, "bold"),
            text_color="#21180F"
        ).pack(
            pady=(5, 5)
        )

        name_entry = ctk.CTkEntry(
            dialog,
            width=380,
            height=40,
            placeholder_text="Example: BCA 3rd Semester"
        )

        name_entry.pack()

        # ==============================================
        # COMMENT
        # ==============================================

        ctk.CTkLabel(
            dialog,
            text="Comment",
            font=("Arial", 14, "bold"),
            text_color="#21180F"
        ).pack(
            pady=(15, 5)
        )

        comment_box = ctk.CTkTextbox(
            dialog,
            width=380,
            height=100
        )

        comment_box.pack()

        # ==============================================
        # SUBMIT
        # ==============================================

        def submit_comment():

            display_name = (
                name_entry
                .get()
                .strip()
            )

            text = (
                comment_box
                .get("1.0", "end")
                .strip()
            )

            if not display_name:

                messagebox.showwarning(
                    "Name Required",
                    "Please enter your name, class or club.",
                    parent=dialog
                )

                return

            if not text:

                messagebox.showwarning(
                    "Empty Comment",
                    "Please write something.",
                    parent=dialog
                )

                return

            comment = CommunityComment(
                post_id=post_id,
                user_id=None,
                comment_text=text,
                display_name=display_name
            )

            if comment.save():

                messagebox.showinfo(
                    "Comment Added",
                    "💬 Your comment has been posted!",
                    parent=dialog
                )

                dialog.destroy()

                self.load_posts()

            else:

                messagebox.showerror(
                    "Error",
                    "Could not save comment.",
                    parent=dialog
                )

        ctk.CTkButton(
            dialog,
            text="💬 POST COMMENT",
            width=220,
            height=45,
            command=submit_comment
        ).pack(
            pady=20
        )

    # ==================================================
    # POST WINDOW
    # ==================================================

    def open_post_window(self):

        self.selected_image = None

        dialog = ctk.CTkToplevel(
            self.winfo_toplevel()
        )

        dialog.title(
            "Post to Community"
        )

        dialog.geometry(
            "550x750"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.transient(
            self.winfo_toplevel()
        )

        # ==============================================
        # IDENTITY
        # ==============================================

        ctk.CTkLabel(
            dialog,
            text="Your Name / Class / Club",
            font=("Arial", 16, "bold"),
            text_color="#21180F"
        ).pack(
            pady=(25, 5)
        )

        display_name_entry = ctk.CTkEntry(
            dialog,
            width=400,
            height=40,
            placeholder_text="Example: BCA 3rd Semester"
        )

        display_name_entry.pack()

        # ==============================================
        # TITLE
        # ==============================================

        ctk.CTkLabel(
            dialog,
            text="Notice Title",
            font=("Arial", 16, "bold"),
            text_color="#21180F"
        ).pack(
            pady=(20, 5)
        )

        title_entry = ctk.CTkEntry(
            dialog,
            width=400,
            height=40,
            placeholder_text="Example: Cricket Tournament"
        )

        title_entry.pack()

        # ==============================================
        # CATEGORY
        # ==============================================

        ctk.CTkLabel(
            dialog,
            text="Category",
            font=("Arial", 16, "bold"),
            text_color="#21180F"
        ).pack(
            pady=(20, 5)
        )

        category_box = ctk.CTkComboBox(
            dialog,
            width=400,
            values=[
                "Event",
                "Club",
                "Achievement",
                "Quote",
                "Student Announcement",
                "General"
            ]
        )

        category_box.set(
            "General"
        )

        category_box.pack()

        # ==============================================
        # CONTENT
        # ==============================================

        ctk.CTkLabel(
            dialog,
            text="Message",
            font=("Arial", 16, "bold"),
            text_color="#21180F"
        ).pack(
            pady=(20, 5)
        )

        content_box = ctk.CTkTextbox(
            dialog,
            width=400,
            height=130
        )

        content_box.pack()

        # ==============================================
        # ATTACHMENT
        # ==============================================

        attachment_label = ctk.CTkLabel(
            dialog,
            text="No image selected",
            font=("Arial", 12),
            text_color="#4A3728"
        )

        attachment_label.pack(
            pady=10
        )

        def choose_image():

            file_path = filedialog.askopenfilename(
                parent=dialog,
                initialdir=os.path.expanduser(
                    "~/Downloads"
                ),
                title="Choose Image",
                filetypes=[
                    (
                        "Images",
                        "*.jpg *.jpeg *.png *.webp"
                    ),
                    (
                        "All Files",
                        "*.*"
                    )
                ]
            )

            if file_path:

                self.selected_image = file_path

                attachment_label.configure(
                    text=os.path.basename(
                        file_path
                    )
                )

        ctk.CTkButton(
            dialog,
            text="🖼️ Attach Image",
            width=200,
            command=choose_image
        ).pack(
            pady=5
        )

        # ==============================================
        # SUBMIT
        # ==============================================

        def submit():

            display_name = (
                display_name_entry
                .get()
                .strip()
            )

            title = (
                title_entry
                .get()
                .strip()
            )

            content = (
                content_box
                .get("1.0", "end")
                .strip()
            )

            category_name = category_box.get()

            # ==========================================
            # VALIDATION
            # ==========================================

            if not display_name:

                messagebox.showwarning(
                    "Name Required",
                    "Please enter your name, class or club.",
                    parent=dialog
                )

                return

            if not title:

                messagebox.showwarning(
                    "Missing Title",
                    "Please enter a title.",
                    parent=dialog
                )

                return

            # ==========================================
            # CATEGORY
            # ==========================================

            category_map = {

                "Event": 3,
                "Club": 4,
                "Achievement": 5,
                "Quote": 6,
                "Student Announcement": 7,
                "General": 8

            }

            category_id = category_map.get(
                category_name,
                8
            )

            # ==========================================
            # ATTACHMENT
            # ==========================================

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

            # ==========================================
            # CREATE POST
            # ==========================================

            post = CommunityPost(
                title=title,
                content=content,
                category_id=category_id,
                attachment=attachment,
                attachment_type=attachment_type,
                posted_by=None,
                display_name=display_name,
                status="active"
            )

            # ==========================================
            # SAVE POST
            # ==========================================

            if post.save():

                messagebox.showinfo(
                    "Posted",
                    "📌 Your notice has been pinned!",
                    parent=dialog
                )

                self.selected_image = None

                dialog.destroy()

                self.load_posts()

            else:

                messagebox.showerror(
                    "Error",
                    "Could not save the post.",
                    parent=dialog
                )

        ctk.CTkButton(
            dialog,
            text="📌 PIN TO COMMUNITY BOARD",
            width=300,
            height=50,
            font=("Arial", 16, "bold"),
            command=submit
        ).pack(
            pady=25
        )

    # ==================================================
    # REMOVE POST
    # ==================================================

    def remove_post(self, post):

        confirm = messagebox.askyesno(
            "Remove Community Post",
            f"Are you sure you want to remove:\n\n"
            f"{post['title']}\n\n"
            f"This cannot be undone."
        )

        if not confirm:
            return

        community_post = CommunityPost(
            post_id=post["post_id"],
            title=post["title"],
            content=post.get("content"),
            category_id=post.get("category_id"),
            attachment=post.get("attachment"),
            attachment_type=post.get("attachment_type"),
            posted_by=post.get("posted_by"),
            display_name=post.get("display_name"),
            status=post.get("status")
        )

        if community_post.delete():

            messagebox.showinfo(
                "Removed",
                "🗑️ Community post removed successfully."
            )

            self.load_posts()

        else:

            messagebox.showerror(
                "Error",
                "Could not remove the community post."
            )