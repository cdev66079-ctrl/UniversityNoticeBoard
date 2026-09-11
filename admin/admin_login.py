import customtkinter as ctk
from tkinter import messagebox

from database import Database


class AdminLogin(ctk.CTkFrame):

    def __init__(self, parent, on_success, back_to_board):

        super().__init__(parent)

        self.on_success = on_success
        self.back_to_board = back_to_board

        self.configure(
            fg_color="#F2F2F2"
        )

        self.create_interface()

    # ==========================================
    # INTERFACE
    # ==========================================

    def create_interface(self):

        container = ctk.CTkFrame(
            self,
            width=450,
            height=500
        )

        container.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        container.pack_propagate(False)

        # ======================================
        # TITLE
        # ======================================

        ctk.CTkLabel(
            container,
            text="🔐 Admin Login",
            font=("Arial", 28, "bold")
        ).pack(
            pady=(45, 30)
        )

        # ======================================
        # EMAIL
        # ======================================

        ctk.CTkLabel(
            container,
            text="Admin Email",
            font=("Arial", 15, "bold")
        ).pack(
            anchor="w",
            padx=50
        )

        self.email_entry = ctk.CTkEntry(
            container,
            width=350,
            height=45,
            placeholder_text="admin@university.com"
        )

        self.email_entry.pack(
            pady=(5, 20)
        )

        # ======================================
        # PASSWORD
        # ======================================

        ctk.CTkLabel(
            container,
            text="Password",
            font=("Arial", 15, "bold")
        ).pack(
            anchor="w",
            padx=50
        )

        self.password_entry = ctk.CTkEntry(
            container,
            width=350,
            height=45,
            show="*"
        )

        self.password_entry.pack(
            pady=(5, 25)
        )

        # ======================================
        # LOGIN
        # ======================================

        ctk.CTkButton(
            container,
            text="🔐 LOGIN AS ADMIN",
            width=250,
            height=50,
            font=("Arial", 16, "bold"),
            command=self.login
        ).pack(
            pady=10
        )

        # ======================================
        # BACK
        # ======================================

        ctk.CTkButton(
            container,
            text="← Back to Notice Board",
            width=200,
            command=self.back_to_board
        ).pack(
            pady=15
        )

    # ==========================================
    # LOGIN
    # ==========================================

    def login(self):

        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not email or not password:

            messagebox.showwarning(
                "Missing Information",
                "Please enter email and password."
            )

            return

        db = Database()

        if not db.connect():

            messagebox.showerror(
                "Database Error",
                "Could not connect to database."
            )

            return

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
                WHERE email = %s
                AND password = %s
                AND role = 'admin'
                LIMIT 1
            """

            cursor.execute(
                query,
                (
                    email,
                    password
                )
            )

            user = cursor.fetchone()

            cursor.close()
            db.close()

            if user:

                print(
                    "Admin login successful:",
                    user["name"]
                )

                self.on_success(user)

            else:

                messagebox.showerror(
                    "Login Failed",
                    "Invalid admin email or password."
                )

        except Exception as e:

            print(
                "Admin login error:",
                e
            )

            try:
                db.close()
            except Exception:
                pass

            messagebox.showerror(
                "Error",
                f"Something went wrong:\n\n{e}"
            )