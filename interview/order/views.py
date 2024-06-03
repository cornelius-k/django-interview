from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class DeactivateOrderView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def patch(self, request: Request, *args, **kwargs) -> Response:
        order = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(order, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()

        return Response(serializer.data, status=200)
    
    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)
        