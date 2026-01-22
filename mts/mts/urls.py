from django.urls import path
from mtsapp import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('create/', views.create_chat, name='create_chat'),
    path('chat/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('chat/<int:chat_id>/delete/', views.chat_delete, name='chat_delete'),
]

