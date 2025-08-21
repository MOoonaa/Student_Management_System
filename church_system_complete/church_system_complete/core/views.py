from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import StudentRegisterForm
from .models import Student
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # ✅ Only create student profile if user is NOT admin
            if not user.is_superuser and not user.is_staff:
                Student.objects.create(
                    user=user,
                    name=user.username,
                    email=user.email
                )

            login(request, user)
            return redirect('dashboard')
    else:
        form = StudentRegisterForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    # ✅ If user is admin, skip Student dashboard
    if request.user.is_superuser or request.user.is_staff:
        return render(request, 'core/admin_only.html')

    try:
        student_profile = Student.objects.get(user=request.user)
        return render(request, 'core/dashboard.html', {'profile': student_profile})
    except Student.DoesNotExist:
        return render(request, 'core/admin_only.html')

    
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    
    students = Student.objects.all()

    if request.method == 'POST':
        # إضافة طالب جديد
        if 'add_student' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            grade = request.POST.get('grade', '')
            absences = request.POST.get('absence', 0)
            Student.objects.create(
                name=name,
                email=email,
                grade=grade,
                absences=absences
            )
            return redirect('admin_dashboard')

        # حذف طالب
        elif 'delete_student' in request.POST:
            student_id = request.POST.get('student_id')
            Student.objects.filter(id=student_id).delete()
            return redirect('admin_dashboard')

        # تعديل طالب
        elif 'update_student' in request.POST:
            student_id = request.POST.get('student_id')
            grade = request.POST.get('grade')
            absences = request.POST.get('absence')
            try:
                student = Student.objects.get(id=student_id)
                if grade is not None:
                    student.grade = grade
                if absences is not None:
                    student.absences = absences
                student.save()
            except Student.DoesNotExist:
                pass
            return redirect('admin_dashboard')

    return render(request, 'admin_dashboard.html', {'students': students})
