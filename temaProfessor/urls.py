from django.urls import path

from temaProfessor import views

urlpatterns = [
    path('meustemas/', views.ListarTemasProfessorView.as_view(), name='listaTemaProfessor'),
    path('criartema/', views.CriarTemaView.as_view(), name='criarTema'),
    path('editartema/<int:pk>/', views.EditarTemaView.as_view(), name='editarTema'),
    path('excluirtema/<int:pk>/', views.ExcluirTemaView.as_view(), name='excluirTema'),
]
