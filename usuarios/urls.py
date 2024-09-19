from django.urls import path

from usuarios import views

urlpatterns = [
    path('registrar/', views.CriarUsuarioView.as_view(), name='registrarUsuario'),
    path('logar/', views.LogarUsuarioView.as_view(), name='logarUsuario'),
    path('deslogar/', views.DeslogarUsuarioView.as_view(), name='deslogarUsuario'),
    path('editar/', views.EditarUsuarioView.as_view(), name='editarUsuario'),
]
