from dataclasses import asdict

from django.http import JsonResponse
from django.views import View

from .services import list_snacks


class SnacksView(View):
    def get(self, request):
        snacks = list_snacks()
        serializable_snacks = list(map(asdict, snacks))
        return JsonResponse({'items': serializable_snacks})
