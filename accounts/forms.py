from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django import forms

class UserAuthenticationForm(AuthenticationForm):

    class Meta :
        model = User
        fields = ('username','password')     
        widgets = {
            'options': forms.TextInput(attrs={'name':'options'}),
        }    
    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-custom', 'placeholder': 'Enter Username'}) 
        self.fields['username'].help_text = None
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-custom', 'placeholder': 'Enter Password'}) 
        self.fields['password'].help_text = None
        self.fields['password'].label = False

class UserSignUpForm(UserCreationForm):
 
    class Meta :
        model = User
        fields = ('username', 'email', 'password1', )       
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-custom','placeholder':'Enter Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-custom','placeholder':'Enter Email'}),
        }
        labels = {
            'username' : (''),
            'email' : (''),
        }    
        help_texts = {
            'username': None,
            'email': None,
        } 
    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-custom', 'placeholder': 'Enter Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-custom', 'placeholder': 'Re-Enter Password'})   
        self.fields['password2'].help_text = None
        self.fields['email'].max_length = None
        self.fields['email'].required=False
        self.fields['password1'].label = False
        self.fields['password2'].label = False
        self.fields['username'].required = False
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None



