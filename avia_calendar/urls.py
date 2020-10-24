from django.urls import path

from . import views


urlpatterns = [
    path('', views.CaledarPageView.as_view(), name='calendar_page'),

]