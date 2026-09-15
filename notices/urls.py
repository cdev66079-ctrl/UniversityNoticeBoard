from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [

    # =====================================================
    # PUBLIC
    # =====================================================

    # -----------------------------------------------------
    # HOME
    # -----------------------------------------------------

    path(
        "",
        views.home,
        name="home"
    ),


    # =====================================================
    # NOTIFICATIONS
    # =====================================================

    path(
        "notifications/<int:notification_id>/read/",
        views.mark_notification_read,
        name="mark_notification_read"
    ),

    path(
        "notifications/read-all/",
        views.mark_all_notifications_read,
        name="mark_all_notifications_read"
    ),


    # =====================================================
    # UNIVERSITY NOTICES
    # =====================================================

    # IMPORTANT:
    # /notices/ now uses the NEW university notice board

    path(
        "notices/",
        views.university_notices,
        name="notices"
    ),

    # Optional separate URL for the same new page
    path(
        "university-notices/",
        views.university_notices,
        name="university_notices"
    ),

    # Individual notice
    path(
        "notice/<int:notice_id>/",
        views.notice_detail,
        name="notice_detail"
    ),


    # =====================================================
    # COMMUNITY
    # =====================================================

    path(
        "community/",
        views.community_board,
        name="community"
    ),

    # Alias used by some templates
    path(
        "community-board/",
        views.community_board,
        name="community_board"
    ),

    # Create community post
    path(
        "community/create/",
        views.create_community_post,
        name="create_community_post"
    ),

    # Community post details
    path(
        "community/<int:post_id>/",
        views.community_detail,
        name="community_detail"
    ),

    # Add comment
    path(
        "community/<int:post_id>/comment/",
        views.add_community_comment,
        name="add_community_comment"
    ),

    # Edit own community post
    path(
        "community/<int:post_id>/edit/",
        views.edit_community_post,
        name="edit_community_post"
    ),

    # Delete own community post
    path(
        "community/<int:post_id>/delete/",
        views.delete_community_post,
        name="delete_community_post"
    ),


    # =====================================================
    # ADMIN AUTHENTICATION
    # =====================================================

    path(
        "admin-login/",
        views.admin_login,
        name="admin_login"
    ),

    path(
        "admin-logout/",
        views.admin_logout,
        name="admin_logout"
    ),


    # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),


    # =====================================================
    # ADMIN — UNIVERSITY NOTICES
    # =====================================================

    path(
        "admin/notices/",
        views.admin_notices,
        name="admin_notices"
    ),

    path(
        "admin/create-notice/",
        views.admin_create_notice,
        name="admin_create_notice"
    ),

    path(
        "admin/notices/<int:notice_id>/edit/",
        views.admin_edit_notice,
        name="admin_edit_notice"
    ),

    path(
        "admin/notice/<int:notice_id>/delete/",
        views.admin_delete_notice,
        name="admin_delete_notice"
    ),


    # =====================================================
    # ADMIN — AI NOTICE GENERATOR
    # =====================================================

    path(
        "admin/ai-generate-notice/",
        views.ai_generate_notice,
        name="ai_generate_notice"
    ),


    # =====================================================
    # ADMIN — COMMUNITY
    # =====================================================

    path(
        "admin/community/",
        views.admin_community,
        name="admin_community"
    ),

    path(
        "admin/community/<int:post_id>/delete/",
        views.admin_delete_community_post,
        name="admin_delete_community_post"
    ),

    path(
        "admin/community/<int:post_id>/hide/",
        views.admin_hide_community_post,
        name="admin_hide_community_post"
    ),

    path(
        "admin/community/<int:post_id>/restore/",
        views.admin_restore_community_post,
        name="admin_restore_community_post"
    ),


    # =====================================================
    # ADMIN — COMMENTS
    # =====================================================

    path(
        "admin/comments/",
        views.admin_comments,
        name="admin_comments"
    ),

    path(
        "admin/comment/<int:comment_id>/delete/",
        views.admin_delete_comment,
        name="admin_delete_comment"
    ),


    # =====================================================
    # ADMIN — CATEGORIES
    # =====================================================

    path(
        "admin/categories/",
        views.admin_categories,
        name="admin_categories"
    ),

    path(
        "admin/categories/add/",
        views.admin_add_category,
        name="admin_add_category"
    ),

    path(
        "admin/categories/<int:category_id>/delete/",
        views.admin_delete_category,
        name="admin_delete_category"
    ),
    path("db-test/", views.db_test, name="db_test"),
]


# =========================================================
# MEDIA FILES
# =========================================================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )