# Generated by Django 2.2 on 2019-11-15 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0003_auto_20191115_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='horario_pista',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horario_pista', to='pistas.HorarioPista'),
        ),
    ]
