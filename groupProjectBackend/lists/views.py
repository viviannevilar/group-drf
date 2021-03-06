from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsOwner, HasOwnerPermissionOrIsOwner, IsOwnerCollectionOrHasPermission
from .models import Collection, Item
from .serialisers import (
  CollectionSerialiser,
  CollectionDetailSerialiser,
  CollectionSimpleDetailSerialiser,
  ItemSerialiser,
  CollectionSharedSerialiser
  )
from django.core.signing import BadSignature
from django.http import Http404
from django.contrib.auth import get_user_model

User = get_user_model()

#################### Collections ####################

class CollectionsList(generics.ListCreateAPIView):
  """ 
  Shows all collections
  url: collections/ 
  """
  serializer_class = CollectionSerialiser
  permission_classes = [IsAuthenticated, HasOwnerPermissionOrIsOwner, ]

  def get_queryset(self):
    my_queryset = Collection.objects.filter(user=self.request.user) | Collection.objects.filter(allowed_users__in = [self.request.user.id])
    return my_queryset.distinct()

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)


class CollectionsArchiveList(generics.ListAPIView):
  """ 
  Shows all collections that are archived
  url: archived-collections/ 
  """
  serializer_class = CollectionSerialiser
  permission_classes = [IsAuthenticated, HasOwnerPermissionOrIsOwner, ]

  def get_queryset(self):
    my_queryset = Collection.objects.filter(user=self.request.user, is_active=False) | Collection.objects.filter(allowed_users__in = [self.request.user.id], is_active=False)
    return my_queryset.distinct()

  #  def get_queryset(self):
  #     return Collection.objects.filter(user=self.request.user, is_active=False)


class CollectionsActiveList(generics.ListAPIView):
  """ 
  Shows all collections that are active (not archived)
  url: active-collections/ 
  """
  serializer_class = CollectionSerialiser
  permission_classes = [IsAuthenticated, HasOwnerPermissionOrIsOwner, ]

  def get_queryset(self):
    my_queryset = Collection.objects.filter(user=self.request.user, is_active=True) | Collection.objects.filter(allowed_users__in = [self.request.user.id], is_active=True)
    return my_queryset.distinct()

  # def get_queryset(self):
  #   return Collection.objects.filter(user=self.request.user, is_active=True)


class CollectionSafe(APIView):
  ''' 
  view someone else's collection that they shared with a link 
  uses CollectionDetailSerialiser 
  url: collection/safe/<signed_pk>/
  '''
  def get_object(self, signed_pk):
    try:
      pk = Collection.signer.unsign(signed_pk)
      return Collection.objects.get(pk=pk)
    except (BadSignature, Collection.DoesNotExist):
      raise Http404('No collection matches the given query')
  
  def get(self, request, signed_pk):
    collection = self.get_object(signed_pk)
    serializer = CollectionDetailSerialiser(collection)
    return Response(serializer.data)  


class CollectionSharedUsers(generics.RetrieveAPIView):
  '''
  to see users that are allowed
  url: collection/<int:pk>/allowed_users/
  '''
  queryset = Collection.objects.all()
  serializer_class = CollectionSharedSerialiser
  permission_classes = [IsAuthenticated, IsOwner, ]


class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
  """ 
  url: collection/<int:pk>/
  """
  queryset = Collection.objects.all()
  serializer_class = CollectionDetailSerialiser
  permission_classes = [IsAuthenticated, HasOwnerPermissionOrIsOwner,  ]


class CollectionSimpleDetail(generics.RetrieveAPIView):
  """ 
  url: collection/simple/<int:pk>/
  """
  queryset = Collection.objects.all()
  serializer_class = CollectionSimpleDetailSerialiser
  permission_classes = [IsAuthenticated, HasOwnerPermissionOrIsOwner, ]


class CollectionToggleArchive(APIView):
  """
  archive or unarchive collection
  """
  queryset = Collection.objects.all()
  permission_classes = [IsAuthenticated, HasOwnerPermissionOrIsOwner,]

  def get_object(self, pk):
    try:
      return Collection.objects.get(pk=pk)
    except Collection.DoesNotExist:
      raise Http404

  def post(self, request, pk):
    collection = self.get_object(pk)
    self.check_object_permissions(request, collection)        
    data = request.data
    if collection.is_active == True:
      collection.is_active = False
      response = "collection unarchived!"
    else:
      collection.is_active = True
      response = "collection archived"
    collection.save()
    return Response({'status': response})


class ItemsActiveList(generics.ListAPIView):
  """ 
  Shows all lists that are active (not archived)
  url: items/ 
  """
  serializer_class = ItemSerialiser
  permission_classes = [IsAuthenticated, IsOwner,]

  def get_queryset(self):
    return Item.objects.filter(user=self.request.user, is_active=True)


class ItemsArchiveList(generics.ListAPIView):
  """ 
  Shows all lists that are archived
  url: items/ 
  """
  serializer_class = ItemSerialiser
  permission_classes = [IsAuthenticated, IsOwner,]

  def get_queryset(self):
    return Item.objects.filter(user=self.request.user, is_active=False)


class ItemToggleArchive(APIView):
  '''
  archive or unarchive item
  '''
  queryset = Item.objects.all()
  permission_classes = [IsAuthenticated, IsOwnerCollectionOrHasPermission, ]

  def get_object(self, pk, **kwargs):
    try:
      return Item.objects.get(pk=pk)
    except Item.DoesNotExist:
      raise Http404

  def post(self, request, pk, **kwargs):
    item = self.get_object(pk)
    self.check_object_permissions(request, item)  
    data = request.data
    if item.is_active == True:
      item.is_active = False
      response = "item archived!"
    else:
      item.is_active = True
      response = "item unarchived"
    item.save()
    return Response({'status': response})


class CollectionRankingView(APIView):
  """
  shows the custom ranking of items in a collection
  """
  permission_classes = [IsAuthenticated, HasOwnerPermissionOrIsOwner,]

  def post(self, request, pk):
    collection_pk = request.data['collection_id']
    items = Item.objects.filter(collection__pk=collection_pk)
    print(f"items: {items}")
    
    # get reverse of array so that the first item is the last one updated
    # this because date modified is the default version that django lists
    # the items
    array = request.data['ranking']
    rev_array= array[::-1]

    for (idx, item_pk) in enumerate(rev_array):
      Item.objects.filter(pk=item_pk).update(ranking=(len(array) - 1 - idx))
    
    return Response({'statusText': "Order saved!", 'ok': True})


class CollectionShare(APIView):
  """
  give another user permission to edit collection
  url: collection/<int:pk>/add_user/
  """
  queryset = Collection.objects.all()
  permission_classes = [IsAuthenticated, IsOwner, ]

  def get_object(self, pk):
    try:
      return Collection.objects.get(pk=pk)
    except Collection.DoesNotExist:
      raise Http404

  def post(self, request, pk):
    collection = self.get_object(pk)
    self.check_object_permissions(request, collection)  
    username = request.data['username']
    # print(f"username: {username}")

    try:
      user = User.objects.get(username=username)
      # print(f"user: ", {user.id})
      # print(collection.allowed_users.filter(id=user.id).exists() == True)
      if collection.allowed_users.filter(id=user.id).exists() == True:
        response = f"you have already shared this collection with {username}!"
      else:
        collection.allowed_users.add(user)
        response = f"user {username} can now edit this collection!"
        collection.save()
    except:
      response = "this username is invalid!"
    
    return Response({'status': response})


class CollectionUnshare(APIView):
  """
  remove another user's permission to edit collection
  url: collection/<int:pk>/remove_user/
  """
  queryset = Collection.objects.all()
  permission_classes = [IsAuthenticated, IsOwner, ]

  def get_object(self, pk):
    try:
      return Collection.objects.get(pk=pk)
    except Collection.DoesNotExist:
      raise Http404

  def post(self, request, pk):
    collection = self.get_object(pk)
    self.check_object_permissions(request, collection)  
    username = request.data['username']
    # print(f"username: {username}")

    try:
      user = User.objects.get(username=username)
      # print(f"user: ", {user.id})
      # print(collection.allowed_users.filter(id=user.id).exists() == True)
      if collection.allowed_users.filter(id=user.id).exists() == True:
        collection.allowed_users.remove(user)
        response = f"user {username} no longer has permission to edit this collection!"
        collection.save()
      else:
       response = f"User {username} can't be removed as they currently don't have permission!"
    except:
      response = "this username is invalid!"
    
    return Response({'status': response})


############################################
class CollectionItemsCreate(generics.ListCreateAPIView):
  """ 
  Create items in a collection; needs to be collection owner or have owner's permission
  url: collection/<int:collection>/items/ 
  """
  serializer_class = ItemSerialiser
  permission_classes = [IsAuthenticated, IsOwnerCollectionOrHasPermission, ]

  def get_queryset(self):
    return Item.objects.filter(collection=self.kwargs['collection'])

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)


class ItemCollectionDetail(generics.RetrieveUpdateDestroyAPIView):
  """ 
  url: item/<int:collection>/<int:pk>/
  """
  queryset = Item.objects.all()
  serializer_class = ItemSerialiser
  permission_classes = [IsAuthenticated, IsOwnerCollectionOrHasPermission,]




# those are old views which didn't have good permissions. 
# replaced by the onesx above
# ItemsList replaced by CollectionItemsCreate
# ItemDetail replaced by ItemCollectionDetail

# class ItemsList(generics.ListCreateAPIView):
#    """ 
#    Shows all lists
#    url: items/ 
#    """
#    serializer_class = ItemSerialiser
#    permission_classes = [IsAuthenticated, IsOwner,]

#    def get_queryset(self):
#       return Item.objects.filter(user=self.request.user)

#    def perform_create(self, serializer):
#       serializer.save(user=self.request.user)


# class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
#    """ 
#    url: item/<int:pk>/
#    """
#    queryset = Item.objects.all()
#    serializer_class = ItemSerialiser
#    permission_classes = [IsAuthenticated, IsOwner,]