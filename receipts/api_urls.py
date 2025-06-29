from django.urls import path
from . import api_views
from .api_views import RegisterView, ReceiptListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('upload/', api_views.upload_receipt_api),
    path('receipts/<int:receipt_id>/edit/', api_views.update_receipt),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('receipts/', ReceiptListView.as_view(), name='receipts'),
]
