import os

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import (
    User,
    Notice,
    CommunityPost,
    CommunityComment,
    NoticeImage,     
    Category,
    Notification,
    NotificationRead,
)
from django.conf import settings
import os
from django.utils import timezone
from django.db.models import Q
import random
import uuid
from django.http import JsonResponse
from .services.ai_notice import generate_notice_from_file

from django.contrib.auth.hashers import check_password, make_password
import nepali_datetime
import socket
from django.db import connection

# =========================================================
# COMMUNITY PAPER STYLES
# =========================================================

COMMUNITY_PAPER_STYLES = [
    "sticky-yellow",
    "sticky-pink",
    "sticky-blue",
    "sticky-green",
    "y2k-purple",
    "ripped-paper",
    "notebook",
    "polaroid",
    "newspaper",
    "meme",
    "ticket",
    "doodle",
]
def style_community_posts(posts):
    for post in posts:
        if not post.paper_style:
            post.paper_style = random.choice(
                COMMUNITY_PAPER_STYLES
            )

    return posts
def get_bs_date(gregorian_datetime):
    """
    Convert a Gregorian datetime/date into a readable
    Bikram Sambat date.
    """

    if not gregorian_datetime:
        return None

    # Convert Django datetime to Gregorian date
    if hasattr(gregorian_datetime, "date"):
        gregorian_date = gregorian_datetime.date()
    else:
        gregorian_date = gregorian_datetime

    # Convert Gregorian date to BS
    bs_date = nepali_datetime.date.from_datetime_date(
        gregorian_date
    )

    # Nepali month names
    nepali_months = {
        1: "Baisakh",
        2: "Jestha",
        3: "Ashadh",
        4: "Shrawan",
        5: "Bhadra",
        6: "Ashwin",
        7: "Kartik",
        8: "Mangsir",
        9: "Poush",
        10: "Magh",
        11: "Falgun",
        12: "Chaitra",
    }

    month_name = nepali_months.get(
        bs_date.month,
        ""
    )

    return {
        "year": bs_date.year,
        "month": bs_date.month,
        "month_name": month_name,
        "day": bs_date.day,
        "formatted": (
            f"{bs_date.year} "
            f"{month_name} "
            f"{bs_date.day}"
        ),
    }
def home(request):

    notices = list(
        Notice.objects
        .filter(status="active")
        .order_by("-posted_at")[:5]
    )

    for notice in notices:

        # BS date
        notice.bs_date = get_bs_date(notice.posted_at)

        # Category
        notice.public_category = None

        if notice.category_id:
            category = Category.objects.filter(
                category_id=notice.category_id
            ).first()

            if category:
                notice.public_category = category.category_name

        # Image
        image = (
            NoticeImage.objects
            .filter(notice_id=notice.notice_id)
            .order_by("image_id")
            .first()
        )

        notice.public_image = (
            image.image_path
            if image
            else None
        )

    community_posts = list(
        CommunityPost.objects
        .filter(status="active")
        .order_by("-posted_at")[:3]
    )

    # your existing community processing here...

    return render(
        request,
        "notices/home.html",
        {
            "notices": notices,
            "community_posts": community_posts,
        }
    )
    # =====================================================
    # COMMUNITY POSTS
    # NO CATEGORY
    # =====================================================

    community_posts = list(
        CommunityPost.objects
        .filter(status="active")
        .order_by("-posted_at")[:3]
    )

    for post in community_posts:

        # Image attachment
        post.public_image = None

        if (
            post.attachment
            and post.attachment_type == "image"
        ):
            post.public_image = post.attachment

        # BS + AD Date
        post.bs_date = get_bs_date(
            post.posted_at
        )

        # Comment count
        post.comment_count = (
            CommunityComment.objects
            .filter(
                post_id=post.post_id
            )
            .count()
        )

    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        "notices/home.html",
        {
            "notices": notices,
            "community_posts": community_posts,
        }
    )
# =========================================================
# UNIVERSITY NOTICE BOARD
# =========================================================
def notices_page(request):

    notices = (
        Notice.objects
        .filter(status="active")
        .order_by("-posted_at")
    )

    categories = (
        Category.objects
        .all()
        .order_by("category_name")
    )

    for notice in notices:

        notice.images = (
            NoticeImage.objects
            .filter(
                notice_id=notice.notice_id
            )
            .order_by("image_id")
        )

        if notice.post_type == "image":

            first_image = notice.images.first()

            notice.board_image = (
                first_image.image_path
                if first_image
                else None
            )

    return render(
        request,
        "notices/notices.html",
        {
            "notices": notices,
            "categories": categories,
        }
    )
# =========================================================
# UNIVERSITY NOTICE DETAIL
# =========================================================


def notice_detail(request, notice_id):

    notice = get_object_or_404(
        Notice,
        notice_id=notice_id,
        status="active"
    )

    # -------------------------------------------------
    # DATE
    # -------------------------------------------------

    notice.bs_date = get_bs_date(notice.posted_at)

    # -------------------------------------------------
    # CATEGORY
    # -------------------------------------------------

    notice.public_category = None

    if notice.category_id:

        category = Category.objects.filter(
            category_id=notice.category_id
        ).first()

        if category:
            notice.public_category = category.category_name

    # -------------------------------------------------
    # IMAGES
    # -------------------------------------------------

    images = list(
        NoticeImage.objects
        .filter(notice_id=notice.notice_id)
        .order_by("image_id")
    )

    notice.public_image = (
        images[0].image_path
        if images
        else None
    )

    # -------------------------------------------------
    # IMAGE-ONLY NOTICE
    # -------------------------------------------------

    image_pin = (
        notice.post_type == "image"
        and notice.public_image
    )

    return render(
        request,
        "notices/notice_detail.html",
        {
            "notice": notice,
            "images": images,
            "image_pin": image_pin,
        }
    )
def community_board(request):
    posts = CommunityPost.objects.filter(
        status="active"
    ).order_by("-posted_at")

    for post in posts:
        # Category is no longer used for Community
        post.public_category = None

        # Image
        post.public_image = (
            post.attachment
            if post.attachment_type == "image" and post.attachment
            else None
        )

        # Comment count
        post.comment_count = CommunityComment.objects.filter(
            post_id=post.post_id
        ).count()

    return render(
        request,
        "notices/community_board.html",
        {
            "posts": posts,
        }
    )
#=================================================
# CREATE COMMUNITY POST
# ANYONE CAN POST
# =========================================================
# =========================================================
# CREATE COMMUNITY POST
# ANYONE CAN POST
# NO CATEGORY
# =========================================================

def create_community_post(request):

    if request.method == "POST":

        post_type = request.POST.get(
            "post_type",
            "text"
        ).strip()

        uploaded_file = request.FILES.get(
            "attachment"
        )

        # =====================================================
        # IMAGE PIN
        # =====================================================

        if post_type == "image":

            if not uploaded_file:

                return render(
                    request,
                    "notices/create_community_post.html",
                    {
                        "error":
                            "Please select an image."
                    }
                )

            content_type = (
                uploaded_file.content_type or ""
            ).lower()

            allowed_images = {
                "image/jpeg",
                "image/jpg",
                "image/png",
                "image/webp",
                "image/gif",
                "image/bmp",
                "image/tiff",
            }

            if content_type not in allowed_images:

                return render(
                    request,
                    "notices/create_community_post.html",
                    {
                        "error":
                            "Only image files are allowed."
                    }
                )

            # ---------------------------------------------
            # SAVE IMAGE
            # ---------------------------------------------

            upload_dir = (
                settings.MEDIA_ROOT
                / "community"
                / "images"
            )

            upload_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            filename = os.path.basename(
                uploaded_file.name
            )

            base_name, extension = os.path.splitext(
                filename
            )

            base_name = (
                base_name
                .strip()
                .replace(" ", "_")
                .replace("/", "_")
                .replace("\\", "_")
            )

            extension = extension.lower()

            final_filename = (
                f"{base_name}{extension}"
            )

            counter = 1

            while (
                upload_dir / final_filename
            ).exists():

                final_filename = (
                    f"{base_name}_{counter}"
                    f"{extension}"
                )

                counter += 1

            file_path = (
                upload_dir / final_filename
            )

            with open(
                file_path,
                "wb+"
            ) as destination:

                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            attachment_path = (
                "/media/community/images/"
                f"{final_filename}"
            )

            # ---------------------------------------------
            # CREATE IMAGE POST
            # ---------------------------------------------

            CommunityPost.objects.create(

                title="Image Pin",

                content=None,

                category_id=None,

                attachment=attachment_path,

                attachment_type="image",

                posted_by=None,

                display_name=None,

                status="active",

                posted_at=timezone.now(),

                post_type="image",

                paper_style="image-pin",
            )

            messages.success(
                request,
                "Image pinned to Community Board."
            )

            return redirect(
                "community"
            )

        # =====================================================
        # NORMAL COMMUNITY NOTE
        # =====================================================

        title = request.POST.get(
            "title",
            ""
        ).strip()

        content = request.POST.get(
            "content",
            ""
        ).strip()

        display_name = request.POST.get(
            "display_name",
            ""
        ).strip()

        uploaded_file = request.FILES.get(
            "attachment"
        )

        if not title:

            return render(
                request,
                "notices/create_community_post.html",
                {
                    "error":
                        "Post title is required."
                }
            )

        if not display_name:

            return render(
                request,
                "notices/create_community_post.html",
                {
                    "error":
                        "Your name or club name is required."
                }
            )

        if not content:

            return render(
                request,
                "notices/create_community_post.html",
                {
                    "error":
                        "Post content is required."
                }
            )

        attachment_path = None
        attachment_type = "none"

        # ---------------------------------------------
        # OPTIONAL NORMAL POST FILE
        # ---------------------------------------------

        if uploaded_file:

            content_type = (
                uploaded_file.content_type or ""
            ).lower()

            if content_type.startswith(
                "image/"
            ):

                upload_dir = (
                    settings.MEDIA_ROOT
                    / "community"
                    / "images"
                )

                attachment_type = "image"

            elif content_type == "application/pdf":

                upload_dir = (
                    settings.MEDIA_ROOT
                    / "community"
                    / "pdfs"
                )

                attachment_type = "pdf"

            else:

                return render(
                    request,
                    "notices/create_community_post.html",
                    {
                        "error":
                            "Only images and PDF files are allowed."
                    }
                )

            upload_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            filename = os.path.basename(
                uploaded_file.name
            )

            base_name, extension = os.path.splitext(
                filename
            )

            base_name = (
                base_name
                .strip()
                .replace(" ", "_")
                .replace("/", "_")
                .replace("\\", "_")
            )

            extension = extension.lower()

            final_filename = (
                f"{base_name}{extension}"
            )

            counter = 1

            while (
                upload_dir / final_filename
            ).exists():

                final_filename = (
                    f"{base_name}_{counter}"
                    f"{extension}"
                )

                counter += 1

            file_path = (
                upload_dir / final_filename
            )

            with open(
                file_path,
                "wb+"
            ) as destination:

                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            if attachment_type == "image":

                attachment_path = (
                    "/media/community/images/"
                    f"{final_filename}"
                )

            else:

                attachment_path = (
                    "/media/community/pdfs/"
                    f"{final_filename}"
                )

        # ---------------------------------------------
        # CREATE NORMAL COMMUNITY POST
        # ---------------------------------------------

        CommunityPost.objects.create(

            title=title,

            content=content,

            category_id=None,

            attachment=attachment_path,

            attachment_type=attachment_type,

            posted_by=None,

            display_name=display_name,

            status="active",

            posted_at=timezone.now(),

            post_type="text",

            paper_style="sticky-yellow",
        )

        messages.success(
            request,
            "Community post published successfully."
        )

        return redirect(
            "community"
        )

    return render(
        request,
        "notices/create_community_post.html"
    )
# =========================================================
# COMMUNITY POST EDIT
# =========================================================
def edit_community_post(request, post_id):

    # =====================================================
    # GET POST
    # =====================================================

    post = get_object_or_404(
        CommunityPost,
        post_id=post_id,
        status="active"
    )

    # =====================================================
    # CHECK OWNER
    # =====================================================

    owner_token = request.session.get(
        f"community_post_{post_id}"
    )

    if (
        not owner_token
        or owner_token != post.owner_token
    ):

        messages.error(
            request,
            "You are not allowed to edit this post."
        )

        return redirect(
            "community_detail",
            post_id=post_id
        )

    # =====================================================
    # SAVE
    # =====================================================

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        content = request.POST.get(
            "content",
            ""
        ).strip()

        if not title:

            return render(
                request,
                "notices/edit_community_post.html",
                {
                    "post": post,
                    "error": "Post title is required."
                }
            )

        if not content:

            return render(
                request,
                "notices/edit_community_post.html",
                {
                    "post": post,
                    "error": "Post content is required."
                }
            )

        # =================================================
        # UPDATE
        # =================================================

        post.title = title
        post.content = content

        post.save(
            update_fields=[
                "title",
                "content",
            ]
        )

        messages.success(
            request,
            "Your community post has been updated."
        )

        return redirect(
            "community_detail",
            post_id=post_id
        )

    # =====================================================
    # GET EDIT PAGE
    # =====================================================

    return render(
        request,
        "notices/edit_community_post.html",
        {
            "post": post,
        }
    )
# =========================================================
# COMMUNITY POST DELETE
# =========================================================

def delete_community_post(request, post_id):

    post = get_object_or_404(
        CommunityPost,
        post_id=post_id,
        status="active"
    )

    owner_token = request.session.get(
        f"community_post_{post_id}"
    )

    if not owner_token or owner_token != post.owner_token:
        messages.error(
            request,
            "You are not allowed to delete this post."
        )
        return redirect(
            "community_detail",
            post_id=post_id
        )

    if request.method == "POST":

        post.delete()

        request.session.pop(
            f"community_post_{post_id}",
            None
        )

        messages.success(
            request,
            "Your community post has been deleted."
        )

        return redirect("community")

    return redirect(
        "community_detail",
        post_id=post_id
    )
def community_detail(request, post_id):

    post = get_object_or_404(
        CommunityPost,
        post_id=post_id,
        status="active"
    )

    if post.post_type == "image":

        return redirect(
            "community"
        )

    comments = (
        CommunityComment.objects
        .filter(
            post_id=post_id
        )
        .order_by("-commented_at")
    )

    return render(
        request,
        "notices/community_detail.html",
        {
            "post": post,
            "comments": comments,
        }
    )
#=========================================================
#community comment
#=========================================================
def add_community_comment(request, post_id):

    if request.method != "POST":
        return redirect(
            "community_detail",
            post_id=post_id
        )

    post = get_object_or_404(
        CommunityPost,
        post_id=post_id,
        status="active"
    )

    display_name = request.POST.get(
        "display_name",
        ""
    ).strip()

    comment_text = request.POST.get(
        "comment_text",
        ""
    ).strip()

    # =====================================================
    # VALIDATION
    # =====================================================

    if not display_name:
        return redirect(
            "community_detail",
            post_id=post_id
        )

    if not comment_text:
        return redirect(
            "community_detail",
            post_id=post_id
        )

    # =====================================================
    # LIMIT
    # =====================================================

    display_name = display_name[:150]
    comment_text = comment_text[:2000]

    # =====================================================
    # CREATE COMMENT
    # =====================================================

    CommunityComment.objects.create(
        post_id=post.post_id,
        user_id=None,
        display_name=display_name,
        comment_text=comment_text,
        commented_at=timezone.now(),
    )

    return redirect(
        "community_detail",
        post_id=post_id
    )
# =========================================================
# ADMIN LOGIN
# =========================================================
def admin_login(request):

    # Already logged in
    if request.session.get("admin_id"):
        return redirect("admin_dashboard")

    error = None

    if request.method == "POST":

        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if not email or not password:
            error = "Email and password are required."

        else:
            user = (
                User.objects
                .filter(
                    email=email,
                    role="admin"
                )
                .first()
            )

            if not user:
                error = "Invalid admin email or password."

            else:

                password_valid = False

                # New hashed passwords
                if user.password and user.password.startswith(
                    ("pbkdf2_", "argon2", "bcrypt")
                ):
                    password_valid = check_password(
                        password,
                        user.password
                    )

                # Old plaintext password
                else:
                    password_valid = (
                        user.password == password
                    )

                    # Automatically upgrade old password
                    if password_valid:
                        user.password = make_password(password)

                        user.save(
                            update_fields=["password"]
                        )

                if password_valid:

                    # Store admin session
                    request.session["admin_id"] = user.user_id
                    request.session["admin_name"] = user.name

                    # Session expires when browser closes
                    request.session.set_expiry(0)

                    return redirect("admin_dashboard")

                else:
                    error = "Invalid admin email or password."

    return render(
        request,
        "notices/admin_login.html",
        {
            "error": error
        }
    )
# =========================================================
# ADMIN DASHBOARD
# =========================================================
def admin_dashboard(request):
    if not request.session.get("admin_id"):
        return redirect("admin_login")

    total_notices = Notice.objects.count()
    active_notices = Notice.objects.filter(status="active").count()

    total_community_posts = CommunityPost.objects.count()
    active_community_posts = CommunityPost.objects.filter(status="active").count()

    total_comments = CommunityComment.objects.count()
    total_categories = Category.objects.count()

    # Recent university notices
    recent_notices = list(
        Notice.objects
        .order_by("-posted_at")[:5]
    )

    # Attach first image to each notice
    for notice in recent_notices:
        image = (
            NoticeImage.objects
            .filter(notice_id=notice.notice_id)
            .order_by("image_id")
            .first()
        )
        notice.dashboard_image = image.image_path if image else None

        # Get category name
        category = None
        if notice.category_id:
            category = Category.objects.filter(
                category_id=notice.category_id
            ).first()

        notice.dashboard_category = (
            category.category_name if category else "General"
        )

    recent_posts = (
        CommunityPost.objects
        .order_by("-posted_at")[:5]
    )

    context = {
        "total_notices": total_notices,
        "active_notices": active_notices,
        "total_community_posts": total_community_posts,
        "active_community_posts": active_community_posts,
        "total_comments": total_comments,
        "total_categories": total_categories,

        "recent_notices": recent_notices,
        "recent_posts": recent_posts,

        "admin_name": request.session.get(
            "admin_name",
            "Administrator"
        ),
    }

    return render(
        request,
        "notices/admin_dashboard.html",
        context
    )
# =========================================================
# NOTIFICATIONS
# =========================================================

def mark_notification_read(request, notification_id):

    notification = get_object_or_404(
        Notification,
        notification_id=notification_id
    )

    # Create browser/session identifier
    if not request.session.session_key:
        request.session.create()

    browser_key = request.session.session_key

    # Mark as read
    NotificationRead.objects.get_or_create(
        notification_id=notification.notification_id,
        browser_key=browser_key,
        defaults={
            "read_at": timezone.now()
        }
    )

    # Open the related notice
    if notification.notice_id:

        return redirect(
            "notice_detail",
            notice_id=notification.notice_id
        )

    return redirect("home")


def mark_all_notifications_read(request):

    if not request.session.session_key:
        request.session.create()

    browser_key = request.session.session_key

    notifications = Notification.objects.all()

    for notification in notifications:

        NotificationRead.objects.get_or_create(
            notification_id=notification.notification_id,
            browser_key=browser_key,
            defaults={
                "read_at": timezone.now()
            }
        )

    return redirect(request.META.get("HTTP_REFERER", "home"))
# =========================================================
# ADMIN LOGOUT
# =========================================================
def admin_logout(request):

    request.session.flush()

    return redirect("admin_login")

# =========================================================
# ADMIN NOTICE MANAGEMENT
# =========================================================
def admin_notices(request):

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    notices = (
        Notice.objects
        .all()
        .order_by("-posted_at")
    )

    for notice in notices:

        notice.board_image = None

        if notice.post_type == "image":

            image = (
                NoticeImage.objects
                .filter(
                    notice_id=notice.notice_id
                )
                .order_by("image_id")
                .first()
            )

            if image:
                notice.board_image = (
                    image.image_path
                )

    return render(
        request,
        "notices/admin_notices.html",
        {
            "notices": notices,
        }
    )
# =========================================================
# ADMIN EDIT NOTICE
# =========================================================

def admin_edit_notice(request, notice_id):

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    notice = get_object_or_404(
        Notice,
        notice_id=notice_id
    )

    categories = (
        Category.objects
        .all()
        .order_by("category_name")
    )

    # -----------------------------------------------------
    # SAVE CHANGES
    # -----------------------------------------------------

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        category_id = request.POST.get(
            "category_id",
            ""
        ).strip()

        priority = request.POST.get(
            "priority",
            "normal"
        ).strip()

        audience = request.POST.get(
            "audience",
            "Everyone"
        ).strip()

        if not title:

            messages.error(
                request,
                "Notice title is required."
            )

            return redirect(
                "admin_edit_notice",
                notice_id=notice_id
            )

        # -------------------------------------------------
        # UPDATE BASIC INFORMATION
        # -------------------------------------------------

        notice.title = title
        notice.description = description
        notice.priority = priority
        notice.audience = audience

        if category_id:
            notice.category_id = int(category_id)
        else:
            notice.category_id = None

        notice.save()

        messages.success(
            request,
            "Notice updated successfully."
        )

        return redirect("admin_notices")

    # -----------------------------------------------------
    # EXISTING IMAGES
    # -----------------------------------------------------

    images = (
        NoticeImage.objects
        .filter(
            notice_id=notice.notice_id
        )
        .order_by("image_id")
    )

    return render(
        request,
        "notices/admin_edit_notice.html",
        {
            "notice": notice,
            "categories": categories,
            "images": images,
        }
    )
# =========================================================
# ADMIN DELETE UNIVERSITY NOTICE
# =========================================================

def admin_delete_notice(request, notice_id):

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    if request.method != "POST":
        return redirect("admin_notices")

    notice = get_object_or_404(
        Notice,
        notice_id=notice_id
    )

    # Delete associated images
    NoticeImage.objects.filter(
        notice_id=notice.notice_id
    ).delete()

    # Delete notice
    notice.delete()

    messages.success(
        request,
        "University notice deleted successfully."
    )

    return redirect("admin_notices")
# =========================================================
# ADMIN CREATE UNIVERSITY NOTICE
# ==============================
def admin_create_notice(request):

    # =====================================================
    # ADMIN SECURITY
    # =====================================================

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    categories = (
        Category.objects
        .all()
        .order_by("category_name")
    )

    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        post_type = request.POST.get(
            "post_type",
            "text"
        ).strip()

        # =================================================
        # IMAGE PIN
        # =================================================

        if post_type == "image":

            image_files = request.FILES.getlist("images")

            # Exactly one image
            if len(image_files) != 1:

                return render(
                    request,
                    "notices/admin_create_notice.html",
                    {
                        "categories": categories,
                        "error":
                            "Image Pin requires exactly one image."
                    }
                )

            image = image_files[0]

            # ---------------------------------------------
            # VALIDATE IMAGE
            # ---------------------------------------------

            content_type = (
                image.content_type or ""
            ).lower()

            allowed_images = {
                "image/jpeg",
                "image/jpg",
                "image/png",
                "image/webp",
                "image/gif",
                "image/bmp",
                "image/tiff",
            }

            if content_type not in allowed_images:

                return render(
                    request,
                    "notices/admin_create_notice.html",
                    {
                        "categories": categories,
                        "error":
                            "Only image files are allowed."
                    }
                )

            # ---------------------------------------------
            # SAVE IMAGE
            # ---------------------------------------------

            upload_dir = (
                settings.MEDIA_ROOT
                / "notices"
                / "images"
            )

            upload_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            filename = os.path.basename(image.name)

            base_name, extension = os.path.splitext(
                filename
            )

            base_name = (
                base_name
                .strip()
                .replace(" ", "_")
                .replace("/", "_")
                .replace("\\", "_")
            )

            extension = extension.lower()

            final_filename = (
                f"{base_name}{extension}"
            )

            counter = 1

            while (
                upload_dir / final_filename
            ).exists():

                final_filename = (
                    f"{base_name}_{counter}"
                    f"{extension}"
                )

                counter += 1

            file_path = (
                upload_dir / final_filename
            )

            with open(
                file_path,
                "wb+"
            ) as destination:

                for chunk in image.chunks():
                    destination.write(chunk)

            image_path = (
                "/media/notices/images/"
                f"{final_filename}"
            )

            # ---------------------------------------------
            # CREATE IMAGE PIN NOTICE
            # ---------------------------------------------

            notice = Notice.objects.create(

                title="Image Pin",

                description=None,

                category_id=None,

                attachment=None,

                attachment_type="none",

                posted_by=request.session.get(
                    "admin_id"
                ),

                priority="normal",

                audience="Everyone",

                status="active",

                post_type="image",

                posted_at=timezone.now(),
            )

            # ---------------------------------------------
            # SAVE NOTICE IMAGE
            # ---------------------------------------------

            NoticeImage.objects.create(
                notice_id=notice.notice_id,
                image_path=image_path,
                uploaded_at=timezone.now(),
            )

            # ---------------------------------------------
            # NOTIFICATION
            # ---------------------------------------------

            Notification.objects.create(
                title="New University Notice",
                message="A new image has been pinned.",
                notice_id=notice.notice_id,
                created_at=timezone.now(),
            )

            messages.success(
                request,
                "Image pinned to University Board."
            )

            return redirect("admin_dashboard")


        # =================================================
        # NORMAL OFFICIAL NOTICE
        # =================================================

        title = request.POST.get(
            "title",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        category_id = request.POST.get(
            "category_id"
        )

        priority = request.POST.get(
            "priority",
            "normal"
        )

        audience = request.POST.get(
            "audience",
            "Everyone"
        ).strip()

        image_files = request.FILES.getlist(
            "images"
        )

        pdf_file = request.FILES.get(
            "attachment"
        )

        # ---------------------------------------------
        # TITLE VALIDATION
        # ---------------------------------------------

        if not title:

            return render(
                request,
                "notices/admin_create_notice.html",
                {
                    "categories": categories,
                    "error":
                        "Notice title is required."
                }
            )

        # ---------------------------------------------
        # IMAGE LIMIT
        # ---------------------------------------------

        if len(image_files) > 5:

            return render(
                request,
                "notices/admin_create_notice.html",
                {
                    "categories": categories,
                    "error":
                        "You can upload a maximum of 5 images."
                }
            )

        # ---------------------------------------------
        # IMAGE VALIDATION
        # ---------------------------------------------

        for image in image_files:

            content_type = (
                image.content_type or ""
            ).lower()

            if not content_type.startswith("image/"):

                return render(
                    request,
                    "notices/admin_create_notice.html",
                    {
                        "categories": categories,
                        "error":
                            "Only image files are allowed."
                    }
                )

        # ---------------------------------------------
        # PDF
        # ---------------------------------------------

        attachment_path = None
        attachment_type = "none"

        if pdf_file:

            if (
                pdf_file.content_type
                != "application/pdf"
            ):

                return render(
                    request,
                    "notices/admin_create_notice.html",
                    {
                        "categories": categories,
                        "error":
                            "The attachment must be a PDF."
                    }
                )

            upload_dir = (
                settings.MEDIA_ROOT
                / "notices"
                / "pdfs"
            )

            upload_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            filename = os.path.basename(
                pdf_file.name
            )

            base_name, extension = os.path.splitext(
                filename
            )

            base_name = (
                base_name
                .strip()
                .replace(" ", "_")
                .replace("/", "_")
                .replace("\\", "_")
            )

            extension = extension.lower()

            final_filename = (
                f"{base_name}{extension}"
            )

            counter = 1

            while (
                upload_dir / final_filename
            ).exists():

                final_filename = (
                    f"{base_name}_{counter}"
                    f"{extension}"
                )

                counter += 1

            file_path = (
                upload_dir / final_filename
            )

            with open(
                file_path,
                "wb+"
            ) as destination:

                for chunk in pdf_file.chunks():
                    destination.write(chunk)

            attachment_path = (
                "/media/notices/pdfs/"
                f"{final_filename}"
            )

            attachment_type = "pdf"

        # ---------------------------------------------
        # CREATE NORMAL NOTICE
        # ---------------------------------------------

        notice = Notice.objects.create(

            title=title,

            description=description,

            category_id=(
                int(category_id)
                if category_id
                else None
            ),

            attachment=attachment_path,

            attachment_type=attachment_type,

            posted_by=request.session.get(
                "admin_id"
            ),

            priority=priority,

            audience=(
                audience or "Everyone"
            ),

            status="active",

            post_type="text",

            posted_at=timezone.now(),
        )

        # ---------------------------------------------
        # SAVE NORMAL NOTICE IMAGES
        # ---------------------------------------------

        for image in image_files:

            upload_dir = (
                settings.MEDIA_ROOT
                / "notices"
                / "images"
            )

            upload_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            filename = os.path.basename(
                image.name
            )

            base_name, extension = os.path.splitext(
                filename
            )

            base_name = (
                base_name
                .strip()
                .replace(" ", "_")
                .replace("/", "_")
                .replace("\\", "_")
            )

            extension = extension.lower()

            final_filename = (
                f"{base_name}{extension}"
            )

            counter = 1

            while (
                upload_dir / final_filename
            ).exists():

                final_filename = (
                    f"{base_name}_{counter}"
                    f"{extension}"
                )

                counter += 1

            file_path = (
                upload_dir / final_filename
            )

            with open(
                file_path,
                "wb+"
            ) as destination:

                for chunk in image.chunks():
                    destination.write(chunk)

            image_path = (
                "/media/notices/images/"
                f"{final_filename}"
            )

            NoticeImage.objects.create(
                notice_id=notice.notice_id,
                image_path=image_path,
                uploaded_at=timezone.now(),
            )

        # ---------------------------------------------
        # NOTIFICATION
        # ---------------------------------------------

        Notification.objects.create(
            title="New University Notice",
            message=title,
            notice_id=notice.notice_id,
            created_at=timezone.now(),
        )

        messages.success(
            request,
            "University notice created successfully."
        )

        return redirect("admin_dashboard")


    # =====================================================
    # GET
    # =====================================================

    return render(
        request,
        "notices/admin_create_notice.html",
        {
            "categories": categories,
        }
    )
# =========================================================
# ADMIN COMMUNITY MANAGEMENT
# =========================================================
def admin_community(request):

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    search = request.GET.get(
        "search",
        ""
    ).strip()

    status = request.GET.get(
        "status",
        ""
    ).strip()

    posts = (
        CommunityPost.objects
        .all()
        .order_by("-posted_at")
    )

    # =====================================================
    # SEARCH
    # =====================================================

    if search:

        posts = posts.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(display_name__icontains=search)
        )

    # =====================================================
    # STATUS
    # =====================================================

    if status:

        posts = posts.filter(
            status=status
        )

    posts = list(
        posts[:100]
    )

    # =====================================================
    # PREPARE POSTS
    # =====================================================

    for post in posts:

        post.dashboard_image = None

        if (
            post.attachment
            and post.attachment_type == "image"
        ):
            post.dashboard_image = post.attachment

        post.comment_count = (
            CommunityComment.objects
            .filter(
                post_id=post.post_id
            )
            .count()
        )

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        "posts": posts,

        "search": search,

        "selected_status": status,

        "admin_name": request.session.get(
            "admin_name",
            "Administrator"
        ),
    }

    return render(
        request,
        "notices/admin_community.html",
        context
    )
# =========================================================
# ADMIN HIDE COMMUNITY POST
# =========================================================

def admin_hide_community_post(request, post_id):

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    if request.method != "POST":
        return redirect("admin_community")

    post = get_object_or_404(
        CommunityPost,
        post_id=post_id
    )

    post.status = "hidden"
    post.save(
        update_fields=["status"]
    )

    messages.success(
        request,
        "Community post hidden."
    )

    return redirect("admin_community")
def admin_delete_community_post(request, post_id):
    if not request.session.get("admin_id"):
        return redirect("admin_login")

    if request.method != "POST":
        return redirect("admin_community")

    post = get_object_or_404(
        CommunityPost,
        post_id=post_id
    )

    # Delete comments belonging to this post first
    CommunityComment.objects.filter(
        post_id=post_id
    ).delete()

    # Delete the community post
    post.delete()

    messages.success(
        request,
        "Community post deleted successfully."
    )

    return redirect("admin_community")
# =========================================================
# ADMIN RESTORE COMMUNITY POST
# =========================================================

def admin_restore_community_post(request, post_id):

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    if request.method != "POST":
        return redirect("admin_community")

    post = get_object_or_404(
        CommunityPost,
        post_id=post_id
    )

    post.status = "active"
    post.save(
        update_fields=["status"]
    )

    messages.success(
        request,
        "Community post restored."
    )

    return redirect("admin_community")
# =========================================================
# ADMIN COMMENT MANAGEMENT
# =========================================================
def admin_comments(request):
    if not request.session.get("admin_id"):
        return redirect("admin_login")

    from django.db.models import Q

    search = request.GET.get("search", "").strip()

    comments = CommunityComment.objects.all().order_by("-commented_at")

    if search:
        comments = comments.filter(
            Q(comment_text__icontains=search) |
            Q(display_name__icontains=search)
        )

    comments = list(comments[:200])

    for comment in comments:
        comment.community_post = (
            CommunityPost.objects
            .filter(post_id=comment.post_id)
            .first()
        )

    context = {
        "comments": comments,
        "search": search,
        "admin_name": request.session.get(
            "admin_name",
            "Administrator"
        ),
    }

    return render(
        request,
        "notices/admin_comments.html",
        context
    )
# =========================================================
# ADMIN DELETE COMMENT
# =========================================================

def admin_delete_comment(request, comment_id):
    if not request.session.get("admin_id"):
        return redirect("admin_login")

    if request.method != "POST":
        return redirect("admin_comments")

    comment = get_object_or_404(
        CommunityComment,
        comment_id=comment_id
    )

    comment.delete()

    messages.success(
        request,
        "Comment deleted successfully."
    )

    return redirect("admin_comments")
# =========================================================
# ADMIN CATEGORY MANAGEMENT
# =========================================================
def admin_categories(request):
    if not request.session.get("admin_id"):
        return redirect("admin_login")

    categories = list(
        Category.objects.all().order_by("category_name")
    )

    for category in categories:
        category.notice_count = Notice.objects.filter(
            category_id=category.category_id
        ).count()

        category.community_count = 0

        category.total_count = (
    category.notice_count
)

    context = {
        "categories": categories,
        "admin_name": request.session.get(
            "admin_name",
            "Administrator"
        ),
    }

    return render(
        request,
        "notices/admin_categories.html",
        context
    )
# =========================================================
# ADMIN ADD CATEGORY
# =========================================================

def admin_add_category(request):

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    if request.method != "POST":
        return redirect("admin_categories")

    category_name = request.POST.get(
        "category_name",
        ""
    ).strip()

    if not category_name:

        messages.error(
            request,
            "Category name is required."
        )

        return redirect("admin_categories")

    existing = Category.objects.filter(
        category_name__iexact=category_name
    ).exists()

    if existing:

        messages.error(
            request,
            "That category already exists."
        )

        return redirect("admin_categories")

    Category.objects.create(
        category_name=category_name
    )

    messages.success(
        request,
        "Category added successfully."
    )

    return redirect("admin_categories")
# =========================================================
# ADMIN DELETE CATEGORY
# =========================================================

def admin_delete_category(request, category_id):

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    if request.method != "POST":
        return redirect("admin_categories")

    category = get_object_or_404(
        Category,
        category_id=category_id
    )

    category.delete()

    messages.success(
        request,
        "Category deleted successfully."
    )

    return redirect("admin_categories")

def ai_generate_notice(request):

    if not request.session.get("admin_id"):
        return JsonResponse(
            {
                "success": False,
                "error": "Admin authentication required."
            },
            status=403
        )

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "error": "POST request required."
            },
            status=405
        )

    uploaded_file = request.FILES.get("attachment")

    if not uploaded_file:
        return JsonResponse(
            {
                "success": False,
                "error": "Please upload a PDF or image first."
            },
            status=400
        )

    allowed_types = [
        "application/pdf",
        "image/jpeg",
        "image/png",
        "image/webp",
    ]

    if uploaded_file.content_type not in allowed_types:
        return JsonResponse(
            {
                "success": False,
                "error": "Only PDF, JPG, PNG and WEBP files are supported."
            },
            status=400
        )

    # 50 MB maximum
    if uploaded_file.size > 50 * 1024 * 1024:
        return JsonResponse(
            {
                "success": False,
                "error": "File must be smaller than 50 MB."
            },
            status=400
        )

    categories = Category.objects.all().order_by(
        "category_name"
    )

    try:

        result = generate_notice_from_file(
            uploaded_file,
            categories
        )

        category_name = result.get(
            "category",
            ""
        ).strip()

        category = categories.filter(
            category_name__iexact=category_name
        ).first()

        category_id = (
            category.category_id
            if category
            else ""
        )

        return JsonResponse(
            {
                "success": True,
                "title": result.get(
                    "title",
                    ""
                ),
                "description": result.get(
                    "description",
                    ""
                ),
                "category": category_name,
                "category_id": category_id,
            }
        )

    except Exception as e:

        import traceback

        print("\n========== AI ERROR ==========")
        print(str(e))
        traceback.print_exc()
        print("========== END AI ERROR ==========\n")

        return JsonResponse(
            {
                "success": False,
                "error": str(e)
            },
            status=500
        )
# =========================================================
# UNIVERSITY NOTICE BOARD
# =========================================================
def university_notices(request):

    notices = list(
        Notice.objects
        .filter(status="active")
        .order_by("-posted_at")
    )

    for notice in notices:

        # Category
        category = None

        if notice.category_id:
            category = Category.objects.filter(
                category_id=notice.category_id
            ).first()

        notice.public_category = (
            category.category_name
            if category
            else "General"
        )

        # First image
        image = (
            NoticeImage.objects
            .filter(
                notice_id=notice.notice_id
            )
            .order_by("image_id")
            .first()
        )

        notice.public_image = (
            image.image_path
            if image
            else None
        )

        notice.board_image = (
            image.image_path
            if image
            else None
        )

        # BS date
        notice.bs_date = get_bs_date(
            notice.posted_at
        )

    return render(
        request,
        "notices/university_notices.html",
        {
            "notices": notices
        }
    )
# =========================================================
# NOTIFICATION - MARK AS READ
# =========================================================

def mark_notification_read(request, notification_id):

    if request.method != "POST":
        return redirect("home")

    notification = get_object_or_404(
        Notification,
        notification_id=notification_id
    )

    if not request.session.session_key:
        request.session.create()

    browser_key = request.session.session_key

    NotificationRead.objects.get_or_create(
        notification_id=notification.notification_id,
        browser_key=browser_key
    )

    if notification.notice_id:

        return redirect(
            "notice_detail",
            notice_id=notification.notice_id
        )

    return redirect("home")


# =========================================================
# NOTIFICATION - MARK ALL AS READ
# =========================================================

def mark_all_notifications_read(request):

    if request.method != "POST":
        return redirect("home")

    if not request.session.session_key:
        request.session.create()

    browser_key = request.session.session_key

    notifications_list = Notification.objects.all()

    for notification in notifications_list:

        NotificationRead.objects.get_or_create(
            notification_id=notification.notification_id,
            browser_key=browser_key
        )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "/"
        )
    )
def django_test(request):
    return HttpResponse("Django is working!")