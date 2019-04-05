from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
from django.views.generic import DetailView

from teacher.models import Teacher


def index(request):
    if 'mail' not in request.session:
        return HttpResponseRedirect('../authorization/')
    return render(request, 'teacher/teacher.html')


class TeacherDetailView(DetailView):
    template_name = 'teacher/teacher.html'
    model = Teacher

    def get(self, *args, **kwargs):
        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        if 'role' != 'teacher':
            return HttpResponseRedirect('../authorization/')
        return super(TeacherDetailView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
