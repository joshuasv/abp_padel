# Generated by Django 2.2 on 2019-11-17 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campeonatos', '0012_enfrentamiento_ronda'),
    ]

    operations = [
        migrations.AddField(
            model_name='enfrentamiento',
            name='campeonato',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='campeonatos.Campeonato'),
            preserve_default=False,
        ),
    ]
