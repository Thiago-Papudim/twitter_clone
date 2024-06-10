from django import forms
from .models import Tweet, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Formulário extra para Usuários
class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Picture")

    class Meta:
        model = Profile
        fields = ('profile_image', )

class TweetForm(forms.ModelForm):
    body = forms.CharField(required=True, 
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Digite seu Tweet",
                "class": "form-control",
            }
        ), label="",)
    
    class Meta:
        model = Tweet
        exclude = ("user", "likes",)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite seu email'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite seu primeiro nome'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite seu sobrenome'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nome de Usuário'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Obrigatório. 150 caracteres ou menos. Somente letras, dígitos e @/./+/-/_.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Sua senha não pode ser muito semelhante às suas outras informações pessoais.</li><li>Sua senha deve conter pelo menos 8 caracteres.</li><li>Sua senha não pode ser uma senha comumente usada. </li><li>Sua senha não pode ser totalmente numérica.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirme sua senha'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Digite a mesma senha de antes, para verificação.</small></span>'