from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ClassStatus, Student, Notification, Assignment, Quiz


# =========================
# 🟢 CLASS STATUS OBSERVER
# =========================
@receiver(post_save, sender=ClassStatus)
def class_status_notification(sender, instance, created, **kwargs):
    if created:
        if instance.status == "class_today":
            message = "📢 Class is scheduled for today"
        elif instance.status == "no_class":
            message = "❌ No class today"

        else:
            return  # ❗ safety: ignore unknown values

        for student in Student.objects.all():
            Notification.objects.create(
                student=student,
                message=message
            )


# =========================
# 📤 ASSIGNMENT OBSERVER
# =========================
@receiver(post_save, sender=Assignment)
def assignment_notification(sender, instance, created, **kwargs):
    if created:
        message = f"📚 New Assignment Uploaded: {instance.title}"

        for student in Student.objects.all():
            Notification.objects.create(
                student=student,
                message=message
            )


# =========================
# 🧠 QUIZ OBSERVER
# =========================
@receiver(post_save, sender=Quiz)
def quiz_notification(sender, instance, created, **kwargs):
    if created:
        message = f"📝 New Quiz Available: {instance.title}"

        for student in Student.objects.all():
            Notification.objects.create(
                student=student,
                message=message
            )