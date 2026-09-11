from django.db import models
import random

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(
        max_length=20,
        choices=[
            ("admin", "Admin"),
            ("student", "Student"),
            ("teacher", "Teacher"),
            ("club", "Club"),
        ],
        default="student",
        null=True,
    )
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "users"

    def __str__(self):
        return self.name


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = False
        db_table = "categories"

    def __str__(self):
        return self.category_name


class Notice(models.Model):
    notice_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    category_id = models.IntegerField(null=True, blank=True)
    attachment = models.CharField(max_length=500, null=True, blank=True)
    attachment_type = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    posted_by = models.IntegerField(null=True, blank=True)
    posted_at = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        default="active",
        null=True,
        blank=True
    )
    priority = models.CharField(
        max_length=20,
        default="normal",
        null=True,
        blank=True
    )
    audience = models.CharField(
        max_length=255,
        default="Everyone",
        null=True,
        blank=True
    )
    post_type = models.CharField(
    max_length=20,
    default="text",
)

     
    class Meta:
        managed = False
        db_table = "notices"

    def __str__(self):
        return self.title
class NoticeImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    notice_id = models.IntegerField()
    image_path = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "notice_images"

    def __str__(self):
        return self.image_path

class CommunityPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    category_id = models.IntegerField(null=True, blank=True)
    attachment = models.CharField(max_length=500, null=True, blank=True)
    attachment_type = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    posted_by = models.IntegerField(null=True, blank=True)
    display_name = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    posted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        default="active",
        null=True,
        blank=True
    )
    paper_style = models.CharField(
    max_length=30,
    default="sticky-yellow",
    null=True,
    blank=True,
)
    owner_token = models.CharField(
    max_length=64,
    null=True,
    blank=True,
)
    post_type = models.CharField(
    max_length=20,
    default="text"
)

    
    class Meta:
        managed = False
        db_table = "community_posts"

    def __str__(self):
        return self.title


class CommunityComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post_id = models.IntegerField()
    user_id = models.IntegerField(null=True, blank=True)
    display_name = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    comment_text = models.TextField()
    commented_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "community_comments"

    def __str__(self):
        return self.comment_text[:50]


class NoticeSubmission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    attachment = models.CharField(max_length=500, null=True, blank=True)
    attachment_type = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    submitted_by = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    submitter_type = models.CharField(
        max_length=20,
        default="student",
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        default="pending",
        null=True,
        blank=True
    )
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.IntegerField(null=True, blank=True)
    paper_style = models.CharField(
    max_length=30,
    default="sticky-yellow",
    null=True,
    blank=True,
)

    class Meta:
        managed = False
        db_table = "notice_submissions"

    def __str__(self):
        return self.title

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=200)

    message = models.TextField(null=True, blank=True)

    notice_id = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "notifications"

    def __str__(self):
        return self.title


class NotificationRead(models.Model):
    read_id = models.AutoField(primary_key=True)

    notification_id = models.IntegerField()

    browser_key = models.CharField(max_length=100)

    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "notification_reads"

    def __str__(self):
        return f"{self.notification_id} - {self.browser_key}"