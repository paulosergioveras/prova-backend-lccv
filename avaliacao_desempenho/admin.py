from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from .models import (
    AvaliacaoDesempenho,
    Colaborador,
    ItemAvaliacaoDesempenho,
    TipoItemAvaliacaoDesempenho,
)
from models.choices import StatusAvaliacao


@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    '''
    Configurações do Django admin para o modelo Colaborador.
    '''
    
    model = Colaborador
    fields = ('nome', 'email', 'cpf',)
    search_fields = ('nome', 'email', 'cpf',)
    ordering = ('nome',)


class ItemAvaliacaoInline(admin.TabularInline):
    '''
    Inline para editar itens de avaliação dentro da avaliação.
    '''

    model = ItemAvaliacaoDesempenho
    extra = 0
    fields = ('tipo_item_avaliacao_desempenho', 'nota', 'observacoes',)
    readonly_fields = ('tipo_item_avaliacao_desempenho',)
    can_delete = False
   
    def has_add_permission(self, request, obj=None):
        '''
        Impede a adição de novos itens inline.
        '''
        
        return False


@admin.register(AvaliacaoDesempenho)
class AvaliacaoDesempenhoAdmin(admin.ModelAdmin):
    '''
    Configurações do Django admin para o modelo AvaliacaoDesempenho.
    '''

    list_display = (
        'colaborador',
        'supervisor',
        'mes_competencia',
        'status_avaliacao',
        'nota',
    )

    list_filter = ('status_avaliacao', 'mes_competencia',)

    search_fields = (
        'colaborador__nome',
        'supervisor__nome',
    )

    readonly_fields = ('nota',)
    inlines = (ItemAvaliacaoInline,)

    actions = [
        'action_iniciar',
        'action_dar_feedback',
        'action_concluir',
    ]

    @admin.action(description=_('Iniciar avaliação'))
    def _transicionar(self, request, queryset, status_requerido, metodo, label_acao):
        elegiveis = queryset.filter(status_avaliacao=status_requerido)
        ignorados = queryset.exclude(status_avaliacao=status_requerido).count()

        count = 0
        for avaliacao in elegiveis:
            getattr(avaliacao, metodo)()
            count += 1

        if count:
            self.message_user(
                request,
                f'{count} avaliação(ões) {label_acao} com sucesso.',
            )
        if ignorados:
            self.message_user(
                request,
                f'{ignorados} avaliação(ões) ignorada(s) por estarem em status incompatível.',
                level=messages.WARNING,
            )

    @admin.action(description=_('Iniciar avaliações selecionadas'))
    def action_iniciar(self, request, queryset):
        self._transicionar(
            request, queryset, StatusAvaliacao.CRIADA, 'iniciar', 'iniciadas'
        )

    @admin.action(description=_('Enviar para feedback'))
    def action_dar_feedback(self, request, queryset):
        self._transicionar(
            request,
            queryset,
            StatusAvaliacao.EM_ELABORACAO,
            'dar_feedback',
            'enviadas para avaliação'
        )

    @admin.action(description=_('Concluir avaliações selecionadas'))
    def action_concluir(self, request, queryset):
        self._transicionar(
            request, queryset, StatusAvaliacao.EM_AVALIACAO, 'concluir', 'concluídas'
        )


@admin.register(TipoItemAvaliacaoDesempenho)
class TipoItemAvaliacaoDesempenhoAdmin(admin.ModelAdmin):
    '''
    Configurações do Django admin para o modelo TipoItemAvaliacaoDesempenho.
    '''
    
    list_display = ('dimensao', 'tipo_item_avaliacao_desempenho',)
    list_filter = ('dimensao',)
    search_fields = ('tipo_item_avaliacao_desempenho',)
    ordering = ('dimensao', 'tipo_item_avaliacao_desempenho',)


@admin.register(ItemAvaliacaoDesempenho)
class ItemAvaliacaoDesempenhoAdmin(admin.ModelAdmin):
    '''
    Configurações do Django admin para o modelo ItemAvaliacaoDesempenho
    '''

    list_display = ('avaliacao', 'tipo_item_avaliacao_desempenho', 'nota',)

    list_filter = (
        'tipo_item_avaliacao_desempenho__dimensao',
        'nota',
    )

    search_fields = (
        'avaliacao__colaborador__nome',
        'avaliacao__supervisor__nome',
        'tipo_item_avaliacao_desempenho__dimensao',
    )

    ordering = ('avaliacao', 'tipo_item_avaliacao_desempenho',)
    
    def save_model(self, request, obj, form, change):
        '''
        Atualiza a nota da avaliação após salvar o item.
        '''

        super().save_model(request, obj, form, change)
        if change:
            obj.avaliacao.atualizar_nota()
