from multiprocessing import Value
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(customer=user)

    def perform_create(self, serializer):
        items_data = self.request.data.get('items', [])
        serializer.save(customer=self.request.user, items=items_data)
