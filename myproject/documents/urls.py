from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.document_upload, name='document_upload'),
    path('view/', views.document_view, name='document_view'),
    path('delete/<int:pk>/', views.document_delete, name='document_delete'),
]
