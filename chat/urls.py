from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from chat.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('chat/<slug:chatname>/', ChatView.as_view(), name='chat'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', Logout, name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/messages/<slug:chatname>/', MessagesAPIView.as_view(), name="messages"),
    path('admin/', admin.site.urls),
]
