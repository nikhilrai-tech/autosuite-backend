"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from myapp.views import BardAnswerView,BardResponseUpdateView,BardRequestCreateView,CropSeedPriceView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',BardAnswerView.as_view(), name='get_bard_answer'),
    path('api/<int:pk>/', BardResponseUpdateView.as_view(), name='update-response'),
    path('api/create', BardRequestCreateView.as_view(), name='create-bard-request'),
    # path('api/amazon',scrap.as_view(), name='bard-answer'),
    path('cropseed/price/', CropSeedPriceView.as_view(), name='cropseed-price'),
]
