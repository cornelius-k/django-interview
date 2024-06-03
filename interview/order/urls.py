
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, DeactivateOrderView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('<int:id>/active', DeactivateOrderView.as_view(), name='activate-order'),
    path('', OrderListCreateView.as_view(), name='order-list'),
]