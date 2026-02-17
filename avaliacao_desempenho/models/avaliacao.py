from django.db import models
from django.db import transaction
from decimal import Decimal
from django.db.models import Sum

from .choices import StatusAvaliacao
from .colaborador import Colaborador


class AvaliacaoDesempenho(models.Model):
    colaborador = models.ForeignKey(
        Colaborador,
        on_delete=models.CASCADE,
        related_name='avaliacao_recebida'
    )

    supervisor = models.ForeignKey(
        Colaborador,
        on_delete=models.CASCADE,
        related_name='avaliacao_supervisionada'
    )

    mes_competencia = models.DateField()

    status_avaliacao = models.CharField(
        max_length=30,
        choices=StatusAvaliacao.choices,
        default=StatusAvaliacao.CRIADA
    )

    nota = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    sugestoes_supervisor = models.TextField(blank=True, null=True)
    observacoes_avaliado = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Avaliação de Desempenho'
        verbose_name_plural = 'Avaliações de Desempenho'
        unique_together = ('colaborador', 'mes_competencia')
        ordering = ['-mes_competencia']

    def __str__(self):
        return f'Avaliação de {self.colaborador.nome} - {self.mes_competencia} - {self.status_avaliacao}'

    def save(self, *args, **kwargs):
        nova_avaliacao = self.pk is None
        super().save(*args, **kwargs)

        if nova_avaliacao:
            from .item_avaliacao import ItemAvaliacaoDesempenho
            from django.apps import apps

            with transaction.atomic():
                TipoItemAvaliacaoDesempenho = apps.get_model(
                    'avaliacao_desempenho', 'TipoItemAvaliacaoDesempenho'
                )
                tipos = TipoItemAvaliacaoDesempenho.objects.all()
                item_criar = [
                    ItemAvaliacaoDesempenho(
                        avaliacao=self,
                        tipo_item_avaliacao_desempenho=tipo,
                        nota=1,
                    )
                    for tipo in tipos
                ]
                ItemAvaliacaoDesempenho.objects.bulk_create(item_criar)


    def iniciar(self):
        if self.status_avaliacao == StatusAvaliacao.CRIADA:
            self.status_avaliacao = StatusAvaliacao.EM_ELABORACAO
            self.save()

    def dar_feedback(self):
        if self.status_avaliacao == StatusAvaliacao.EM_ELABORACAO:
            self.status_avaliacao = StatusAvaliacao.EM_AVALIACAO
            self.save()

    def concluir(self):
        if self.status_avaliacao == StatusAvaliacao.EM_AVALIACAO:
            self.status_avaliacao = StatusAvaliacao.CONCLUIDA
            self.save()

    def atualizar_nota(self):
        with transaction.atomic():
            from django.apps import apps
            TipoItemAvaliacaoDesempenho = apps.get_model(
                'avaliacao_desempenho', 'TipoItemAvaliacaoDesempenho'
            )
            total_tipos = TipoItemAvaliacaoDesempenho.objects.count()

            if total_tipos == 0:
                percentual = Decimal('0.00')
            else:
                soma_notas = self.itens.aggregate(total=Sum('nota'))['total'] or 0
                percentual = (Decimal(soma_notas) / Decimal(total_tipos * 5)) * Decimal('100')
                percentual = percentual.quantize(Decimal('0.01'))

            AvaliacaoDesempenho.objects.filter(pk=self.pk).update(nota=percentual)
            self.nota = percentual
