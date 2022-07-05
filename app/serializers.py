from app.models import Item
from rest_framework import serializers

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        # is_completed should not be given in fields. Only what can be edited by the user should be here
        fields = ['id','title','description']
