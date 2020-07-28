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
        fields = ('question','answer','figure','multiple_answer')                    

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)        
        self.fields['answer'].required = True  
        self.fields['question'].required = True  
        self.fields['figure'].required = False

class OptionsForm(forms.ModelForm):
    class Meta:
        model = Options
        fields = ('options',)
        widgets = {
            'options': forms.TextInput(attrs={'name':'options'}),
        }           

    def __init__(self, *args, **kwargs):
        super(OptionsForm, self).__init__(*args, **kwargs)        
        self.fields['options'].required = False    
        self.fields['options'].help_text = 'separate two options by comma'          










