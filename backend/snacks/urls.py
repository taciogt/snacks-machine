from django.urls import path

from .views import SnacksView, BuySnacksView

urlpatterns = (
    path('', SnacksView.as_view(), name='snacks-endpoint'),
    path('buy/', BuySnacksView.as_view(), name='buy_snacks-endpoint'),
)
