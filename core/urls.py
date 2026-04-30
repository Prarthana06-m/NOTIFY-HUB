from django.urls import path
from . import views

urlpatterns = [
    path('', views.role_select, name='role_select'),

    path('student-login/', views.student_login, name='student_login'),
    path('teacher-login/', views.teacher_login, name='teacher_login'),

    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    # ✅ THIS LINE FIXES YOUR ERROR
    path('mark-read/<int:notif_id>/', views.mark_read, name='mark_read'),

    path('delete-assignment/<int:id>/', views.delete_assignment, name='delete_assignment'),

    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),

    path('logout/', views.custom_logout, name='logout'),
]