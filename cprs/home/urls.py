from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('accounts/login', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('details/<str:asin>', views.DetailsView.as_view(), name='details'),
    path('details/<str:asin>/comment/create', views.CommentCreateView.as_view(), name='comment_create'),
    path('details/<str:asin>/comment/delete', views.CommentDeleteView.as_view(), name='comment_delete'),
]
