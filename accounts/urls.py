from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='index_login'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cadastro_1/', views.cadastro_1, name='cadastro_1'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
