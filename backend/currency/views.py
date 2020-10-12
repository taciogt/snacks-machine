from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View

from core.currency.exceptions import InvalidCashValueError
from .services import insert_cash, retrieve_cash


class CurrencyView(View):
    def post(self, request):
        cash_value = float(request.POST.get('cash_value'))
        try:
            cash_amount = insert_cash(cash_value=cash_value)
        except InvalidCashValueError as exception:
            return HttpResponseBadRequest(str(exception))
        else:
            return JsonResponse({
                'cash_amount': cash_amount.cash_values,
                'total_value': cash_amount.total_value
            })

    def delete(self, request):
        cash_amount = retrieve_cash()
        return JsonResponse({
            'cash_amount': cash_amount.cash_values,
            'total_value': cash_amount.total_value
        })
