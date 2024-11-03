# interviews/forms.py

from django import forms
from .models import ProgrammingLanguage, Question

class LanguageForm(forms.ModelForm):
    class Meta:
        model = ProgrammingLanguage
        fields = ['name']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'language', 'answer']  # Include the answer field

# interviews/forms.py


class SelectLanguageForm(forms.Form):
    language = forms.ModelChoiceField(queryset=ProgrammingLanguage.objects.all(), label="Select a Programming Language")
