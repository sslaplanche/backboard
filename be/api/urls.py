from django.urls import path
from . import views

urlpatterns = [
     # Endpoints
    path('test/', views.Test.as_view(), name='test'),
    path('MyFantasyRoster/', views.MyFantasyRoster.as_view(), name='MyFantasyRoster'),
]