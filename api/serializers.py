from rest_framework import serializers

from api.models import entries


class EntriesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = entries
        fields = "__all__"
        

    




        
        