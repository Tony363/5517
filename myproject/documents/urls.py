from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('upload/', views.document_upload, name='document_upload'),
    path('view/', views.document_view, name='document_view'),
    path('logout/', views.logout_view, name='logout'),
    path('delete/<str:key>/', views.document_delete, name='document_delete'),
    path('<filename>', views.serve_document, name='serve_document'),
]
