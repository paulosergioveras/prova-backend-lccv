from rest_framework import routers
from django.urls import path, include

from .views.colaborador import ColaboradorViewSet
from .views.avaliacao import AvaliacaoViewSet
from .views.item_avaliacao import (
    TipoItemAvaliacaoViewSet,
    ItemAvaliacaoViewSet,
)

router = routers.DefaultRouter()
router.register(r'colaboradores', ColaboradorViewSet, basename='colaborador')
router.register(r'avaliacoes', AvaliacaoViewSet, basename='avaliacao')
router.register(r'tipos-itens', TipoItemAvaliacaoViewSet, basename='tipoitem')
router.register(r'itens-avaliacao', ItemAvaliacaoViewSet, basename='itemavaliacao')

urlpatterns = [
    path('', include(router.urls)),
]
