from django.contrib import admin
from .models import Student, Teacher, Notification, Assignment, Quiz, Question, Result

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Notification)
admin.site.register(Assignment)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Result)