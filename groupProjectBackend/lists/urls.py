from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    re_path(r'collection/safe/(?P<signed_pk>[0-9]+/[A-Za-z0-9_=-]+)/$', views.CollectionSafe.as_view()),
    path('collections/', views.CollectionsList.as_view()),
    path('archived-collections/', views.CollectionsArchiveList.as_view()),
    path('active-collections/', views.CollectionsActiveList.as_view()),    
    path('collection/<int:pk>/', views.CollectionDetail.as_view()),
    path('collection/simple/<int:pk>/', views.CollectionSimpleDetail.as_view()),
    path('collection/<int:pk>/archive/', views.CollectionToggleArchive.as_view()),
    # path('items/', views.ItemsList.as_view()),
    path('item/<int:collection>/<int:pk>/', views.ItemCollectionDetail.as_view()),
    path('active-items/', views.ItemsActiveList.as_view()),
    path('archived-items/', views.ItemsArchiveList.as_view()),
    # path('item/<int:pk>/', views.ItemDetail.as_view()),
    path('item/<int:collection>/<int:pk>/archive/', views.ItemToggleArchive.as_view()),
    path('collection/<int:pk>/ranking/', views.CollectionRankingView.as_view()),
    path('collection/<int:pk>/add_user/', views.CollectionShare.as_view()),
    path('collection/<int:pk>/remove_user/', views.CollectionUnshare.as_view()),
    path('collection/<int:collection>/items/', views.CollectionItemsCreate.as_view()),
    path('collection/<int:pk>/allowed_users/', views.CollectionSharedUsers.as_view()),
    #path('collection/<int:pk>/sort/', views.CollectionSort.as_view())

]
