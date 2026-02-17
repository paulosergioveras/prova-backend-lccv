from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .choices import DimensaoItemAvaliacao

'''
AvaliacaoDesempenho é referenciado por string em ForeignKey
nenhuma importação necessária para evitar dependência circular
'''


class TipoItemAvaliacaoDesempenho(models.Model):
    dimensao = models.CharField(
        max_length=30,
        choices=DimensaoItemAvaliacao.choices
    )

    tipo_item_avaliacao_desempenho = models.TextField()
    descricao = models.TextField()

    class Meta:
        verbose_name = 'Tipo de Item de Avaliação de Desempenho'
        verbose_name_plural = 'Tipos de Itens de Avaliação de Desempenho'
        ordering = ['dimensao']

    def __str__(self):
        return self.dimensao


class ItemAvaliacaoDesempenho(models.Model):
    avaliacao = models.ForeignKey(
        'AvaliacaoDesempenho',
        on_delete=models.CASCADE,
        related_name='itens'
    )
     
    tipo_item_avaliacao_desempenho = models.ForeignKey(
        'TipoItemAvaliacaoDesempenho',
        on_delete=models.PROTECT,
        related_name='tipos'
    )

    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Item de Avaliação de Desempenho'
        verbose_name_plural = 'Itens de Avaliações de Desempenho'
        ordering = ['tipo_item_avaliacao_desempenho']
    
    def __str__(self):
        return self.tipo_item_avaliacao_desempenho
