# Generated by Django 4.2.11 on 2024-09-17 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jogo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tema',
            name='estar_logado',
            field=models.BooleanField(default=False),
        ),
    ]