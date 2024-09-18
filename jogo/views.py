import random

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from jogo.forms import LetraForm
from jogo.models import Jogo, Letra
from temaProfessor.models import Tema, Palavra


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'


class ListarTemasView(ListView):
    model = Tema
    template_name = 'temas/listar_temas.html'
    context_object_name = 'temas'


class DetalharTemaView(DetailView):
    template_name = "temas/detalhar_tema.html"
    model = Tema


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
