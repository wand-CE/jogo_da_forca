from django.conf.urls.static import static
from django.urls import path

from jogo import views
from jogo_da_forca import settings

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('temas/', views.ListarTemasView.as_view(), name='listaTemas'),
    path('jogar/<int:tema_id>/', views.JogoForcaView.as_view(), name='jogarForca'),
    path('relatorio-alunos/pdf/', views.RelatorioAlunosJogaramView.as_view(),
         name='relatorio_alunos_pdf'),
    path('gerar-pdf/<int:tema_id>/<int:palavra_id>/', views.GeraJogoForcaPDFView.as_view(),
         name='gerar_jogo_forca_pdf'),
]
