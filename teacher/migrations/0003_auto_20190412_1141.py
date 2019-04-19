# Generated by Django 2.1.5 on 2019-04-12 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_teacher_google_scholar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Faculty'),
        ),
        migrations.AlterField(
            model_name='protection',
            name='teacher_department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Department'),
        ),
        migrations.AlterField(
            model_name='specialty',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Department'),
        ),
        migrations.AlterField(
            model_name='studentgroup',
            name='specialty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Specialty'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Department'),
        ),
    ]