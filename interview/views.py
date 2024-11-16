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
# interviews/views.py

import pyttsx3
import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ProgrammingLanguage, Question, StudentAnswer
from django.http import JsonResponse
import speech_recognition as sr  # For Speech-to-Text
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse

def save_question_audio(question_text, question_id):
    """Save question audio using TTS and return path."""
    engine = pyttsx3.init()
    audio_file_path = f'media/audio/question_{question_id}.mp3'
    engine.save_to_file(question_text, audio_file_path)
    engine.runAndWait()
    return audio_file_path

@login_required
def start_interview(request, language_id):
    # Filter questions by language_id
    questions = Question.objects.filter(language_id=language_id)
    
    # Generate audio for each question
    audio_files = {}
    for question in questions:
        audio_file_path = save_question_audio(question.question_text, question.id)
        audio_files[question.id] = audio_file_path

    return render(request, 'interview/interview.html', {
        'questions': questions,
        'audio_files': audio_files
    })
@login_required
def process_response(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        user_audio = request.FILES.get('user_audio')

        # Save the audio file temporarily
        file_path = os.path.join(settings.MEDIA_ROOT, 'temp', f'{request.user.id}_response.wav')
        with open(file_path, 'wb') as f:
            f.write(user_audio.read())
        
        # Transcribe the audio
        user_response = transcribe_audio(file_path)

        question = Question.objects.get(id=question_id)
        score = 10 if user_response.lower() == question.answer.lower() else 0
        StudentAnswer.objects.create(
            student=request.user,
            question=question,
            student_response=user_response,
            score=score
        )
        return JsonResponse({'status': 'success', 'score': score})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


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
# interviews/views.py

from google.cloud import speech
from django.conf import settings

def transcribe_audio(file_path):
    client = speech.SpeechClient()
    with open(file_path, "rb") as audio_file:
        audio_content = audio_file.read()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript if response.results else ""


# Example in views.py

def save_audio_file(user, audio_data):
    file_path = os.path.join(settings.MEDIA_ROOT, 'interviews', f'{user.id}_response.wav')
    with open(file_path, 'wb') as f:
        f.write(audio_data)
    return file_path

def submit_answers(request):
    # Your function logic here
    return HttpResponse("Answers submitted successfully!")

