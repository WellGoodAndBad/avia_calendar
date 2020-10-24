from django.urls import path

from . import views


urlpatterns = [
    # path('news/', views.NewsListViewSet.as_view({'get': 'list'})),
    path("parse/", views.StartParser.as_view()),
    path("check/", views.StartCheck.as_view())
]