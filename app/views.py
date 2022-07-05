from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.serializers import ItemSerializer
from app.models import Item
import json


@api_view(['GET', 'POST','PUT','DELETE'])
def item_view(request, item_id=None):
    # item created below in try block is not accessible outside. So create here and change below
    item = None
    if request.method != 'POST':
        if item_id!=None:
            try:
                item = Item.objects.get(id=int(item_id))
            except Item.DoesNotExist:
                    return Response(status=404)
        # GET method doesn't require item_id
        elif request.method != 'GET':
            return Response(status=404)

    if request.method == 'GET':
        if not item:
            items = Item.objects.all()
            data = ItemSerializer(items, many=True).data
        else:
            data = ItemSerializer(item).data
        return Response({"data":data})
            
    
    elif request.method == 'POST':
        # even if you pass 'id' from front-end, it is ignored by DRF during deserialization (if you didn't pass Item instance as 1st argument). So safe
        item_serializer = ItemSerializer(data = json.loads(request.body.decode('utf-8')))
        if item_serializer.is_valid():
            item = item_serializer.save()
            serializer = ItemSerializer(item)
            data = serializer.data
            return Response({"data":data},status=201)
        return Response({"message":item_serializer.errors},status=400)
    
    elif request.method == 'PUT':
        # since we're passing both item (instance of Item model) and data, data will be loaded into item and returned.Thus by calling serializer.save(), we update the existing instance (PUTing)
        serializer = ItemSerializer(item, data = json.loads(request.body.decode('utf-8')))
        if serializer.is_valid():
            item = serializer.save()
            serializer = ItemSerializer(item)
            data = serializer.data
            return Response({"data":data})
        return Response({"message":serializer.errors},status=404)
    
    elif request.method == 'DELETE':
        item = Item.objects.get(id=int(item_id))
        item.delete()
        return Response(status=204)
