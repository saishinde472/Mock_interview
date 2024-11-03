# interviews/views.py

from django.shortcuts import render, redirect
from .models import ProgrammingLanguage, Question
from .forms import LanguageForm, QuestionForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import StudentAnswer
from .forms import SelectLanguageForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import pyttsx3  # Text-to-speech library
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.contrib import messages  # Import messages framework

@staff_member_required
def add_language(request):
    if request.method == 'POST':
        form = LanguageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Programming language added successfully!')  # Success message
            return redirect('add_language')  # Redirect to the same page to add another language
    else:
        form = LanguageForm()
    
    return render(request, 'interview/add_language.html', {'form': form})

def add_question(request):
    languages = ProgrammingLanguage.objects.all()  # Get all programming languages
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)  # Create a Question object but don’t save it yet
            question.language = form.cleaned_data['language']  # Assign the selected language
            question.save()  # Now save the question
            messages.success(request, 'Question added successfully!')
            return redirect('add_question')
    else:
        form = QuestionForm()

    return render(request, 'interview/add_question.html', {'form': form, 'languages': languages})
# interviews/views.py

import pyttsx3
import os

def save_question_audio(question_text, question_id):
    engine = pyttsx3.init()
    audio_file_path = f'media/audio/question_{question_id}.mp3'
    engine.save_to_file(question_text, audio_file_path)
    engine.runAndWait()
    return audio_file_path

@login_required
def start_interview(request):
 
    if request.method == 'POST':
        form = SelectLanguageForm(request.POST)
        if form.is_valid():
            language = form.cleaned_data['language']
            questions = Question.objects.filter(language=language)

            # Save audio files for questions
            audio_files = {}
            for question in questions:
                audio_file_path = save_question_audio(question.question_text, question.id)
                audio_files[question.id] = audio_file_path  # Store path for use in template

            return render(request, 'interview/interview.html', {'questions': questions, 'audio_files': audio_files})
    else:
        form = SelectLanguageForm()
    return render(request, 'interview/select_language.html', {'form': form})



@login_required
def submit_answers(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                question = Question.objects.get(id=question_id)
                answer = StudentAnswer(
                    student=request.user,
                    question=question,
                    student_response=value,
                    score=10 if value.strip().lower() == question.answer.strip().lower() else 0  # Compare with the stored answer
                )
                answer.save()
        return redirect('interview_report')
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def interview_report(request):
    answers = StudentAnswer.objects.filter(student=request.user)
    total_score = sum(answer.score for answer in answers)
    feedback = "Great work!" if total_score > 80 else "Needs improvement"
    context = {
        'answers': answers,
        'total_score': total_score,
        'feedback': feedback,
    }
    return render(request, 'interview/report.html', context)

@login_required
def interview_report_pdf(request):
    answers = StudentAnswer.objects.filter(student=request.user)
    total_score = sum(answer.score for answer in answers)
    feedback = "Great work!" if total_score > 80 else "Needs improvement"
    context = {
        'answers': answers,
        'total_score': total_score,
        'feedback': feedback,
    }
    html = render_to_string('interview/report_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="interview_report.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response
@login_required
def select_language(request):
    languages = ProgrammingLanguage.objects.all()
    if request.method == 'POST':
        language_id = request.POST.get('language_id')
        print(f"Received language_id: {language_id}")  # Print the received language_id
        if language_id:
            return redirect('start_interview', language_id=language_id)
        else:
            messages.error(request, 'Please select a language.')
    return render(request, 'interview/select_language.html', {'languages': languages})
