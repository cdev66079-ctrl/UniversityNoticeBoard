from database import Database
import os


class Notice:

    def __init__(
        self,
        title,
        description=None,
        category_id=None,
        audience="Everyone",
        attachment=None,
        attachment_type="none",
        posted_by=1
    ):
        self.title = title
        self.description = description
        self.category_id = category_id

        # If admin leaves audience blank
        # automatically make it Everyone
        self.audience = (
            audience.strip()
            if audience and audience.strip()
            else "Everyone"
        )

        self.attachment = attachment
        self.attachment_type = attachment_type
        self.posted_by = posted_by

    # =====================================================
    # SAVE NOTICE
    # =====================================================

    def save(self):

        db = Database()

        if not db.connect():
            return False

        query = """
            INSERT INTO notices
            (
                title,
                description,
                category_id,
                audience,
                attachment,
                attachment_type,
                posted_by
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            self.title,
            self.description,
            self.category_id,
            self.audience,
            self.attachment,
            self.attachment_type,
            self.posted_by
        )

        try:

            cursor = db.connection.cursor()

            cursor.execute(
                query,
                values
            )

            db.connection.commit()

            self.notice_id = cursor.lastrowid

            cursor.close()
            db.close()

            print(
                "Notice saved successfully:",
                self.notice_id
            )

            return True

        except Exception as e:

            print(
                "Notice save error:",
                e
            )

            try:
                db.connection.rollback()
                db.close()
            except Exception:
                pass

            return False

    # =====================================================
    # GET ALL ACTIVE NOTICES
    # =====================================================

    @staticmethod
    def get_all():

        db = Database()

        if not db.connect():
            return []

        query = """
            SELECT
                n.notice_id,
                n.title,
                n.description,
                n.category_id,
                n.audience,
                n.attachment,
                n.attachment_type,
                n.priority,
                n.posted_by,
                n.posted_at,
                n.expiry_date,
                n.status,

                c.category_name

            FROM notices n

            LEFT JOIN categories c
                ON n.category_id = c.category_id

            WHERE n.status = 'active'

            ORDER BY n.posted_at DESC
        """

        try:

            cursor = db.connection.cursor(
                dictionary=True
            )

            cursor.execute(query)

            notices = cursor.fetchall()

            cursor.close()
            db.close()

            return notices

        except Exception as e:

            print(
                "Notice fetch error:",
                e
            )

            try:
                db.close()
            except Exception:
                pass

            return []

    # =====================================================
    # DELETE NOTICE
    # =====================================================

    @staticmethod
    def delete(notice_id):

        db = Database()

        if not db.connect():
            return False

        try:

            cursor = db.connection.cursor()

            # ---------------------------------------------
            # GET ATTACHMENT
            # ---------------------------------------------

            cursor.execute(
                """
                SELECT attachment
                FROM notices
                WHERE notice_id = %s
                """,
                (notice_id,)
            )

            result = cursor.fetchone()

            attachment = (
                result[0]
                if result
                else None
            )

            # ---------------------------------------------
            # DELETE DATABASE RECORD
            # ---------------------------------------------

            cursor.execute(
                """
                DELETE FROM notices
                WHERE notice_id = %s
                """,
                (notice_id,)
            )

            db.connection.commit()

            cursor.close()
            db.close()

            # ---------------------------------------------
            # DELETE ATTACHMENT FILE
            # ---------------------------------------------

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

                    os.remove(image_path)

                    print(
                        "Deleted attachment:",
                        image_path
                    )

            print(
                f"Notice {notice_id} deleted."
            )

            return True

        except Exception as e:

            print(
                "Notice delete error:",
                e
            )

            try:
                db.connection.rollback()
                db.close()
            except Exception:
                pass

            return False

    # =====================================================
    # EXPIRE OLD NOTICES
    # =====================================================

    @staticmethod
    def expire_old_notices():

        db = Database()

        if not db.connect():
            return False

        try:

            cursor = db.connection.cursor()

            query = """
                UPDATE notices

                SET status = 'expired'

                WHERE status = 'active'

                AND expiry_date IS NOT NULL

                AND expiry_date < CURDATE()
            """

            cursor.execute(query)

            db.connection.commit()

            expired_count = cursor.rowcount

            cursor.close()
            db.close()

            print(
                f"Expired {expired_count} old notice(s)."
            )

            return True

        except Exception as e:

            print(
                "Notice expiry error:",
                e
            )

            try:
                db.connection.rollback()
                db.close()
            except Exception:
                pass

            return False
