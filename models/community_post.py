from database import Database
from utils.nepali_date import format_bs_datetime

class CommunityPost:

    def __init__(
        self,
        title,
        content="",
        category_id=None,
        attachment=None,
        attachment_type="none",
        posted_by=None,
        display_name=None,
        post_id=None,
        posted_at=None,
        status="active"
    ):
        self.post_id = post_id
        self.title = title
        self.content = content
        self.category_id = category_id
        self.attachment = attachment
        self.attachment_type = attachment_type
        self.posted_by = posted_by
        self.display_name = display_name
        self.posted_at = posted_at
        self.status = status

    # ==========================================
    # SAVE POST
    # ==========================================

    def save(self):

        db = Database()

        if not db.connect():
            return False

        try:

            cursor = db.connection.cursor()

            query = """
                INSERT INTO community_posts
                (
                    title,
                    content,
                    category_id,
                    attachment,
                    attachment_type,
                    posted_by,
                    display_name,
                    status
                )
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                self.title,
                self.content,
                self.category_id,
                self.attachment,
                self.attachment_type,
                self.posted_by,
                self.display_name,
                self.status
            )

            cursor.execute(
                query,
                values
            )

            db.connection.commit()

            self.post_id = cursor.lastrowid

            cursor.close()
            db.close()

            print(
                "Community post saved:",
                self.post_id
            )

            return True

        except Exception as e:

            print(
                "Community post save error:",
                e
            )

            try:
                db.connection.rollback()
                db.close()
            except Exception:
                pass

            return False

    # ==========================================
    # GET ALL APPROVED POSTS
    # ==========================================

    @staticmethod
    def get_all():

        db = Database()

        if not db.connect():
            return []

        try:

            cursor = db.connection.cursor(
                dictionary=True
            )

            query = """
                SELECT
                    cp.post_id,
                    cp.title,
                    cp.content,
                    cp.category_id,
                    cp.attachment,
                    cp.attachment_type,
                    cp.posted_by,
                    cp.display_name,
                    cp.posted_at,

                    COALESCE(
                        cp.display_name,
                        u.name,
                        'Anonymous'
                    ) AS poster_name,

                    c.category_name

                FROM community_posts cp

                LEFT JOIN users u
                    ON cp.posted_by = u.user_id

                LEFT JOIN categories c
                    ON cp.category_id = c.category_id

                WHERE cp.status = 'active'

                ORDER BY cp.posted_at DESC
            """

            cursor.execute(query)

            posts = cursor.fetchall()

            cursor.close()
            db.close()

            return posts

        except Exception as e:

            print(
                "Get community posts error:",
                e
            )

            try:
                db.close()
            except Exception:
                pass

            return []

    # ==========================================
    # DELETE POST
    # ==========================================

    def delete(self):

        db = Database()

        if not db.connect():
            return False

        try:

            cursor = db.connection.cursor()

            query = """
                DELETE FROM community_posts
                WHERE post_id = %s
            """

            cursor.execute(
                query,
                (self.post_id,)
            )

            db.connection.commit()

            cursor.close()
            db.close()

            print(
                f"Community post {self.post_id} deleted."
            )

            return True

        except Exception as e:

            print(
                "Community post delete error:",
                e
            )

            try:
                db.connection.rollback()
                db.close()
            except Exception:
                pass

            return False
    @staticmethod
    def archive_old_posts():

     db = Database()

     if not db.connect():
        return False

     try:

        cursor = db.connection.cursor()

        query = """
            UPDATE community_posts
            SET status = 'archived'
            WHERE status = 'active'
            AND posted_at < NOW() - INTERVAL 60 DAY
        """

        cursor.execute(query)

        db.connection.commit()

        archived_count = cursor.rowcount

        cursor.close()
        db.close()

        print(
            f"Archived {archived_count} old community post(s)."
        )

        return True

     except Exception as e:

        print(
            "Archive error:",
            e
        )

        try:
            db.connection.rollback()
            db.close()
        except Exception:
            pass

        return False