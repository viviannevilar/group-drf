from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Collection
from .serialisers import (
    CollectionSerialiser,
    CollectionDetailSerialiser,
                        )

class CollectionsList(generics.ListCreateAPIView):
    """ 
    Shows all collections that aren't archived
    url: collections/ 
    """
    queryset = Collection.objects.filter(archived=False)
    serializer_class = CollectionSerialiser

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    """ 
    url: collection/<int:pk>/
    """
    queryset = Collection.objects.all()
    serializer_class = CollectionDetailSerialiser


class CollectionToggleArchive(APIView):
    "archive or unarchive collection"

    queryset = Collection.objects.all()

    def get_object(self, pk):
        try:
            return Collection.objects.get(pk=pk)
        except Collection .DoesNotExist:
            raise Http404

    def post(self, request, pk):
        collection = self.get_object(pk)
        self.check_object_permissions(request, collection)        
        data = request.data
        if collection.archived == True:
            collection.archived = False
            response = "collection unarchived!"
        else:
            collection.archived = True
            response = "collection archived"
        collection.save()
        return Response({'status': response})