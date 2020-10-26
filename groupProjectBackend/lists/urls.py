from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('collections/', views.CollectionsList.as_view()),
    path('collection/<int:pk>/', views.CollectionDetail.as_view()),
    path('collection/<int:pk>/archive/', views.CollectionToggleArchive.as_view()),
    path('items/', views.ItemsList.as_view()),
    path('item/<int:pk>/', views.ItemDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)