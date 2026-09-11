import customtkinter as ctk
from PIL import Image
import os

from models.notice import Notice
from utils.nepali_date import format_bs_datetime


class NoticeBoard(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        open_admin,
        open_community,
        current_user=None
    ):

        super().__init__(parent)

        self.open_admin = open_admin
        self.open_community = open_community
        self.current_user = current_user

        self.notice_images = []

        # ==============================================
        # LIGHT / DARK COLORS
        # ==============================================

        self.light_colors = {
            "background": "#6B4226",
            "header": "#3B2415",
            "outer": "#8A5A32",
            "board": "#A66D3F",
            "paper": "#FFF8DC",
            "paper_border": "#D2B98B",
            "title": "#332215",
            "text": "#3B2415",
            "secondary": "#765432",
            "date": "#777777",
            "viewer": "#E8D5B7",
            "button": "#6B4226",
            "button_hover": "#4A2C19"
        }

        self.dark_colors = {
            "background": "#171717",
            "header": "#101010",
            "outer": "#242424",
            "board": "#303030",
            "paper": "#262626",
            "paper_border": "#444444",
            "title": "#F5F5F5",
            "text": "#EAEAEA",
            "secondary": "#BDBDBD",
            "date": "#AAAAAA",
            "viewer": "#1E1E1E",
            "button": "#444444",
            "button_hover": "#555555"
        }

        # ==============================================
        # CURRENT THEME
        # ==============================================

        self.current_theme = "Light"

        self.configure(
            fg_color=self.get_color("background")
        )

        self.create_header()
        self.create_board()
        self.load_notices()

    # =====================================================
    # THEME COLOR
    # =====================================================

    def get_color(self, name):

        if self.current_theme == "Dark":

            return self.dark_colors[name]

        return self.light_colors[name]

    # =====================================================
    # TOGGLE DARK MODE
    # =====================================================

    def toggle_dark_mode(self):

        if self.current_theme == "Light":

            self.current_theme = "Dark"

            ctk.set_appearance_mode("Dark")

        else:

            self.current_theme = "Light"

            ctk.set_appearance_mode("Light")

        self.refresh_theme()

    # =====================================================
    # REFRESH THEME
    # =====================================================

    def refresh_theme(self):

        # Rebuild the complete board so every widget
        # receives the correct colors.

        for widget in self.winfo_children():

            widget.destroy()

        self.notice_images.clear()

        self.configure(
            fg_color=self.get_color("background")
        )

        self.create_header()
        self.create_board()
        self.load_notices()

    # =====================================================
    # HEADER
    # =====================================================

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            height=80,
            corner_radius=0,
            fg_color=self.get_color("header")
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        # ==============================================
        # TITLE
        # ==============================================

        title = ctk.CTkLabel(
            header,
            text="🎓  PUSAT NOTICE BOARD",
            font=("Georgia", 27, "bold"),
            text_color=(
                "#FFF4D6"
                if self.current_theme == "Light"
                else "#FFFFFF"
            )
        )

        title.pack(
            side="left",
            padx=25
        )

        # ==============================================
        # DARK MODE BUTTON
        # ==============================================

        if self.current_theme == "Light":

            theme_text = "🌙 Dark Mode"

        else:

            theme_text = "☀ Light Mode"

        theme_button = ctk.CTkButton(
            header,
            text=theme_text,
            width=135,
            height=38,
            font=("Arial", 12, "bold"),
            fg_color=self.get_color("button"),
            hover_color=self.get_color("button_hover"),
            command=self.toggle_dark_mode
        )

        theme_button.pack(
            side="right",
            padx=10
        )

        # ==============================================
        # COMMUNITY BUTTON
        # ==============================================

        community_button = ctk.CTkButton(
            header,
            text="🧑‍🤝‍🧑 Community",
            width=150,
            height=40,
            fg_color=self.get_color("button"),
            hover_color=self.get_color("button_hover"),
            command=self.open_community
        )

        community_button.pack(
            side="right",
            padx=10
        )

        # ==============================================
        # ADMIN BUTTON
        # ==============================================

        admin_button = ctk.CTkButton(
            header,
            text="⚙ ADMIN",
            width=110,
            height=38,
            font=("Arial", 13, "bold"),
            fg_color=self.get_color("button"),
            hover_color=self.get_color("button_hover"),
            command=self.open_admin
        )

        admin_button.pack(
            side="right",
            padx=10
        )

    # =====================================================
    # BOARD
    # =====================================================

    def create_board(self):

        outer = ctk.CTkFrame(
            self,
            fg_color=self.get_color("outer"),
            corner_radius=18,
            border_width=8,
            border_color=(
                "#4A2C19"
                if self.current_theme == "Light"
                else "#151515"
            )
        )

        outer.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.board = ctk.CTkScrollableFrame(
            outer,
            fg_color=self.get_color("board"),
            corner_radius=10
        )

        self.board.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=12
        )

        # ==============================================
        # THREE COLUMNS
        # ==============================================

        for column in range(3):

            self.board.grid_columnconfigure(
                column,
                weight=1
            )

    # =====================================================
    # LOAD NOTICES
    # =====================================================

    def load_notices(self):

        for widget in self.board.winfo_children():

            widget.destroy()

        self.notice_images.clear()

        notices = Notice.get_all()

        if not notices:

            empty = ctk.CTkLabel(
                self.board,
                text="📌  The notice board is empty",
                font=("Georgia", 24, "bold"),
                text_color=self.get_color("text")
            )

            empty.pack(
                pady=150
            )

            return

        for index, notice in enumerate(notices):

            self.create_notice_card(
                notice,
                index
            )

    # =====================================================
    # FORMAT DATE
    # =====================================================

    def get_display_date(self, date_value):

        if not date_value:

            return "Date unavailable"

        try:

            bs_date = format_bs_datetime(
                date_value
            )

            if hasattr(
                date_value,
                "strftime"
            ):

                ad_date = date_value.strftime(
                    "%B %d, %Y"
                )

                if hasattr(
                    date_value,
                    "hour"
                ):

                    ad_date = date_value.strftime(
                        "%B %d, %Y • %I:%M %p"
                    )

            else:

                ad_date = str(
                    date_value
                )

            return (
                f"{bs_date} (BS)\n"
                f"{ad_date} (AD)"
            )

        except Exception as e:

            print(
                "Date formatting error:",
                e
            )

            return str(
                date_value
            )

    # =====================================================
    # NOTICE CARD
    # =====================================================

    def create_notice_card(
        self,
        notice,
        index
    ):

        paper_sizes = [
            (310, 420),
            (330, 440),
            (300, 410),
            (320, 430)
        ]

        width, height = paper_sizes[
            index % len(paper_sizes)
        ]

        paper = ctk.CTkFrame(
            self.board,
            width=width,
            height=height,
            corner_radius=3,
            fg_color=self.get_color("paper"),
            border_width=1,
            border_color=self.get_color("paper_border")
        )

        row = index // 3
        column = index % 3

        paper.grid(
            row=row,
            column=column,
            padx=25,
            pady=30,
            sticky="n"
        )

        paper.grid_propagate(False)

        # =================================================
        # PIN
        # =================================================

        pin_colors = [
            "🔴",
            "🔵",
            "🟢",
            "🟡"
        ]

        pin = ctk.CTkLabel(
            paper,
            text=pin_colors[index % 4],
            font=("Arial", 20),
            fg_color="transparent"
        )

        pin.place(
            relx=0.5,
            y=3,
            anchor="n"
        )

        # =================================================
        # IMPORTANT
        # =================================================

        if notice.get("priority") == "important":

            important = ctk.CTkLabel(
                paper,
                text="⚠ IMPORTANT",
                font=("Arial", 11, "bold"),
                text_color="#FF5C5C"
            )

            important.pack(
                pady=(30, 0)
            )

        else:

            spacer = ctk.CTkLabel(
                paper,
                text="",
                fg_color="transparent"
            )

            spacer.pack(
                pady=15
            )

        # =================================================
        # CATEGORY
        # =================================================

        category = notice.get(
            "category_name"
        )

        if category:

            category_label = ctk.CTkLabel(
                paper,
                text=category.upper(),
                font=("Arial", 9, "bold"),
                text_color=self.get_color("secondary")
            )

            category_label.pack(
                pady=(2, 2)
            )

        # =================================================
        # AUDIENCE
        # =================================================

        audience = notice.get(
            "audience"
        )

        if not audience:

            audience = "Everyone"

        audience_label = ctk.CTkLabel(
            paper,
            text=f"👥 For: {audience}",
            font=("Arial", 10, "bold"),
            text_color=self.get_color("secondary"),
            wraplength=width - 40
        )

        audience_label.pack(
            pady=(2, 5)
        )

        # =================================================
        # TITLE
        # =================================================

        title = ctk.CTkLabel(
            paper,
            text=notice["title"],
            font=("Georgia", 18, "bold"),
            text_color=self.get_color("title"),
            wraplength=width - 40
        )

        title.pack(
            padx=15,
            pady=5
        )

        # =================================================
        # IMAGE
        # =================================================

        attachment = notice.get(
            "attachment"
        )

        if attachment:

            project_folder = os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )

            image_path = os.path.join(
                project_folder,
                attachment
            )

            if os.path.exists(image_path):

                try:

                    image = Image.open(
                        image_path
                    )

                    image.thumbnail(
                        (width - 35, height - 175)
                    )

                    ctk_image = ctk.CTkImage(
                        light_image=image,
                        dark_image=image,
                        size=image.size
                    )

                    self.notice_images.append(
                        ctk_image
                    )

                    image_label = ctk.CTkLabel(
                        paper,
                        text="",
                        image=ctk_image
                    )

                    image_label.pack(
                        pady=5
                    )

                    image_label.bind(
                        "<Button-1>",
                        lambda event, n=notice:
                        self.open_notice(n)
                    )

                except Exception as e:

                    print(
                        "Image error:",
                        e
                    )

        # =================================================
        # DATE
        # =================================================

        display_date = self.get_display_date(
            notice.get("posted_at")
        )

        date_label = ctk.CTkLabel(
            paper,
            text=f"📅 {display_date}",
            font=("Arial", 8),
            text_color=self.get_color("date"),
            justify="center"
        )

        date_label.pack(
            side="bottom",
            pady=8
        )

        # =================================================
        # CLICKABLE PAPER
        # =================================================

        clickable_widgets = [
            paper,
            pin,
            title,
            audience_label,
            date_label
        ]

        if category:

            clickable_widgets.append(
                category_label
            )

        for widget in clickable_widgets:

            widget.bind(
                "<Button-1>",
                lambda event, n=notice:
                self.open_notice(n)
            )

    # =====================================================
    # OPEN FULL NOTICE
    # =====================================================

    def open_notice(self, notice):

        viewer = ctk.CTkToplevel(
            self.winfo_toplevel()
        )

        viewer.title(
            notice["title"]
        )

        viewer.geometry(
            "850x750"
        )

        viewer.configure(
            fg_color=self.get_color("viewer")
        )

        viewer.transient(
            self.winfo_toplevel()
        )

        # =================================================
        # HEADER
        # =================================================

        header = ctk.CTkFrame(
            viewer,
            height=70,
            corner_radius=0,
            fg_color=self.get_color("header")
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text=notice["title"],
            font=("Georgia", 22, "bold"),
            text_color="#FFF4D6" if self.current_theme == "Light" else "#FFFFFF",
            wraplength=650
        )

        title.pack(
            side="left",
            padx=25
        )

        # =================================================
        # CONTENT
        # =================================================

        content = ctk.CTkScrollableFrame(
            viewer,
            fg_color=self.get_color("viewer")
        )

        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # =================================================
        # AUDIENCE
        # =================================================

        audience = notice.get(
            "audience"
        )

        if not audience:

            audience = "Everyone"

        audience_label = ctk.CTkLabel(
            content,
            text=f"👥 Notice For: {audience}",
            font=("Arial", 14, "bold"),
            text_color=self.get_color("secondary"),
            wraplength=700
        )

        audience_label.pack(
            pady=(5, 15)
        )

        # =================================================
        # CATEGORY
        # =================================================

        category = notice.get(
            "category_name"
        )

        if category:

            category_label = ctk.CTkLabel(
                content,
                text=f"📂 Category: {category}",
                font=("Arial", 12, "bold"),
                text_color=self.get_color("secondary")
            )

            category_label.pack(
                pady=5
            )

        # =================================================
        # IMAGE
        # =================================================

        attachment = notice.get(
            "attachment"
        )

        if attachment:

            project_folder = os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )

            image_path = os.path.join(
                project_folder,
                attachment
            )

            if os.path.exists(image_path):

                try:

                    image = Image.open(
                        image_path
                    )

                    image.thumbnail(
                        (750, 500)
                    )

                    viewer_image = ctk.CTkImage(
                        light_image=image,
                        dark_image=image,
                        size=image.size
                    )

                    self.notice_images.append(
                        viewer_image
                    )

                    image_label = ctk.CTkLabel(
                        content,
                        text="",
                        image=viewer_image
                    )

                    image_label.pack(
                        pady=10
                    )

                except Exception as e:

                    print(
                        "Viewer image error:",
                        e
                    )

        # =================================================
        # DESCRIPTION
        # =================================================

        description = notice.get(
            "description"
        )

        if description:

            description_label = ctk.CTkLabel(
                content,
                text=description,
                font=("Arial", 16),
                text_color=self.get_color("text"),
                wraplength=700,
                justify="left"
            )

            description_label.pack(
                padx=30,
                pady=20
            )

        # =================================================
        # POSTED DATE
        # =================================================

        posted_date = self.get_display_date(
            notice.get("posted_at")
        )

        date_label = ctk.CTkLabel(
            content,
            text=f"📅 Posted:\n{posted_date}",
            font=("Arial", 12),
            text_color=self.get_color("date"),
            justify="center"
        )

        date_label.pack(
            pady=10
        )

        # =================================================
        # EXPIRY DATE
        # =================================================

        expiry_date = notice.get(
            "expiry_date"
        )

        if expiry_date:

            expiry_display = self.get_display_date(
                expiry_date
            )

            expiry_label = ctk.CTkLabel(
                content,
                text=f"⏳ Expires:\n{expiry_display}",
                font=("Arial", 12),
                text_color="#FF6666",
                justify="center"
            )

            expiry_label.pack(
                pady=(0, 10)
            )

        # =================================================
        # PRIORITY
        # =================================================

        if notice.get("priority") == "important":

            priority_label = ctk.CTkLabel(
                content,
                text="⚠ IMPORTANT NOTICE",
                font=("Arial", 13, "bold"),
                text_color="#FF5C5C"
            )

            priority_label.pack(
                pady=5
            )

        # =================================================
        # CLOSE
        # =================================================

        close_button = ctk.CTkButton(
            viewer,
            text="✕ Close",
            width=140,
            height=40,
            fg_color=self.get_color("button"),
            hover_color=self.get_color("button_hover"),
            command=viewer.destroy
        )

        close_button.pack(
            pady=(0, 20)
        )