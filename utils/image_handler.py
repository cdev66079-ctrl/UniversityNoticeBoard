import os
import shutil
import uuid


class ImageHandler:

    @staticmethod
    def save_image(source_path):

        # Get the UniversityNoticeBoard project folder
        project_folder = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        # Path to assets/notices
        notice_folder = os.path.join(
            project_folder,
            "assets",
            "notices"
        )

        # Create folder only if it doesn't exist
        if not os.path.isdir(notice_folder):
            os.makedirs(notice_folder)

        # Get original file extension
        extension = os.path.splitext(source_path)[1]

        # Generate unique filename
        filename = f"notice_{uuid.uuid4().hex}{extension}"

        destination = os.path.join(
            notice_folder,
            filename
        )

        # Copy the image
        shutil.copy2(
            source_path,
            destination
        )

        print("Image saved to:", destination)

        # Return path relative to project folder
        return os.path.relpath(
            destination,
            project_folder
        )