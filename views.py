from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, StudentProfileForm
from .models import StudentProfile, Job, JobApplication
# Create your views here.

def register_view(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            messages.success(request,'Registration successful.You are new logged in')
            return redirect('dashboard')
        else:
            messages.error(request,'Registration failed')
            
    else:
        form=RegistrationForm()
    return render(request,'base/register.html',{'form':form})
def login_value(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password=request.POST.get('password')
        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid usernmae and password')
    return render(request,'base/login.html') 
def logout_view(request):
    logout(request)
    messages.success(request,'you have been logged out')
    return redirect('login') 
@login_required
def dashboard_view(request):

    total_jobs = Job.objects.filter(is_active=True).count()

    student, created = StudentProfile.objects.get_or_create(user=request.user)

    applied_jobs = JobApplication.objects.filter(student=student).count()

    resume_uploaded = student.resume

    context = {
        'total_jobs': total_jobs,
        'applied_jobs': applied_jobs,
        'resume_uploaded': resume_uploaded,
    }

    return render(request, 'base/dashboard.html', context)
@login_required
def profile_view(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')

    else:
        form = StudentProfileForm(instance=profile)

    return render(request, 'base/profile.html', {'form': form})
@login_required
def job_list_view(request):

    search = request.GET.get('search')

    jobs = Job.objects.filter(is_active=True)

    if search:
        jobs = jobs.filter(job_title__icontains=search)

    context = {
        'jobs': jobs,
        'search': search,
    }

    return render(request, 'base/job_list.html', context)
@login_required
def job_detail_view(request, pk):
    job = Job.objects.get(id=pk)
    return render(request, 'base/job_detail.html', {'job': job})
@login_required
def apply_job_view(request, pk):
    job = Job.objects.get(id=pk)
    student = StudentProfile.objects.get(user=request.user)

    if JobApplication.objects.filter(student=student, job=job).exists():
        messages.warning(request, "You have already applied for this job.")
    else:
        JobApplication.objects.create(
            student=student,
            job=job
        )
        messages.success(request, "Job applied successfully!")

    return redirect('job_detail', pk=pk)
@login_required
def applied_jobs_view(request):
    student = StudentProfile.objects.get(user=request.user)
    applications = JobApplication.objects.filter(student=student)

    return render(
        request,
        'base/applied_jobs.html',
        {'applications': applications}
    )
    