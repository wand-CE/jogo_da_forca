from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, FormView

from usuarios.forms import UsuarioForm


class CriarUsuarioView(CreateView):
    form_class = UsuarioForm
    template_name = "usuario/criar_usuario.html"
    success_url = reverse_lazy('logarUsuario')

    def form_valid(self, form):
        try:
            grupo, created = Group.objects.get_or_create(name=form.cleaned_data['tipo_usuario'])
            usuario = form.save()
            usuario.groups.add(grupo)
            messages.success(self.request, f'Usuário {usuario.username} cadastrado com sucesso!')
            return super().form_valid(form)

        except Exception as e:
            print(e)
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request,
                       'Não foi possível cadastrar o usuário!!!')
        print(form)
        return super().form_invalid(form)


class LogarUsuarioView(FormView):
    template_name = "usuario/logar_usuario.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        data = form.cleaned_data
        username = data.get('username', '')
        password = data.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
            messages.success(self.request, f'Bem-vindo, {username}!')
            return super().form_valid(form)

        messages.error(self.request, 'Usuário ou senha incorretos.')
        return self.form_invalid(form)


class DeslogarUsuarioView(View):
    success_url = reverse_lazy('logarUsuario')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            messages.success(self.request, f'Usuário Deslogado!')
        return redirect(self.success_url)
