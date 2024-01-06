"""
URL configuration for mqtt_temperature_monitoring project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# mqtt_temperature_monitoring/urls.py

from django.contrib import admin
from django.urls import path, include
from publisher.views import TemperaturePublisher
from subscriber.views import TemperatureSubscriber

urlpatterns = [
    path('admin/', admin.site.urls),
    path('publish-temperature/', TemperaturePublisher.as_view(), name='publish_temperature'),
    path('get-temperature/', TemperatureSubscriber.as_view(), name='get_temperature'),
   
]
