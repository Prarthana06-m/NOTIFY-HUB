from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *


# =========================
# 🏠 ROLE SELECT
# =========================
def role_select(request):
    return render(request, 'role_select.html')


# =========================
# 🎓 STUDENT DASHBOARD
# =========================
@login_required
def student_dashboard(request):
    student = Student.objects.get(user=request.user)

    notifications = Notification.objects.filter(student=student).order_by('-created_at')
    assignments = Assignment.objects.all()
    results = Result.objects.filter(student=student).order_by('-created_at')

    return render(request, 'student_dashboard.html', {
        'student': student,
        'notifications': notifications,
        'assignments': assignments,
        'results': results
    })


# =========================
# ✅ MARK AS READ
# =========================
@login_required
def mark_read(request, notif_id):
    notif = Notification.objects.get(id=notif_id, student__user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('student_dashboard')


# =========================
# 👨‍🏫 TEACHER DASHBOARD
# =========================
@login_required
def teacher_dashboard(request):
    teacher = Teacher.objects.get(user=request.user)

    assignments = Assignment.objects.filter(teacher=teacher)
    results = Result.objects.all()

    if request.method == "POST":

        # ✅ OBSERVER TRIGGER (NO LOOP HERE)
        if "class_today" in request.POST:
            ClassStatus.objects.create(status="today")
            messages.success(request, "Notification sent!")

        elif "no_class" in request.POST:
            ClassStatus.objects.create(status="no_class")
            messages.success(request, "Notification sent!")

        # ✅ UPLOAD ASSIGNMENT
        elif "upload_assignment" in request.POST:
            title = request.POST.get("title")
            file = request.FILES.get("file")

            if title and file:
                Assignment.objects.create(
                    title=title,
                    file=file,
                    teacher=teacher
                )
                messages.success(request, "Assignment uploaded!")

        # ✅ ADD QUIZ (RESTORED)
        elif "add_quiz" in request.POST:
            title = request.POST.get("quiz_title")

            if title:
                Quiz.objects.create(
                    title=title,
                    teacher=teacher
                )
                messages.success(request, "Quiz added!")

    return render(request, 'teacher_dashboard.html', {
        'teacher': teacher,
        'assignments': assignments,
        'results': results
    })


# =========================
# ❌ DELETE ASSIGNMENT
# =========================
@login_required
def delete_assignment(request, id):
    assignment = Assignment.objects.get(id=id)
    assignment.delete()
    return redirect('teacher_dashboard')


# =========================
# 🧠 QUIZ
# =========================
@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})


@login_required
def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    student = Student.objects.get(user=request.user)
    score = None

    if request.method == "POST":
        score = 0

        for q in questions:
            selected = request.POST.get(str(q.id))
            if selected == q.correct_answer:
                score += 1

        Result.objects.create(
            student=student,
            quiz=quiz,
            score=score
        )

    return render(request, 'take_quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'score': score
    })


# =========================
# 🔐 STUDENT LOGIN
# =========================
def student_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user, _ = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.save()

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)

            if not Student.objects.filter(user=user).exists():
                Student.objects.create(
                    user=user,
                    name=username,
                    email=f"{username}@mail.com"
                )

            return redirect('student_dashboard')

    return render(request, 'login.html')


# =========================
# 🔐 TEACHER LOGIN
# =========================
def teacher_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user, _ = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.save()

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)

            if not Teacher.objects.filter(user=user).exists():
                Teacher.objects.create(
                    user=user,
                    name=username,
                    email=f"{username}@mail.com"
                )

            return redirect('teacher_dashboard')

    return render(request, 'login.html')


# =========================
# 🚪 LOGOUT
# =========================
def custom_logout(request):
    logout(request)
    return redirect('role_select')