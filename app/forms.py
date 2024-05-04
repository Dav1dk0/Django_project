from django import forms
from .models import Topic, Video, Comment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'description']


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file', 'description']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Log in', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Log in', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

