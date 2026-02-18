from rest_framework import serializers
from ..models import TipoItemAvaliacaoDesempenho, ItemAvaliacaoDesempenho


class TipoItemAvaliacaoDesempenhoSerializer(serializers.ModelSerializer):
    '''
    Serializer para o modelo TipoItemAvaliacaoDesempenho
    '''

    class Meta:
        model = TipoItemAvaliacaoDesempenho
        fields = '__all__'
        read_only_fields = ['id']


class ItemAvaliacaoDesempenhoSerializer(serializers.ModelSerializer):
    '''
    Serializer para o modelo ItemAvaliacaoDesempenho
    '''

    class Meta:
        model = ItemAvaliacaoDesempenho
        fields = '__all__'
        read_only_fields = ['id', 'avaliacao', 'tipo_item_avaliacao_desempenho']
