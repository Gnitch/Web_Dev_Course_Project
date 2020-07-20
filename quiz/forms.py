from django import forms

from .models import Quiz, Question, Options

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title','description')

    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)        
        self.fields['title'].required = True  

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('answer','question')

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)        
        self.fields['answer'].required = True  
        self.fields['question'].required = True  

class OptionsForm(forms.ModelForm):
    class Meta:
        model = Options
        fields = ('options',)

    def __init__(self, *args, **kwargs):
        super(OptionsForm, self).__init__(*args, **kwargs)        
        self.fields['options'].required = True          










