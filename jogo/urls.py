from django.urls import path

from jogo import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('temas/', views.ListarTemasView.as_view(), name='listaTemas'),
    # path('tema/<int:pk>/', views.DetalharTemaView.as_view(), name='detalheTema'),
    path('jogar/<int:tema_id>/', views.JogoForcaView.as_view(), name='jogarForca'),

]
