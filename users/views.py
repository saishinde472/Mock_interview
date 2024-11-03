from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from .models import Resume, Education, Experience
from .forms import ResumeForm, EducationForm, ExperienceForm
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import render_to_string 

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

@login_required
def update_password_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password has been updated!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(user)
    return render(request, 'users/update_password.html', {'form': form})


@login_required
def resume_builder(request):
    resume, created = Resume.objects.get_or_create(user=request.user)
    EducationFormSet = modelformset_factory(Education, form=EducationForm, extra=1, can_delete=True)
    ExperienceFormSet = modelformset_factory(Experience, form=ExperienceForm, extra=1, can_delete=True)

    if request.method == 'POST':
        resume_form = ResumeForm(request.POST, instance=resume)
        education_formset = EducationFormSet(request.POST, queryset=resume.educations.all())
        experience_formset = ExperienceFormSet(request.POST, queryset=resume.experiences.all())

        if resume_form.is_valid() and education_formset.is_valid() and experience_formset.is_valid():
            resume_form.save()
            education_formset.save()
            experience_formset.save()
            return redirect('resume_success')
    else:
        resume_form = ResumeForm(instance=resume)
        education_formset = EducationFormSet(queryset=resume.educations.all())
        experience_formset = ExperienceFormSet(queryset=resume.experiences.all())

    return render(request, 'users/resume_builder.html', {
        'resume_form': resume_form,
        'education_formset': education_formset,
        'experience_formset': experience_formset
    })

@login_required
def generate_pdf(request):
    try:
        resume = Resume.objects.get(user=request.user)
    except Resume.DoesNotExist:
        return redirect('resume_builder')

    # Render the PDF
    html = render_to_string('users/resume_pdf.html', {'resume': resume})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="resume.pdf"'
    
    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response