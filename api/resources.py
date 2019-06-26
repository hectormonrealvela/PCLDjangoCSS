from rest_framework import viewsets
from Document.models import Document
from .serializers import ListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters

class test(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = ListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    __basic_fields = ('numb','user','Nombre')
    search_fields = __basic_fields


    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)





    