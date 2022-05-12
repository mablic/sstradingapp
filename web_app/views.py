from re import sub
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from matplotlib.style import context
from .models import Model
from datetime import date, timedelta

MODEL = Model()

def home(request):
    return render(request, 'web_app/home.html')

def about(request):
    return render(request, 'web_app/about.html')

# this is for sending message to the author
def message(request):
    if request.method == 'POST':
        userName = 'Anonymous' if request.POST['name'] == ',' else request.POST['name']
        subject = 'Anonymous' if request.POST['subject'] == '' else request.POST['subject']
        fromEmail = 'Anonymous' if request.POST['fromEmail'] == '' else request.POST['fromEmail']
        body= 'NA' if request.POST['msg'] == '' else request.POST['msg']
        MODEL.send_email(userName, subject, fromEmail, body)

    return render(request, 'web_app/message.html')

# trademodel get the VaR calculation, graph the model as well as percentage of the model into the
def tradeModel(request):
    if request.method == 'GET':
        ticker = MODEL.get_all_ticker_from_db()
        context = {
            'ticker': ticker
        }
        return render(request, 'web_app/tradeModel.html', context)
    if request.method == 'POST':
        # this is get the general ticker POST request
        startDate = '2021-01-01' if request.POST['startDate'] == '' else request.POST['startDate']
        endDate = '2021-06-30' if request.POST['endDate'] == '' else request.POST['endDate']
        if 'ticker' in request.POST:
            ticker = request.POST['ticker']
            chartType= 'line' if request.POST['chartType'] == '' else request.POST['chartType']
            MODEL.run_base_graph(ticker, startDate, endDate, chartType)
        # this is for the VaR calculation
        if 'positions[]' in request.POST:
            tickers = request.POST.getlist('tickers[]')
            positions = request.POST.getlist('positions[]')
            varList = MODEL.get_VaR_value(startDate, endDate, tickers, positions)
            context = {
                'varList': varList
            }
            return JsonResponse(context)           

    return render(request, 'web_app/tradeModel.html')

def optionModel(request):
    if request.method == 'GET':
        ticker = MODEL.get_all_ticker_from_db()
        context = {
            'ticker': ticker
        }
        return render(request, 'web_app/optionModel.html', context)
    if request.method == 'POST':
        if 'getStrikePrice' in request.POST:
            ticker = request.POST['ticker']
            expirationDate = request.POST['expirationDate']
            expirationDate = date.today().strftime("%Y-%m-%d") if request.POST['expirationDate'] == '' else request.POST['expirationDate']
            putCallList = MODEL.get_option_prices(ticker, expirationDate)
            context = {
                'putCallList': putCallList
            }
            return JsonResponse(context)    
    return render(request, 'web_app/optionModel.html')