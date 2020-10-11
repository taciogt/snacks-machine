from django.http import JsonResponse
from django.views import View

from .services import insert_cash


class CurrencyView(View):
    def post(self, request):
        cash_value = float(request.POST.get('cash_value'))
        cash_amount = insert_cash(cash_value=cash_value)
        return JsonResponse({
            'cash_amount': cash_amount.cash_values,
            'total_value': cash_amount.total_value
        })
