from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('speaker/', views.speaker, name='speaker'),
    path('speaker/<int:pk>/', views.speaker, name='load_speaker'),
    path('chat/', views.chat, name='chat'),
    path('chat/<int:conversation>/', views.chat, name='chat'),
    path('answer/', views.answer, name='answer'),
    path('choices/', views.choices, name='choices'),
    #path('editor/', views.editor, name='editor'),
]
