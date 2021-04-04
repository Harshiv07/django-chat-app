from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views import View
from django.views.generic.base import TemplateView

from chat.models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class HomeView(LoginRequiredMixin, TemplateView):

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # List all users for chatting. Except myself.
        type = get_object_or_404(Institute, institute_id=self.request.user.institute_id).type
        u_type = self.request.user.u_type
        context['students'] = []
        context['teachers'] = []
        
        if type == 'School' or type == 'University':
            if u_type == 'Student':
                obj = ClassesDetails.objects.get(student=self.request.user.email, institute= self.request.user.institute_id)
                print(obj.class_id)
                print(obj.section)
                try:
                    students_list = list(ClassesDetails.objects.filter(~Q(student=self.request.user.email)).filter(class_id = obj.class_id, section= obj.section))
                    for s in students_list:
                        print("student: " + s.student)
                        context['students'].append({'username': get_object_or_404(User, email=s.student).username, 'email': s.student})

                    teachers_list = list(SubjectClassTeacherDetails.objects.filter(classid = obj.class_id, section= obj.section))
                    for t in teachers_list:
                        print("teacher: " + t.teacher)
                        context['teachers'].append({'username': get_object_or_404(User, email=t.teacher).username, 'email': t.teacher})
                    
                except:
                    pass
            elif u_type == 'Teacher':
                class_list = list(SubjectClassTeacherDetails.objects.filter(teacher=self.request.user.email))
                for c in class_list:
                    print(c.classid)
                    print(c.section)
                    try:
                        students_list = list(ClassesDetails.objects.filter(class_id = c.classid, section= c.section))
                        for s in students_list:
                            print("student: " + s.student)
                            context['students'].append({'username': get_object_or_404(User, email=s.student).username, 'email': s.student})

                        teachers_list = list(SubjectClassTeacherDetails.objects.filter(~Q(student=self.request.user.email)).filter(classid = c.classid, section= c.section))
                        for t in teachers_list:
                            print("teacher: " + t.teacher)
                            context['teachers'].append({'username': get_object_or_404(User, email=t.teacher).username, 'email': t.teacher})
                    
                    except:
                        pass
        else:
            if u_type == 'Student':
                obj = BatchDetails.objects.get(student=self.request.user.email, institute= self.request.user.institute_id)
                print(obj.batch_id)
                try:
                    students_list = list(BatchDetails.objects.filter(~Q(student=self.request.user.email)).filter(batch_id = obj.batch_id))
                    for s in students_list:
                        print("student: " + s.student)
                        context['students'].append({'username': get_object_or_404(User, email=s.student).username, 'email': s.student})

                    teachers_list = list(SubjectBatchTeacherDetails.objects.filter(batchid = obj.batch_id))
                    for t in teachers_list:
                        print("teacher: " + t.teacher)
                        context['teachers'].append({'username': get_object_or_404(User, email=t.teacher).username, 'email': t.teacher})
                    
                except:
                    pass
            elif u_type == 'Teacher':
                batch_list = list(SubjectBatchTeacherDetails.objects.filter(teacher=self.request.user.email))
                for b in batch_list:
                    print(b.batchid)
                    try:
                        students_list = list(BatchDetails.objects.filter(~Q(student=self.request.user.email)).filter(batch_id = b.batchid))
                        for s in students_list:
                            print("student: " + s.student)
                            context['students'].append({'username': get_object_or_404(User, email=s.student).username, 'email': s.student})

                        teachers_list = list(SubjectBatchTeacherDetails.objects.filter(batchid = b.batchid))
                        for t in teachers_list:
                            print("teacher: " + t.teacher)
                            context['teachers'].append({'username': get_object_or_404(User, email=t.teacher).username, 'email': t.teacher})
                    except:
                        pass
        
        return context

class ChatView(LoginRequiredMixin, TemplateView):

    template_name = 'chat.html'

    def dispatch(self, request, **kwargs):
        # Get the person we are chatting with, if not exist raise 404.
        print(request.user.email)
        # receiver_username = kwargs['chatname'].replace(
        #     request.user.username, '').replace('-', '')
        username = self.request.user.username
        if username == kwargs['chatname'].split('-')[1]:
            receiver_username = kwargs['chatname'].split('-')[0]
        else:
            receiver_username = kwargs['chatname'].split('-')[1]
            
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
