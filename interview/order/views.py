from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class OrderTagsRetrieveView(generics.RetrieveAPIView):

    def get(self, request, **kwargs):
        '''
        Get all tags for Order
        '''
        tags = Order.objects.get(id=kwargs['pk']).tags.all()
        serializer = OrderTagSerializer(tags, many=True)

        return Response(serializer.data, status=200)
