from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('sign-in', views.SignInView.as_view()),
    path('details', views.DetailsView.as_view()),
]
