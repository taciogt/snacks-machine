from django.urls import path

from .views import CurrencyView

urlpatterns = (
    path('', CurrencyView.as_view(), name='currency-api'),
)
