import json
import os


class AdminSession:

    SESSION_FILE = "admin_session.json"

    @staticmethod
    def save(user_id):
        data = {
            "user_id": user_id
        }

        with open(
            AdminSession.SESSION_FILE,
            "w"
        ) as file:

            json.dump(data, file)

    @staticmethod
    def get_user_id():

        if not os.path.exists(
            AdminSession.SESSION_FILE
        ):
            return None

        try:

            with open(
                AdminSession.SESSION_FILE,
                "r"
            ) as file:

                data = json.load(file)

            return data.get("user_id")

        except Exception:

            return None

    @staticmethod
    def clear():

        if os.path.exists(
            AdminSession.SESSION_FILE
        ):

            os.remove(
                AdminSession.SESSION_FILE
            )