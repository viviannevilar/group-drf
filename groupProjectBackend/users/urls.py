from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
urlpatterns = [
    path('users/', views.CustomUserList.as_view()),
    path('user/<str:username>/', views.CustomUserDetail.as_view()),   
    path('register/', views.UserCreate.as_view()),
    path('users/register/', views.UzerCreate.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)