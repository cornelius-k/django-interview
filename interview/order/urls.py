
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, OrderTagsRetrieveView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('<int:pk>/tags/', OrderTagsRetrieveView.as_view(), name="order-tags"),
    path('', OrderListCreateView.as_view(), name='order-list'),

]