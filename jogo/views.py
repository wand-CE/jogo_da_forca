import os
import random
from io import BytesIO

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView
from xhtml2pdf import pisa

from jogo.forms import LetraForm, RelatorioFiltroForm
from jogo.models import Jogo, Letra
from temaProfessor.models import Tema, Palavra
from jogo.util import GeraPDFMixin
from jogo_da_forca import settings


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_professor'] = user.groups.filter(name='Professor').exists()
        return context


class ListarTemasView(ListView):
    model = Tema
    template_name = 'temas/listar_temas.html'
    context_object_name = 'temas'


class JogoForcaView(View):
    template_name = 'jogo/jogo_forca.html'
    form_class = LetraForm

    def get(self, request, *args, **kwargs):
        tema_id = kwargs.get('tema_id')
        tema = get_object_or_404(Tema, id=int(tema_id))
        palavras = Palavra.objects.filter(tema=tema)

        if not palavras:
            return render(request, self.template_name, {'tema': tema, 'error': 'Tema sem palavras cadastradas.'})

        palavra = random.choice(palavras)

        jogador = request.user if request.user.is_authenticated else None

        # Cria um novo jogo para o jogador
        if jogador:
            jogo = Jogo.objects.create(palavra=palavra, jogador=jogador, )
        else:
            jogo = Jogo.objects.create(palavra=palavra)

        context = {
            'tema': tema,
            'palavra': palavra.palavra,
            'jogo_id': jogo.id,
            'acertos': list(jogo.acertos.values_list('letra', flat=True)),
            'erros': list(jogo.erros.values_list('letra', flat=True)),
            'resultado': jogo.calcular_resultado() if jogo else 'Em andamento',
            'form': self.form_class(),
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'palavra': palavra.palavra,
                'acertos': context['acertos'],
                'erros': context['erros'],
                'resultado': context['resultado'],
            })

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            letra = form.cleaned_data['letra'].upper()
            tema_id = kwargs.get('tema_id')
            tema = get_object_or_404(Tema, id=tema_id)
            palavras = Palavra.objects.filter(tema=tema)

            if not palavras:
                return JsonResponse({'error': 'Nenhuma palavra encontrada para este tema.'}, status=400)

            palavra = random.choice(palavras)
            jogador = request.user if request.user.is_authenticated else None

            # Obtém o ID do jogo do formulário
            jogo_id = request.POST.get('jogo_id')
            jogo = get_object_or_404(Jogo, id=jogo_id, jogador=jogador)

            if letra and len(letra) == 1:
                if letra in palavra.palavra.upper():
                    jogo.acertos.add(Letra.objects.get_or_create(letra=letra)[0])
                else:
                    jogo.erros.add(Letra.objects.get_or_create(letra=letra)[0])

                jogo.save()

            return JsonResponse({
                'palavra': palavra.palavra,
                'acertos': list(jogo.acertos.values_list('letra', flat=True)),
                'erros': list(jogo.erros.values_list('letra', flat=True)),
                'resultado': jogo.calcular_resultado(),
            })

        return JsonResponse({'error': 'Dados inválidos.'}, status=400)


class RelatorioAlunosJogaramView(GeraPDFMixin, ListView):
    template_name = 'alunos_jogaram.html'  # Template para HTML
    pdf_template_name = 'relatorios/pdf_alunos_jogaram.html'  # Template para PDF
    model = Jogo
    context_object_name = 'jogos'

    def get_queryset(self):
        form = RelatorioFiltroForm(self.request.GET)
        jogos = Jogo.objects.all()

        if form.is_valid():
            tema = form.cleaned_data.get('tema')
            data_inicio = form.cleaned_data.get('data_inicio')
            data_fim = form.cleaned_data.get('data_fim')

            if tema:
                jogos = jogos.filter(palavra__tema=tema)
            if data_inicio and data_fim:
                jogos = jogos.filter(data_jogo__range=[data_inicio, data_fim])

        return jogos.filter(jogador__isnull=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RelatorioFiltroForm(self.request.GET)
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get('format') == 'pdf':
            return self.render_to_pdf()
        return super().get(request, *args, **kwargs)

    def render_to_pdf(self):
        queryset = self.get_queryset()  # Carrega os dados do queryset
        context = {'jogos': queryset,
                   'form': RelatorioFiltroForm(self.request.GET)}  # Passa os dados corretos para o contexto
        template = get_template(self.pdf_template_name)
        html = template.render(context)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return HttpResponse('Erro ao gerar o PDF.', status=500)


class GeraJogoForcaPDFView(View):
    template_name = 'jogo/pdf_jogo_forca.html'

    def get(self, request, tema_id, palavra_id, *args, **kwargs):
        tema = get_object_or_404(Tema, id=tema_id)
        palavra = get_object_or_404(Palavra, id=palavra_id)

        context = {
            'tema': tema,
            'palavra': palavra.palavra,
            'request': request,
        }

        return self.render_to_pdf(context)

    def render_to_pdf(self, context):
        template = get_template(self.template_name)
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="jogo_forca.pdf"'

        pisa_status = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=response)
        if pisa_status.err:
            return HttpResponse('Erro ao gerar o PDF', status=500)
        return response
