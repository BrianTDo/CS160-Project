from django.urls import path
from .views import transaction

urlpatterns = [
    path('deposit/', transaction),
]