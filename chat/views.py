from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from django.views.generic.edit import FormView
from . import forms
from chat.models import Message
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

def Logout(request):
    """logout logged in user"""
    logout(request)
    return HttpResponseRedirect(reverse_lazy('home'))


class LoginView(FormView):
    """login view"""

    form_class = forms.LoginForm
    success_url = reverse_lazy('home')
    template_name = 'registration/login.html'

    def form_valid(self, form):
        """ process user login"""
        credentials = form.cleaned_data
        print(credentials['email'])
        print(credentials['password'])
        user = authenticate(username=credentials['email'],
                            password=credentials['password'])
        print(user)
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request, messages.INFO, 'Wrong credentials\
                                please try again')
            return HttpResponseRedirect(reverse_lazy('login'))

class HomeView(LoginRequiredMixin, TemplateView):

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # List all users for chatting. Except myself.
        print(self.request.user.username)
        context['users'] = User.objects.exclude(id=self.request.user.id)\
                                       .values('username')
        return context


class ChatView(LoginRequiredMixin, TemplateView):

    template_name = 'chat.html'

    def dispatch(self, request, **kwargs):
        # Get the person we are chatting with, if not exist raise 404.
        print(request.user.username)
        # receiver_username = kwargs['chatname'].replace(
        #     request.user.username, '').replace('-', '')
        receiver_username = kwargs['chatname'].split('-')[1]
        print(kwargs['chatname'].split('-')[1])
        
        kwargs['receiver'] = get_object_or_404(User, username=receiver_username)
        print(kwargs['receiver'].username)
        return super().dispatch(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['receiver'] = kwargs['receiver']
        return context


class MessagesAPIView(View):

    def get(self, request, chatname):
        # Grab two users based on the chat name.
        print('before user fetch')
        users = User.objects.filter(username__in=chatname.split('-'))
        # Filters messages between this two users.
        result = Message.objects.filter(
            Q(sender=users[0], receiver=users[1]) | Q(sender=users[1], receiver=users[0])
        ).annotate(
            username=F('sender__username'), message=F('text'),
        ).order_by('date_created').values('username', 'message', 'date_created')

        return JsonResponse(list(result), safe=False)
