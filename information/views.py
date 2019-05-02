from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView

from student.models import Student
# Create your views here.
from teacher.models import Teacher, Protection, TopicOffer, Department, Specialty, StudentGroup
from theme.models import Record


def index(request):
    if 'mail' not in request.session:
        return HttpResponseRedirect('../authorization/')
    return HttpResponse('<h1>Information page</h1>')


class InfoListView(ListView):
    template_name = 'info/info.html'
    model = Teacher

    def get(self, *args, **kwargs):
        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        return super(InfoListView, self).get(*args, **kwargs)

    def get_queryset(self, **kwargs):
        if self.request.GET.get('year') is not None and self.request.GET.get(
                'specialty') is not None and self.request.GET.get(
            'protection') is not None and self.request.GET.get(
            'preprotection') is not None and self.request.GET.get('specialty') != 'anything':
            specialty = Specialty.objects.get(pk=self.request.GET.get('specialty'))
            year = self.request.GET.get('year')
            group = StudentGroup.objects.filter(year_of_entry=year, specialty=specialty)[0]
            cathedra = Department.objects.get(methodist__methodist_id=self.request.session['user_id'])
            protection = self.request.GET.get('protection')
            pre_protection = self.request.GET.get('preprotection')
            idk = Protection.objects.filter(speciality_group=group, teacher_department=cathedra)[0].pk
            if idk:
                pr = Protection.objects.get(id=idk)
                pr.date_of_confirmation = protection
                pr.date_of_pre_protection = pre_protection
                pr.save()
            else:
                pr = Protection.objects.get_or_create(speciality_group=group, teacher_department=cathedra,
                                                      date_of_pre_protection=pre_protection,
                                                      date_of_confirmation=protection)
            return HttpResponseRedirect('../methodist')

    def get_context_data(self, **kwargs):
        context = super(InfoListView, self).get_context_data(**kwargs)
        if self.request.session['role'] == 'student':
            student = Student.objects.get(pk=self.request.session['user_id'])
            record = Record.objects.filter(status='CONFIRMED', student=student)[0]
            if not record:
                context['message'] = "Ви ще не затверджені за темою!"
                return context
            teacher = Teacher.objects.filter(pk=record.work.teacher_offer.teacher.teacher_id)[0]
            protection = Protection.objects.filter(teacher_department=teacher.department,
                                                   speciality_group=student.specialty)
            if not protection:
                context['message'] = "Дата ще не визначена методистом кафедри!"
                return context
            context['protection'] = protection[0]
        elif self.request.session['role'] == 'teacher':
            specialties = TopicOffer.objects.filter(teacher__teacher_id=self.request.session['user_id'],
                                                    year_of_work=2019)
            protections = Protection.objects.filter(
                teacher_department=Teacher.objects.get(pk=self.request.session['user_id']).department)
            protect_spec = []
            exists = False
            for sp in specialties:
                exists = False
                for pr in protections:
                    if sp.specialty == pr.speciality_group:
                        exists = True
                        protect_spec.append((sp.specialty.specialty.specialty_name, pr.date_of_pre_protection,
                                             pr.date_of_confirmation))
                if not exists:
                    protect_spec.append((sp.specialty.specialty.specialty_name, "---", "---"))
            context['protect_spec'] = protect_spec
        elif self.request.session['role'] == 'methodist':
            cathedra = Department.objects.get(methodist__methodist_id=self.request.session['user_id'])
            teachers = Teacher.objects.filter(department=cathedra)
            offers = TopicOffer.objects.filter(teacher__in=teachers)
            specialties = []
            for of in offers:
                specialties.append(of.specialty.specialty)
            context['cathedra'] = cathedra.department_name
            context['specialties'] = specialties
        return context
