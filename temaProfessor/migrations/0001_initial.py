# Generated by Django 4.2.11 on 2024-09-18 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('estar_logado', models.BooleanField(default=False)),
                ('criado_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Palavra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('palavra', models.CharField(max_length=100)),
                ('dica', models.CharField(blank=True, max_length=255, null=True)),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='temaProfessor.tema')),
            ],
        ),
        migrations.AddConstraint(
            model_name='palavra',
            constraint=models.UniqueConstraint(fields=('tema', 'palavra'), name='unique_palavra_tema'),
        ),
    ]
