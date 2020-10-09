from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from .services import list_snacks


class SnacksView(View):
    def get(self, request):
        return JsonResponse({'items': list_snacks()})
