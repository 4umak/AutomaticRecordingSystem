# Generated by Django 2.1.5 on 2019-03-14 13:08

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='name',
            new_name='department_name',
        ),
        migrations.RenameField(
            model_name='faculty',
            old_name='name',
            new_name='faculty_name',
        ),
        migrations.RenameField(
            model_name='teacher',
            old_name='name',
            new_name='teacher_name',
        ),
    ]
