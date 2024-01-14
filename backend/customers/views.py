from rest_framework import viewsets, permissions
from customers.models import Customer

from customers.serializers import CustomerSerializer
# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Customer.objects.all()
        elif user.is_authenticated:
            return Customer.objects.filter(id=user.pk)
        else:
            return []
        