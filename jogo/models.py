from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Tema(models.Model):
    nome = models.CharField(max_length=100)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    estar_logado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.criado_por.groups.filter(name='professor').exists():
            raise ValidationError('Somente "Professores" podem criar um tema.')
        super().save(*args, **kwargs)


class Palavra(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    palavra = models.CharField(max_length=100)
    dica = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.palavra


class Letra(models.Model):
    letra = models.CharField(max_length=1)

    def __str__(self):
        return self.letra


class Jogo(models.Model):
    palavra = models.ForeignKey(Palavra, on_delete=models.CASCADE)
    jogador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    acertos = models.ManyToManyField(Letra, related_name='acertos', blank=True)
    erros = models.ManyToManyField(Letra, related_name='erros', blank=True)
    data_jogo = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.jogador:
            return f'Jogado por {self.jogador.username} em {self.data_jogo}'
        return f'Jogado por anônimo em {self.data_jogo}'

    def calcular_resultado(self):
        palavra = self.palavra.palavra.upper()

        letras_acertadas = set(letra.upper() for letra in self.acertos.values_list('letra', flat=True))
        letras_erradas = set(letra.upper() for letra in self.erros.values_list('letra', flat=True))

        letras_palavra = set(palavra.replace(' ', ''))

        acertou = letras_palavra.issubset(letras_acertadas)
        perdeu = len(letras_erradas) >= 6

        if acertou:
            return 'Vencedor'
        elif perdeu:
            return 'Perdedor'
        return 'Em andamento'
