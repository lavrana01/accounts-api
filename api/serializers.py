from rest_framework import serializers

from api.models import entries


class EntriesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = entries
        fields = "__all__"


class LedgerSerializer(serializers.ModelSerializer):
    Name = serializers.CharField(max_length=100, source='particulars')
    Balance = serializers.CharField(max_length=100, source='particulars')

    class Meta:
        model = entries
        fields = ['Name', 'Balance']
        

    




        
        