from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_topic/', login_required(views.AddTopic.as_view()), name='add_topic'),
    path('topic/<int:pk>/', views.TopicDetail.as_view(), name='topic_detail'),
    path('topic/<int:topic_id>/add_video/', login_required(views.AddVideo.as_view()), name='add_video_to_topic'),
    path('video/<int:pk>/', login_required(views.VideoDetail.as_view()), name='video_detail'),
    path('register_user/', views.RegisterUser.as_view(), name='register_user'),
    path('login_user/', views.LoginUser.as_view(), name='login_user'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:pk>', views.ProfileDetail.as_view(), name='profile_detail')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
