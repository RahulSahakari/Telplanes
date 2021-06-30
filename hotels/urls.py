from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotelLists, name = 'hotels'),
]