from django.urls import path
from .views import upload_receipt, dashboard, edit_receipt

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('upload/', upload_receipt, name='upload'),
    path('edit/<int:receipt_id>/', edit_receipt, name='edit_receipt'),
]
