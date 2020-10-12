from dataclasses import asdict

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.views import View

from core.currency.exceptions import InsufficientCashError
from core.snacks.exceptions import NegativeSnackQuantityError, SnackNotFound
from web_utils.http_status_codes import HTTP_402_PAYMENT_REQUIRED
from .services import list_snacks, recharge_snack, buy_snack


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
        except SnackNotFound as exception:
            return HttpResponseNotFound(str(exception))
        else:
            return JsonResponse({'snack': asdict(snack)})


class BuySnacksView(View):

    def post(self, request):
        name = request.POST.get('name')
        try:
            change = buy_snack(name=name)
        except InsufficientCashError as exception:
            return HttpResponse(status=HTTP_402_PAYMENT_REQUIRED, content=str(exception))
        return JsonResponse({'change': change.cash_values})
