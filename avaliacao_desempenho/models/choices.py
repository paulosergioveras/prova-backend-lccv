from django.db import models


class DimensaoItemAvaliacao(models.TextChoices):
    '''
    Modelo para representar as dimensções de uma avaliação
    tais como comportamento, entregas e trabalho em equipe.
    '''
    
    COMPORTAMENTO = 'COMPORTAMENTO', 'Comportamento'
    ENTREGAS = 'ENTREGAS', 'Entregas'
    TRABALHO_EQUIPE = 'TRABALHO_EQUIPE', 'Trabalho em equipe'


class StatusAvaliacao(models.TextChoices):
    '''
    Modelo para representar os status de uma avaliação
    como criada, em elaboração, em avaliação e concluída.
    '''

    CRIADA = 'CRIADA', 'Criada'
    EM_ELABORACAO = 'EM_ELABORACAO', 'Em elaboração'
    EM_AVALIACAO = 'EM_AVALIACAO', 'Em avaliação'
    CONCLUIDA = 'CONCLUIDA', 'Concluída'
