from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('sign-in', views.SignInView.as_view()),
    path('details/<str:asin>', views.DetailsView.as_view(), name='details'),
]
