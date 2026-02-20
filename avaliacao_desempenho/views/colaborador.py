from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from ..models import Colaborador
from ..serializers.colaborador import ColaboradorSerializer


class ColaboradorViewSet(viewsets.ModelViewSet):
    '''
    ViewSet para o modelo Colaborador. Fornece list, retrieve, create, update e delete.
    '''

    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['nome', 'email', 'cpf']
    search_fields = ['nome', 'email', 'cpf']
    ordering_fields = ['nome', 'email', 'cpf']
    ordering = ['nome']
