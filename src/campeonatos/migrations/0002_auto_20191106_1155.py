# Generated by Django 2.2 on 2019-11-06 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campeonatos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pareja',
            name='capitan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='capitan', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pareja',
            name='grupo',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='campeonatos.Grupo'),
        ),
        migrations.AddField(
            model_name='pareja',
            name='miembro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='miembro', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='normativa',
            name='campeonato',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campeonatos.Campeonato'),
        ),
        migrations.AddField(
            model_name='grupo',
            name='normativa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campeonatos.Normativa'),
        ),
    ]
