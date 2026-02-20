from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from ..models import TipoItemAvaliacaoDesempenho, ItemAvaliacaoDesempenho
from ..serializers.item_avaliacao import (
    TipoItemAvaliacaoDesempenhoSerializer,
    ItemAvaliacaoDesempenhoSerializer,
)


class TipoItemAvaliacaoViewSet(viewsets.ModelViewSet):
    ''' CRUD para tipos de item de avaliação. '''

    queryset = TipoItemAvaliacaoDesempenho.objects.all()
    serializer_class = TipoItemAvaliacaoDesempenhoSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['dimensao']
    search_fields = ['dimensao', 'tipo_item_avaliacao_desempenho']
    ordering_fields = ['dimensao']


class ItemAvaliacaoViewSet(viewsets.ModelViewSet):
    ''' CRUD para itens de avaliação individuais. '''
    queryset = ItemAvaliacaoDesempenho.objects.all()
    serializer_class = ItemAvaliacaoDesempenhoSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['avaliacao', 'tipo_item_avaliacao_desempenho', 'nota']
    search_fields = [
        'avaliacao__colaborador__nome', 
        'tipo_item_avaliacao_desempenho__tipo_item_avaliacao_desempenho'
    ]
    ordering_fields = ['nota']
