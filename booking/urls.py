from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book, name='book'),
    path('book/<int:service_id>/', views.book, name='book_service'),
    path('success/<int:pk>/', views.success, name='success'),
    path('appointments/', views.appointments_list, name='appointments'),
]
