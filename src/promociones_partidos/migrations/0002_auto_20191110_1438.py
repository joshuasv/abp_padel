# Generated by Django 2.2 on 2019-11-10 13:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promociones_partidos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promocionpartido',
            name='participante_1',
        ),
        migrations.AddField(
            model_name='promocionpartido',
            name='participante_1',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='participante_1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='promocionpartido',
            name='participante_2',
        ),
        migrations.AddField(
            model_name='promocionpartido',
            name='participante_2',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='participante_2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='promocionpartido',
            name='participante_3',
        ),
        migrations.AddField(
            model_name='promocionpartido',
            name='participante_3',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='participante_3', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='promocionpartido',
            name='participante_4',
        ),
        migrations.AddField(
            model_name='promocionpartido',
            name='participante_4',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='participante_4', to=settings.AUTH_USER_MODEL),
        ),
    ]
