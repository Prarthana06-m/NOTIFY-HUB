from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='core.ClassStatus')
def send_notification(sender, instance, created, **kwargs):
    if created:
        from core.models import Student, Notification  # ✅ safe import

        if instance.status == "today":
            message = "📢 Class is scheduled for today"
        else:
            message = "❌ No class today"

        for student in Student.objects.all():
            Notification.objects.create(
                student=student,
                message=message
            )