from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import FormMixin

from .models import Topic, Video
from .forms import TopicForm, VideoForm, CommentForm, RegisterUserForm
from django.views.generic import View, FormView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from .forms import LoginUserForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def home(request):
    topics = Topic.objects.all()
    return render(request, 'libary/index.html', {'topics': topics})


"""def add_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect('home')
    else:
        form = TopicForm()
    return render(request, 'libary/add_topic.html', {'form': form})"""


class AddTopic(FormView):
    form_class = TopicForm
    template_name = 'libary/add_topic.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        topic = form.save(commit=False)
        topic.user = self.request.user
        topic.save()
        return super().form_valid(form)


class TopicDetail(DetailView):
    model = Topic
    template_name = 'libary/topic_detail.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = self.object.videos.all()
        return context


"""def add_video_to_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.author = request.user
            video.topic = topic
            video.save()
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = VideoForm()
    return render(request, 'libary/add_video.html', {'form': form, 'topic': topic})"""


class AddVideo(FormView):
    form_class = VideoForm
    template_name = 'libary/add_video.html'

    def form_valid(self, form):
        topic_id = self.kwargs.get('topic_id')
        topic = get_object_or_404(Topic, id=topic_id)

        video = form.save(commit=False)
        video.user = self.request.user
        video.topic = topic
        video.save()

        return redirect('topic_detail', pk=topic_id)


"""def video_detail(request, video_id):
    video = Video.objects.get(id=video_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.video = video
            comment.author = request.user
            comment.save()
            return redirect('video_detail', video_id=video.id)
    else:
        form = CommentForm()
    return render(request, 'libary/video_detail.html', {'video': video, 'form': form})"""


class VideoDetail(DetailView, FormView):
    model = Video
    template_name = 'libary/video_detail.html'
    context_object_name = 'video'
    form_class = CommentForm
    success_url = reverse_lazy('video_detail')

    def form_valid(self, form):
        self.object = self.get_object()
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.video = self.object
        comment.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def get_success_url(self):
        return reverse_lazy('video_detail', kwargs={'pk': self.object.pk})

"""def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    else:
        form = RegisterUserForm
    return render(request, 'libary/register.html', {'form': form})"""


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'libary/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


"""def login_user(request):
    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "login or password is invalid")
    else:
        form = LoginUserForm()
    return render(request, 'libary/login.html', {'form': form})
"""


class LoginUser(FormView):
    template_name = 'libary/login.html'
    form_class = LoginUserForm

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('home')
        else:
            form.add_error(None, "Login or password is invalid")
            return self.form_invalid(form)


def logout_view(request):
    logout(request)
    return redirect('home')


class ProfileDetail(DetailView):
    model = User
    context_object_name = 'video'
    template_name = 'libary/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.all()
        return context





