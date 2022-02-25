from re import sub
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from matplotlib.style import context
from .models import Model

MODEL = Model()

def home(request):
    return render(request, 'web_app/home.html')

def about(request):
    return render(request, 'web_app/about.html')

def message(request):
    if request.method == 'POST':
        userName = 'Anonymous' if request.POST['name'] == ',' else request.POST['name']
        subject = 'Anonymous' if request.POST['subject'] == '' else request.POST['subject']
        fromEmail = 'Anonymous' if request.POST['fromEmail'] == '' else request.POST['fromEmail']
        body= 'NA' if request.POST['msg'] == '' else request.POST['msg']
        MODEL.send_email(userName, subject, fromEmail, body)

    return render(request, 'web_app/message.html')

def tradeModel(request):
    if request.method == 'GET':
        ticker = MODEL.get_all_ticker_from_db()
        context = {
            'ticker': ticker
        }
        # print(context)
        return render(request, 'web_app/tradeModel.html', context)
    if request.method == 'POST':
        # print(request.POST)
        if 'ticker' in request.POST:
            ticker = request.POST['ticker']
            startDate = '2021-01-01' if request.POST['startDate'] == '' else request.POST['startDate']
            endDate = '2021-06-30' if request.POST['endDate'] == '' else request.POST['endDate']
            chartType= 'line' if request.POST['chartType'] == '' else request.POST['chartType']
            # print('IN VIEW -----------> ticker='+ticker+';startDate='+startDate+';endDate='+endDate+';charType='+chartType)
            MODEL.run_base_graph(ticker, startDate, endDate, chartType)
    return render(request, 'web_app/tradeModel.html')