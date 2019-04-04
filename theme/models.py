from django.db import models

# Create your models here.
from student.models import Student
from teacher.models import CountOfHour
from teacher.models import BranchOfKnowledge


class WriteWork(models.Model):
    work_name = models.CharField(max_length=500, unique=True)
    english_work_name = models.CharField(max_length=500, unique=True)
    student = models.ManyToManyField(Student, through='Record')
    year_of_study = models.SmallIntegerField()
    previous_version = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ManyToManyField(BranchOfKnowledge)
    teacher_hour = models.ForeignKey(CountOfHour, on_delete=models.CASCADE)

    def __str__(self):
        return self.work_name


class Record(models.Model):
    STATUS_TITLE = (
        ('WAIT', 'очікується підтвердження'),
        ('CONFIRMED', 'підтверджкно викладачем'),
        ('REJECTED', 'відхилено викладачем'),
        ('BLOCKED', 'затверджено на іншу тему')
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    work = models.ForeignKey(WriteWork, on_delete=models.CASCADE, to_field='work_name')
    status = models.CharField(max_length=10, choices=STATUS_TITLE)
    date_of_record = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student + self.work


