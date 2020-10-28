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

class CollectionsList(generics.ListCreateAPIView):
    """ 
    Shows all collections that aren't archived
    url: collections/ 
    """
    serializer_class = CollectionSerialiser
    permission_classes = [IsAuthenticated, IsOwner, ]

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CollectionsArchiveList(generics.ListAPIView):
    """ 
    Shows all collections that aren't archived
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
    Shows all collections that aren't archived
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
    Shows all lists that aren't archived
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
    Shows all lists that aren't archived
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
    Shows all lists that aren't archived
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
