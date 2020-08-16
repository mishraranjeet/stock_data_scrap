from django.shortcuts import render
from django.http import JsonResponse
from .trading_scrap import intradingview
from rest_framework.decorators import api_view
# Create your views here.


@api_view(['GET'])
def scrap_data(request):
    if request.method == 'GET':
        symbol = request.GET['symbol']
        data = intradingview(symbols=symbol)
        return JsonResponse({"success":True,"data":data},safe=False)
