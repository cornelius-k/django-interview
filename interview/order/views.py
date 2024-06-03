from django.shortcuts import render
from rest_framework import generics
from django.utils.dateparse import parse_datetime
from rest_framework.response import Response
from rest_framework.request import Request

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=200)
    
    def get_queryset(self):
        queryset = Order.objects.all()
        start_date = parse_datetime(self.request.query_params.get('start_date'))
        embargo_date = parse_datetime(self.request.query_params.get('embargo_date'))
        if start_date and embargo_date:
            queryset = queryset.filter(start_date__gte=start_date, embargo_date__lte=embargo_date)

        return queryset
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer
