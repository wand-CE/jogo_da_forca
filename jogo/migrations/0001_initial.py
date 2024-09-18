# Generated by Django 4.2.11 on 2024-09-17 19:26

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
            name='Letra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letra', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('criado_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Palavra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('palavra', models.CharField(max_length=100)),
                ('dica', models.CharField(blank=True, max_length=255, null=True)),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jogo.tema')),
            ],
        ),
        migrations.CreateModel(
            name='Jogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_anonimo', models.CharField(blank=True, max_length=100, null=True)),
                ('data_jogo', models.DateTimeField(auto_now_add=True)),
                ('acertos', models.ManyToManyField(blank=True, related_name='acertos', to='jogo.letra')),
                ('erros', models.ManyToManyField(blank=True, related_name='erros', to='jogo.letra')),
                ('jogador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('palavra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jogo.palavra')),
            ],
        ),
    ]
