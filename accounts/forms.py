from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django import forms

class UserAuthenticationForm(AuthenticationForm):

    class Meta :
        model = User
        fields = ('username','password')       
    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-custom', 'placeholder': 'Enter Username'}) 
        self.fields['username'].help_text = None
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-custom', 'placeholder': 'Enter Password'}) 
        self.fields['password'].help_text = None
        self.fields['password'].label = False