from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
urlpatterns = [
    path('users/', views.CustomUserList.as_view()),
    path('user/<str:username>/', views.CustomUserDetail.as_view()),
    path('change-password/', views.ChangePasswordView.as_view()),   
    path('register/', views.UserCreate.as_view()),
    # path('password_reset/', include('django_rest_passwordreset.urls'))

]
urlpatterns = format_suffix_patterns(urlpatterns)