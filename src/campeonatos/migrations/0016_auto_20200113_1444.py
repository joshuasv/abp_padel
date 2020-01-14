# Generated by Django 2.2 on 2020-01-13 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campeonatos', '0015_auto_20200113_1304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enfrentamiento',
            old_name='acepto_pareja_1',
            new_name='acepto_pareja',
        ),
        migrations.RemoveField(
            model_name='enfrentamiento',
            name='acepto_pareja_2',
        ),
        migrations.AddField(
            model_name='enfrentamiento',
            name='turno_fecha',
            field=models.CharField(choices=[('1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pareja_1', to='campeonatos.Pareja')), ('2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pareja_2', to='campeonatos.Pareja'))], default='1', max_length=1),
        ),
    ]