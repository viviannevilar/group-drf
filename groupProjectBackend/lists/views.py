from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsOwner
from .models import Collection, Item
from .serialisers import (
   CollectionSerialiser,
   CollectionDetailSerialiser,
   ItemSerialiser,
   )
from django.core.signing import BadSignature
from django.http import Http404


class CollectionsList(generics.ListCreateAPIView):
   """ 
   Shows all collections
   url: collections/ 
   """
   serializer_class = CollectionSerialiser
   permission_classes = [IsAuthenticated, IsOwner, ]

   def get_queryset(self):
      return Collection.objects.filter(user=self.request.user)

   def perform_create(self, serializer):
      serializer.save(user=self.request.user)

class CollectionSafe(APIView):

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


class CollectionsArchiveList(generics.ListAPIView):
   """ 
   Shows all collections that are archived
   url: collections/ 
   """
   serializer_class = CollectionSerialiser
   permission_classes = [IsAuthenticated, IsOwner, ]

   def get_queryset(self):
      return Collection.objects.filter(user=self.request.user, is_active=False)

   def perform_create(self, serializer):
      serializer.save(user=self.request.user)


class CollectionsActiveList(generics.ListAPIView):
   """ 
   Shows all collections that are active (not archived)
   url: collections/ 
   """
   serializer_class = CollectionSerialiser
   permission_classes = [IsAuthenticated, IsOwner, ]

   def get_queryset(self):
      return Collection.objects.filter(user=self.request.user, is_active=True)

   def perform_create(self, serializer):
      serializer.save(user=self.request.user)


class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
   """ 
   url: collection/<int:pk>/
   """
   queryset = Collection.objects.all()
   serializer_class = CollectionDetailSerialiser
   permission_classes = [IsOwner, IsAuthenticated, ]


class CollectionToggleArchive(APIView):
   "archive or unarchive collection"

   queryset = Collection.objects.all()
   permission_classes = [IsAuthenticated, IsOwner]

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

   def perform_create(self, serializer):
      serializer.save(user=self.request.user)


class ItemsArchiveList(generics.ListAPIView):
   """ 
   Shows all lists that are archived
   url: items/ 
   """
   serializer_class = ItemSerialiser
   permission_classes = [IsAuthenticated, IsOwner,]

   def get_queryset(self):
      return Item.objects.filter(user=self.request.user, is_active=False)

   def perform_create(self, serializer):
      serializer.save(user=self.request.user)


class ItemsList(generics.ListCreateAPIView):
   """ 
   Shows all lists
   url: items/ 
   """
   serializer_class = ItemSerialiser
   permission_classes = [IsAuthenticated, IsOwner,]

   def get_queryset(self):
      return Item.objects.filter(user=self.request.user)

   def perform_create(self, serializer):
      serializer.save(user=self.request.user)


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
   """ 
   url: item/<int:pk>/
   """
   queryset = Item.objects.all()
   serializer_class = ItemSerialiser
   permission_classes = [IsAuthenticated, IsOwner,]


class ItemToggleArchive(APIView):
   "archive or unarchive item"

   queryset = Item.objects.all()
   permission_classes = [IsAuthenticated, IsOwner]

   def get_object(self, pk):
      try:
         return Item.objects.get(pk=pk)
      except Item.DoesNotExist:
         raise Http404

   def post(self, request, pk):
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

   #serializer_class = RankingSerialiser
   permission_classes = [IsAuthenticated, IsOwner]

   def post(self, request, pk):
      collection_pk = request.data['collection_id']

      items = Item.objects.filter(collection__pk=collection_pk)
      print(f"items: {items}")
      
      array = request.data['ranking']

      # get reverse of array so that the first item is the last one updated
      # this because date modified is the default version that django lists
      # the items
      rev_array= array[::-1]
      print(f"array: {array}")
      print(f"reverse array: {rev_array}")

      for (idx, item_pk) in enumerate(rev_array):
         Item.objects.filter(pk=item_pk).update(ranking=(len(array) - 1 - idx))
      
      return Response("check")



