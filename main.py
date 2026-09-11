import customtkinter as ctk

from database import Database

from student.notice_board import NoticeBoard
from community.community_board import CommunityBoard

from admin.admin_dashboard import AdminDashboard
from admin.admin_login import AdminLogin
from admin.admin_session import AdminSession

from utils.theme import Theme


class UniversityNoticeBoardApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        # ==========================================
        # APPLICATION SETTINGS
        # ==========================================

        self.title(
            "University Notice Board"
        )

        self.geometry(
            "1200x800"
        )

        self.minsize(
            1000,
            700
        )

        # ==========================================
        # CURRENT USER
        # ==========================================

        self.current_user = None

        # ==========================================
        # DEFAULT THEME
        # ==========================================

        ctk.set_appearance_mode("Light")

        # ==========================================
        # OPEN PUBLIC NOTICE BOARD
        # ==========================================

        self.show_notice_board()

    # ==================================================
    # UNIVERSITY NOTICE BOARD
    # ==================================================

    def show_notice_board(self):

        self.clear_screen()

        board = NoticeBoard(
            self,
            open_admin=self.show_admin,
            open_community=self.show_community,
            current_user=self.current_user,
        )

        board.pack(
            fill="both",
            expand=True
        )

    # ==================================================
    # COMMUNITY BOARD
    # ==================================================

    def show_community(self):

        self.clear_screen()

        board = CommunityBoard(
            self,
            back_to_home=self.show_notice_board,
            current_user=self.current_user,
            toggle_dark_mode=self.toggle_dark_mode
        )

        board.pack(
            fill="both",
            expand=True
        )

    # ==================================================
    # ADMIN
    # ==================================================

    def show_admin(self):

        # ------------------------------------------
        # CHECK SAVED ADMIN SESSION
        # ------------------------------------------

        saved_user_id = AdminSession.get_user_id()

        if saved_user_id:

            user = self.get_admin_by_id(
                saved_user_id
            )

            if user:

                self.current_user = user

                print(
                    "Remembered admin:",
                    self.current_user
                )

                self.show_admin_dashboard()

                return

            else:

                AdminSession.clear()

        # ------------------------------------------
        # NO SAVED SESSION
        # ------------------------------------------

        self.clear_screen()

        login = AdminLogin(
            self,
            on_success=self.admin_login_success,
            back_to_board=self.show_notice_board,
            toggle_dark_mode=self.toggle_dark_mode
        )

        login.pack(
            fill="both",
            expand=True
        )

    # ==================================================
    # ADMIN LOGIN SUCCESS
    # ==================================================

    def admin_login_success(self, user):

        self.current_user = user

        # ------------------------------------------
        # SAVE ADMIN SESSION
        # ------------------------------------------

        AdminSession.save(
            user["user_id"]
        )

        print(
            "Admin logged in:",
            self.current_user
        )

        print(
            "Admin session saved."
        )

        self.show_admin_dashboard()

    # ==================================================
    # GET ADMIN FROM DATABASE
    # ==================================================

    def get_admin_by_id(self, user_id):

        db = Database()

        if not db.connect():

            return None

        try:

            cursor = db.connection.cursor(
                dictionary=True
            )

            query = """
                SELECT
                    user_id,
                    name,
                    email,
                    role
                FROM users
                WHERE user_id = %s
                AND role = 'admin'
                LIMIT 1
            """

            cursor.execute(
                query,
                (user_id,)
            )

            user = cursor.fetchone()

            cursor.close()

            db.close()

            return user

        except Exception as e:

            print(
                "Get admin error:",
                e
            )

            try:
                db.close()
            except Exception:
                pass

            return None

    # ==================================================
    # ADMIN DASHBOARD
    # ==================================================

    def show_admin_dashboard(self):

        self.clear_screen()

        admin = AdminDashboard(
            self,
            back_to_board=self.show_notice_board,
            current_user=self.current_user,
            toggle_dark_mode=self.toggle_dark_mode
        )

        admin.pack(
            fill="both",
            expand=True
        )

    # ==================================================
    # DARK MODE TOGGLE
    # ==================================================

    def toggle_dark_mode(self):

        new_mode = Theme.toggle()

        print(
            f"Theme changed to: {new_mode}"
        )

        # ------------------------------------------
        # RELOAD CURRENT SCREEN
        # ------------------------------------------
        #
        # CustomTkinter changes appearance mode,
        # but our screens contain custom colors.
        # Rebuilding the screen makes Theme.color()
        # apply to every widget.
        #
        # ------------------------------------------

        self.refresh_current_screen()

    # ==================================================
    # REFRESH CURRENT SCREEN
    # ==================================================

    def refresh_current_screen(self):

        # ------------------------------------------
        # NOTICE BOARD
        # ------------------------------------------

        # Determine which screen is currently active
        # using the widgets inside the application.

        for widget in self.winfo_children():

            if isinstance(widget, NoticeBoard):

                self.show_notice_board()
                return

            if isinstance(widget, CommunityBoard):

                self.show_community()
                return

            if isinstance(widget, AdminDashboard):

                self.show_admin_dashboard()
                return

            if isinstance(widget, AdminLogin):

                self.show_admin()
                return

    # ==================================================
    # CLEAR SCREEN
    # ==================================================

    def clear_screen(self):

        for widget in self.winfo_children():

            widget.destroy()


# ======================================================
# START APPLICATION
# ======================================================

if __name__ == "__main__":

    app = UniversityNoticeBoardApp()

    app.mainloop()