from django import forms

from .models import Quiz, Question, Options, Comments, Poll, PollChoices

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title','description','timer',)

    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)        
        self.fields['title'].required = True  
        self.fields['description'].required = False 
        self.fields['timer'].required = False
        self.fields['timer'].help_text = "Keep input blank if no timer is required and time should be between '10 < time < 120' seconds"

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question','answer','explanation','figure','multiple_answer',)                    

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)        
        self.fields['answer'].required = True  
        self.fields['question'].required = True  
        self.fields['figure'].required = False
        self.fields['explanation'].required = False

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

class CommentsForm(forms.ModelForm) :

    class Meta :
        model = Comments
        fields = ('comment',)
        widgets = {
            'comment':forms.TextInput(attrs={'class': 'form-comments','placeholder':'Enter Comment'})
        }
        labels ={
            'comment' : (''),            
        }          

    def __init__(self, *args, **kwargs):
        super(CommentsForm, self).__init__(*args, **kwargs)
        self.fields['comment'].required=True 

class PollForm(forms.ModelForm):


    class Meta :
        model = Poll
        fields = ('title',)

    def __init__(self, *args, **kwargs):
        super(PollForm, self).__init__(*args, **kwargs)
        self.fields['title'].required=True 

class PollChoicesForm(forms.ModelForm):

    class Meta :
        model = PollChoices
        fields = ('choice',)
        widgets = {
            'choice': forms.TextInput(attrs={'placeholder':'Add a choice'}),
        }   

    def __init__(self, *args, **kwargs):
        super(PollChoicesForm, self).__init__(*args, **kwargs)
        self.fields['choice'].required=True 
        self.fields['choice'].label = False        





