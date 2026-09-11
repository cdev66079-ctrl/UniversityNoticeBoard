from database import Database


class CommunityComment:

    def __init__(
        self,
        post_id,
        display_name,
        comment_text,
        user_id=None,
        comment_id=None,
        commented_at=None
    ):

        self.comment_id = comment_id
        self.post_id = post_id
        self.user_id = user_id
        self.display_name = display_name
        self.comment_text = comment_text
        self.commented_at = commented_at

    # ==========================================
    # SAVE COMMENT
    # ==========================================

    def save(self):

        db = Database()

        if not db.connect():
            return False

        try:

            cursor = db.connection.cursor()

            query = """
                INSERT INTO community_comments
                (
                    post_id,
                    user_id,
                    display_name,
                    comment_text
                )
                VALUES
                (%s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (
                    self.post_id,
                    self.user_id,
                    self.display_name,
                    self.comment_text
                )
            )

            db.connection.commit()

            self.comment_id = cursor.lastrowid

            cursor.close()
            db.close()

            return True

        except Exception as e:

            print(
                "Comment save error:",
                e
            )

            try:
                db.connection.rollback()
                db.close()
            except Exception:
                pass

            return False

    # ==========================================
    # GET COMMENTS FOR POST
    # ==========================================

    @staticmethod
    def get_by_post(post_id):

        db = Database()

        if not db.connect():
            return []

        try:

            cursor = db.connection.cursor(
                dictionary=True
            )

            query = """
                SELECT
                    cc.comment_id,
                    cc.post_id,
                    cc.user_id,
                    cc.display_name,
                    cc.comment_text,
                    cc.commented_at,
                    COALESCE(
                        cc.display_name,
                        u.name,
                        'Anonymous'
                    ) AS commenter_name

                FROM community_comments cc

                LEFT JOIN users u
                    ON cc.user_id = u.user_id

                WHERE cc.post_id = %s

                ORDER BY cc.commented_at ASC
            """

            cursor.execute(
                query,
                (post_id,)
            )

            comments = cursor.fetchall()

            cursor.close()
            db.close()

            return comments

        except Exception as e:

            print(
                "Get comments error:",
                e
            )

            try:
                db.close()
            except Exception:
                pass

            return []