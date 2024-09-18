import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from temaProfessor.models import Tema, Palavra


class ProfessorMixin:
    def is_professor(self, request):
        return


class ListarTemasProfessorView(LoginRequiredMixin, ProfessorMixin, ListView):
    model = Tema
    template_name = "professor/listar_temas.html"
    context_object_name = "temas"

    def get_queryset(self):
        return Tema.objects.filter(criado_por=self.request.user)


class CriarTemaView(LoginRequiredMixin, CreateView):
    model = Tema
    template_name = "professor/criar_jogo.html"
    fields = ["nome", "estar_logado"]
    success_url = reverse_lazy('listaTemaProfessor')

    def form_valid(self, form):
        if not self.request.user.groups.filter(name='professor').exists():
            raise PermissionDenied('Você não tem permissão para criar um tema.')

        form.instance.criado_por = self.request.user
        response = super().form_valid(form)

        # Recuperar palavras do formulário
        palavras_json = self.request.POST.get('palavras', '[]')
        palavras = json.loads(palavras_json)

        if not palavras:
            messages.error(self.request, 'Você deve adicionar pelo menos uma palavra.')
            return self.form_invalid(form)

        for palavra_text in palavras:
            Palavra.objects.create(tema=self.object, palavra=palavra_text)

        return response


class EditarTemaView(LoginRequiredMixin, UpdateView):
    model = Tema
    template_name = "professor/editar_tema.html"
    fields = ["nome", "estar_logado"]
    success_url = reverse_lazy('listaTemaProfessor')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['palavras'] = Palavra.objects.filter(tema=self.object)
        return data

    def form_valid(self, form):
        if not self.request.user.groups.filter(name='professor').exists():
            raise PermissionDenied('Você não tem permissão para editar este tema.')

        form.instance.criado_por = self.request.user
        response = super().form_valid(form)

        # Recuperar palavras do formulário
        palavras_json = self.request.POST.get('palavras', '[]')
        palavras = json.loads(palavras_json)

        if not palavras:
            messages.error(self.request, 'Você deve adicionar pelo menos uma palavra.')
            return redirect(reverse('editarTema', kwargs={'pk': self.object.pk}))

        # Excluir palavras antigas
        Palavra.objects.filter(tema=self.object).delete()

        # Adicionar palavras novas
        for palavra_text in palavras:
            palavra_text = palavra_text.upper()  # Garantir que as palavras estejam em maiúsculas
            try:
                Palavra.objects.create(tema=self.object, palavra=palavra_text)
            except IntegrityError:
                messages.error(self.request, f'Palavra duplicada detectada e ignorada: {palavra_text}')

        return response


class ExcluirTemaView(DeleteView):
    model = Tema
    template_name = "professor/excluir_tema.html"
    success_url = reverse_lazy('listaTemaProfessor')
    context_object_name = "tema"

    def form_valid(self, form):
        messages.success(self.request, f'Tema excluído!!!')
        return super().form_valid(form)
