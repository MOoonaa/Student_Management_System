from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .forms import StudentRegisterForm
from .models import Student


# ==============================
# User Registration
# ==============================
def register(request):
    """
    Handles user registration.
    - If POST: validate form, create User, and (if not admin/staff) create linked Student.
    - If GET: display registration form.
    """
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Only create Student profile if user is NOT admin/staff
            if not user.is_superuser and not user.is_staff:
                Student.objects.create(
                    user=user,
                    name=user.username,
                    email=user.email
                )

            # Auto login after registration
            login(request, user)
            return redirect('dashboard')
    else:
        form = StudentRegisterForm()

    return render(request, 'core/register.html', {'form': form})


# ==============================
# User Login
# ==============================
def login_view(request):
    """
    Handles user login using Django's AuthenticationForm.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Start session
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})


# ==============================
# User Logout
# ==============================
def logout_view(request):
    """
    Logs out the current user and redirects to login page.
    """
    logout(request)
    return redirect('login')


# ==============================
# Dashboard (Student / Admin Split)
# ==============================
@login_required
def dashboard(request):
    """
    Displays the correct dashboard based on the user type:
    - If user is admin/staff → admin_only page
    - If user is student → student dashboard
    """
    # ✅ Redirect admin/staff to admin-only page
    if request.user.is_superuser or request.user.is_staff:
        return render(request, 'core/admin_only.html')

    try:
        # Try to fetch Student profile linked to this user
        student_profile = Student.objects.get(user=request.user)
        return render(request, 'core/dashboard.html', {'profile': student_profile})
    except Student.DoesNotExist:
        # If no Student profile exists, fallback to admin-only page
        return render(request, 'core/admin_only.html')


# ==============================
# Admin Dashboard (CRUD for Students)
# ==============================
@login_required
def admin_dashboard(request):
    """
    Admin-only dashboard for managing students.
    Supports:
    - Adding new students
    - Updating student grade/absences
    - Deleting students
    """
    if not request.user.is_superuser:
        return redirect('dashboard')

    students = Student.objects.all()

    if request.method == 'POST':
        # إضافة طالب جديد (Add Student)
        if 'add_student' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            grade = request.POST.get('grade', '')
            absences = int (request.POST.get('absences', 0))

            Student.objects.create(
                name=name,
                email=email,
                grade=grade,
                absences=absences
            )
            return redirect('admin_dashboard')

        # حذف طالب (Delete Student)
        elif 'delete_student' in request.POST:
            student_id = request.POST.get('student_id')
            Student.objects.filter(id=student_id).delete()
            return redirect('admin_dashboard')

        # تعديل طالب (Update Student)
        elif 'update_student' in request.POST:
            student_id = request.POST.get('student_id')
            grade = request.POST.get('grade')
            absences = request.POST.get('absences')

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

    return render(request, 'core/admin_dashboard.html', {'students': students})
