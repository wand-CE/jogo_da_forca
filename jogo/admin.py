from django.contrib import admin
from temaProfessor.models import Tema, Palavra


@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    fields = ['nome', 'estar_logado']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Palavra)
class PalavraAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'tema':
            # Filtra os temas para mostrar apenas aqueles do usuário atual
            kwargs['queryset'] = Tema.objects.filter(criado_por=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
