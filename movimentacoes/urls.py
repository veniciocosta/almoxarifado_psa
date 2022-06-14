from django.urls import path, reverse_lazy
from . import views  # arquivo views.py que está na app portal
from django.contrib.auth import views as auth_view

app_name='movimentacoes'

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', auth_view.LoginView.as_view(template_name='movimentacoes/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='movimentacoes/logout.html'), name='logout'),

    path('produto_lista/', views.produto_lista, name='produto_lista'),
    path('produto_lista/produto/', views.produto, name='produto'),
    path('produto_lista/produto/<int:pk>/', views.produto_submit, name='produto_submit'),
    path('produto_lista/produto/delete/<int:pk>/', views.produto_delete, name='produto_delete'),

    path('movimentacao_lista/', views.movimentacao_lista, name='movimentacao_lista'),
    path('movimentacao_lista/movimentacao/', views.movimentacao, name='movimentacao'),
    path('movimentacao_lista/movimentacao/<int:pk>/', views.movimentacao_submit, name='movimentacao_submit'),
    path('movimentacao_lista/movimentacao/delete/<int:pk>/', views.movimentacao_delete, name='movimentacao_delete'),
]
