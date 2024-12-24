from django.urls import path

from .views import InputView



urlpatterns = [
    path('input/create/', InputView, name = "input_create"),
    path('input/', InputView, name = "input_list"),
    path('input/<int:pk>/', InputView, name = "input_detail"),
    path('input/<int:pk>/<slug:slug>/', InputView, name = "input_operations"), # split data into line datas, find comments ...etc
]