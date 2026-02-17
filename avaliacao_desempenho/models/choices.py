from django.db import models


class DimensaoItemAvaliacao(models.TextChoices):
    COMPORTAMENTO = 'COMPORTAMENTO', 'Comportamento'
    ENTREGAS = 'ENTREGAS', 'Entregas'
    TRABALHO_EQUIPE = 'TRABALHO_EQUIPE', 'Trabalho em equipe'


class StatusAvaliacao(models.TextChoices):
    CRIADA = 'CRIADA', 'Criada'
    EM_ELABORACAO = 'EM_ELABORACAO', 'Em elaboração'
    EM_AVALIACAO = 'EM_AVALIACAO', 'Em avaliação'
    CONCLUIDA = 'CONCLUIDA', 'Concluída'
