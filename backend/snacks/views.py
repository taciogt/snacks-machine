from dataclasses import asdict

from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View

from core.snacks.exceptions import NegativeSnackQuantityError
from .services import list_snacks, recharge_snack


class SnacksView(View):
    def get(self, request):
        snacks = list_snacks()
        serializable_snacks = list(map(asdict, snacks))
        return JsonResponse({'items': serializable_snacks})

    def post(self, request):
        name = request.POST.get('name')
        quantity = int(request.POST.get('quantity'))
        try:
            snack = recharge_snack(name=name, quantity=quantity)
        except NegativeSnackQuantityError as exception:
            return HttpResponseBadRequest(str(exception))
        else:
            return JsonResponse({'snack': asdict(snack)})
