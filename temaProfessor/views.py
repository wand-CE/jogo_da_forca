import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from temaProfessor.models import Tema, Palavra


class ProfessorMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='professor').exists():
            messages.error(request, "Voce deve ser um professor pra acessar essa página")
            return redirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)


class ListarTemasProfessorView(ProfessorMixin, ListView):
    model = Tema
    template_name = "professor/listar_temas.html"
    context_object_name = "temas"

    def get_queryset(self):
        return Tema.objects.filter(criado_por=self.request.user)


class CriarTemaView(ProfessorMixin, CreateView):
    model = Tema
    template_name = "professor/criar_jogo.html"
    fields = ["nome", "estar_logado"]
    success_url = reverse_lazy('listaTemaProfessor')

    def form_valid(self, form):
        # Recuperar palavras do formulário
        palavras_json = self.request.POST.get('palavras', '[]')
        palavras = json.loads(palavras_json)

        if not palavras:
            messages.error(self.request, 'Você deve adicionar pelo menos uma palavra.')
            return self.form_invalid(form)

        form.instance.criado_por = self.request.user
        response = super().form_valid(form)

        for palavra_text in palavras:
            Palavra.objects.create(tema=self.object, palavra=palavra_text)

        return response


class EditarTemaView(ProfessorMixin, UpdateView):
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


class ExcluirTemaView(ProfessorMixin, DeleteView):
    model = Tema
    template_name = "professor/excluir_tema.html"
    success_url = reverse_lazy('listaTemaProfessor')
    context_object_name = "tema"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.criado_por != request.user:
            return HttpResponseForbidden("Você não tem permissão para excluir este tema.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, f'Tema excluído!!!')
        return super().form_valid(form)
