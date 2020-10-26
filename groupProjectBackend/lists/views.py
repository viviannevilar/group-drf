from rest_framework import generics, permissions
from .models import Collection
from .serialisers import (CollectionSerialiser)

class CollectionsList(generics.ListCreateAPIView):
    """ 
    Shows all collections that aren't archived
    url: collections/ 
    """
    queryset = Collection.objects.filter(archived=False)
    serializer_class = CollectionSerialiser

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)