from rest_framework import serializers
from Document.models import Document


class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= Document
        fields = ('id','numb','user','Nombre')






