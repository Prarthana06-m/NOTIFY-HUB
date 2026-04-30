from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # ROLE SELECT
    path('', views.role_select, name='role_select'),

    # LOGIN
    path('student-login/', views.student_login, name='student_login'),
    path('teacher-login/', views.teacher_login, name='teacher_login'),

    # DASHBOARD REDIRECT
    path('dashboard/', views.redirect_user, name='dashboard'),

    # DASHBOARDS
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    # LOGOUT
    path('logout/', views.custom_logout, name='logout'),

    # QUIZ
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),

    path('', include('core.urls')),
]