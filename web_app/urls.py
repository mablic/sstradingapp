from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('', views.home, name='web_app_home'),
    path('about/', views.about, name='web_app_about'),
    path('message/', views.message, name='web_app_message'),
    path('trade_model/', views.tradeModel, name='web_app_trade_model'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)