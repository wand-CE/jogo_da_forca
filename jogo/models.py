from django.contrib.auth.models import User
from django.db import models

from temaProfessor.models import Palavra


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
