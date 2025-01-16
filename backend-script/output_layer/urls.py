from django.urls import path 

from .views import OutputView 


urlpatterns = [
    path("output/create/", OutputView, name = "output_create"), # storing
    path("output/<int:pk>/", OutputView, name = "output_detail"), # retrieving details
    path("output/<int:pk>/<slug:slug>/", OutputView, name = "output_operations"), # translate
]