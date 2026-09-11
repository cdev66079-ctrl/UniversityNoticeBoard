from .models import Notification, NotificationRead


def notifications(request):

    notification_list = list(
        Notification.objects
        .all()
        .order_by("-created_at")[:10]
    )

    # Make sure the browser has a session
    if not request.session.session_key:
        request.session.create()

    browser_key = request.session.session_key

    notification_ids = [
        notification.notification_id
        for notification in notification_list
    ]

    read_ids = set(
        NotificationRead.objects
        .filter(
            browser_key=browser_key,
            notification_id__in=notification_ids
        )
        .values_list(
            "notification_id",
            flat=True
        )
    )

    for notification in notification_list:

        notification.is_read = (
            notification.notification_id in read_ids
        )

    unread_count = sum(
        1
        for notification in notification_list
        if not notification.is_read
    )

    return {
        "notifications": notification_list,
        "unread_notifications_count": unread_count,
    }