from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from ..models import AvaliacaoDesempenho
from ..models.choices import StatusAvaliacao
from ..serializers.avaliacao import AvaliacaoDesempenhoSerializer


class AvaliacaoViewSet(viewsets.ModelViewSet):
    '''
    ViewSet para o modelo AvaliacaoDesempenho. Permite as operações CRUD padrão e ações customizadas
    de ciclo de avaliação.
    '''

    queryset = AvaliacaoDesempenho.objects.all()
    serializer_class = AvaliacaoDesempenhoSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['colaborador', 'supervisor', 'status_avaliacao', 'mes_competencia']
    search_fields = ['colaborador__nome', 'supervisor__nome']
    ordering_fields = ['mes_competencia', 'nota']
    ordering = ['-mes_competencia']

    def validar_status_avaliacao(self, obj, permitidos):
        if obj.status_avaliacao not in permitidos:
            raise serializers.ValidationError('ação não permitida no status atual')

    @action(detail=True, methods=['post'], url_path='iniciar-avaliacao')
    def iniciar(self, request, pk=None):
        ''' Muda status de CRIADA para EM_ELABORACAO '''

        avaliacao = self.get_object()
        avaliacao.iniciar()
        serializer = self.get_serializer(avaliacao)
        return Response({
            'message': 'avaliação iniciada',
            'data': serializer.data,
        })

    @action(detail=True, methods=['post'], url_path='dar-feedback')
    def dar_feedback(self, request, pk=None):
        ''' Muda status de EM_ELABORACAO para EM_AVALIACAO '''

        avaliacao = self.get_object()
        avaliacao.dar_feedback()
        serializer = self.get_serializer(avaliacao)
        return Response({
            'message': 'feedback dado',
            'data': serializer.data,
        })

    @action(detail=True, methods=['post'], url_path='concluir-avaliacao')
    def concluir(self, request, pk=None):
        ''' Muda status de EM_AVALIACAO para CONCLUIDA '''

        avaliacao = self.get_object()
        avaliacao.concluir()
        serializer = self.get_serializer(avaliacao)
        return Response({
            'message': 'avaliação concluída',
            'data': serializer.data,
        })

    @action(detail=True, methods=['post'], url_path='atualizar-nota')
    def atualizar_nota(self, request, pk=None):
        '''
        Recalcula a nota da avaliação com base nos itens.
        Somente permitido quando a avaliação está em elaboração.
        '''

        avaliacao = self.get_object()
        permitidos = [StatusAvaliacao.EM_ELABORACAO]
        self.validar_status_avaliacao(avaliacao, permitidos)

        avaliacao.atualizar_nota()
        serializer = self.get_serializer(avaliacao)
        return Response({
            'message': 'nota atualizada',
            'data': serializer.data,
        })
