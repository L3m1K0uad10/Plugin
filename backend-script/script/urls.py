from django.contrib import admin
from django.urls import path, include 



urlpatterns = [
    path('admin/', admin.site.urls),
    path('input_layer/', include('input_layer.urls')),
    path('output_layer/', include('output_layer.urls'))
]
