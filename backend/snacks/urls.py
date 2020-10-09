from django.urls import path

from .views import SnacksView

urlpatterns = (
    path('', SnacksView.as_view(), name='snacks-api'),
)
