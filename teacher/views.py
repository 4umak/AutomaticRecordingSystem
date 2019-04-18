from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
from django.views.generic import ListView

from teacher.models import Teacher
from theme.models import WriteWork


def index(request):
    if 'mail' not in request.session:
        return HttpResponseRedirect('../authorization/')
    return render(request, 'teacher/teacher.html')


class TeacherListView(ListView):
    template_name = 'teacher/teacher.html'
    model = Teacher

    def get(self, *args, **kwargs):

        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        if not self.request.session['role'] == 'teacher':
            return HttpResponseRedirect('../teacher/')
        return super(TeacherListView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher'] = Teacher.objects.get(pk=self.request.session['user_id'])
        context['work_count'] = Teacher.objects.get(pk=self.request.session['user_id'])
        context['themes_list'] = WriteWork.objects.all().filter(teacher_offer__teacher__teacher_id=self.request.session['user_id'])
        return context
