from django.db import models


class Colaborador(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return self.nome
