# Generated by Django 2.2 on 2019-11-12 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campeonatos', '0005_auto_20191108_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='nombre',
            field=models.CharField(default='z', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='normativa',
            name='categoria',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('X', 'Mixto')], max_length=1),
        ),
    ]