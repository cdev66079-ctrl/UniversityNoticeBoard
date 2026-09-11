from database import Database


class Submission:

    def __init__(
        self,
        title,
        description="",
        attachment=None,
        attachment_type=None,
        submitted_by=None,
        submitter_type="student",
        status="pending",
        submission_id=None,
        submitted_at=None,
        reviewed_at=None,
        reviewed_by=None
    ):

        self.submission_id = submission_id
        self.title = title
        self.description = description
        self.attachment = attachment
        self.attachment_type = attachment_type
        self.submitted_by = submitted_by
        self.submitter_type = submitter_type
        self.status = status
        self.submitted_at = submitted_at
        self.reviewed_at = reviewed_at
        self.reviewed_by = reviewed_by

    # =====================================================
    # SAVE SUBMISSION
    # =====================================================

    def save(self):

        db = Database()

        if not db.connect():
            return False

        try:

            cursor = db.connection.cursor()

            query = """
                INSERT INTO notice_submissions
                (
                    title,
                    description,
                    attachment,
                    attachment_type,
                    submitted_by,
                    submitter_type,
                    status
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """

            values = (
                self.title,
                self.description,
                self.attachment,
                self.attachment_type,
                self.submitted_by,
                self.submitter_type,
                "pending"
            )

            cursor.execute(
                query,
                values
            )

            db.connection.commit()

            self.submission_id = cursor.lastrowid

            cursor.close()
            db.close()

            print(
                "Submission saved:",
                self.submission_id
            )

            return True

        except Exception as e:

            print(
                "Submission save error:",
                e
            )

            try:
                db.connection.rollback()
                db.close()
            except:
                pass

            return False

    # =====================================================
    # GET ALL SUBMISSIONS
    # =====================================================

    @staticmethod
    def get_all():

        db = Database()

        if not db.connect():
            return []

        try:

            cursor = db.connection.cursor(
                dictionary=True
            )

            cursor.execute(
                """
                SELECT *
                FROM notice_submissions
                ORDER BY submitted_at DESC
                """
            )

            submissions = cursor.fetchall()

            cursor.close()
            db.close()

            return submissions

        except Exception as e:

            print(
                "Get submissions error:",
                e
            )

            try:
                db.close()
            except:
                pass

            return []

    # =====================================================
    # GET PENDING SUBMISSIONS
    # =====================================================

    @staticmethod
    def get_pending():

        db = Database()

        if not db.connect():
            return []

        try:

            cursor = db.connection.cursor(
                dictionary=True
            )

            cursor.execute(
                """
                SELECT *
                FROM notice_submissions
                WHERE status = 'pending'
                ORDER BY submitted_at DESC
                """
            )

            submissions = cursor.fetchall()

            cursor.close()
            db.close()

            return submissions

        except Exception as e:

            print(
                "Get pending submissions error:",
                e
            )

            try:
                db.close()
            except:
                pass

            return []

    # =====================================================
    # APPROVE SUBMISSION
    # =====================================================

    @staticmethod
    def approve(
        submission_id,
        reviewed_by=None
    ):

        db = Database()

        if not db.connect():
            return False

        try:

            cursor = db.connection.cursor(
                dictionary=True
            )

            # Get submission

            cursor.execute(
                """
                SELECT *
                FROM notice_submissions
                WHERE submission_id = %s
                """,
                (submission_id,)
            )

            submission = cursor.fetchone()

            if not submission:

                cursor.close()
                db.close()

                return False

            # Change status

            cursor.execute(
                """
                UPDATE notice_submissions
                SET
                    status = 'approved',
                    reviewed_at = NOW(),
                    reviewed_by = %s
                WHERE submission_id = %s
                """,
                (
                    reviewed_by,
                    submission_id
                )
            )

            db.connection.commit()

            cursor.close()
            db.close()

            return True

        except Exception as e:

            print(
                "Approve submission error:",
                e
            )

            try:
                db.connection.rollback()
                db.close()
            except:
                pass

            return False

    # =====================================================
    # REJECT SUBMISSION
    # =====================================================

    @staticmethod
    def reject(
        submission_id,
        reviewed_by=None
    ):

        db = Database()

        if not db.connect():
            return False

        try:

            cursor = db.connection.cursor()

            cursor.execute(
                """
                UPDATE notice_submissions
                SET
                    status = 'rejected',
                    reviewed_at = NOW(),
                    reviewed_by = %s
                WHERE submission_id = %s
                """,
                (
                    reviewed_by,
                    submission_id
                )
            )

            db.connection.commit()

            cursor.close()
            db.close()

            return True

        except Exception as e:

            print(
                "Reject submission error:",
                e
            )

            try:
                db.connection.rollback()
                db.close()
            except:
                pass

            return False