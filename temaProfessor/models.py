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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tema', 'palavra'], name='unique_palavra_tema')
        ]

    def __str__(self):
        return self.palavra

    def save(self, *args, **kwargs):
        # Transformar a palavra em maiúsculas antes de salvar
        self.palavra = self.palavra.upper()
        super().save(*args, **kwargs)
