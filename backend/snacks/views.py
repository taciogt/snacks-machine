from django.http import JsonResponse
from django.views import View

from .services import list_snacks


class SnacksView(View):
    def get(self, request):
        return JsonResponse({'items': list_snacks()})
