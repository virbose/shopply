from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from products.models import Product
from products.serializers import ProductSerializer

class ProductPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'items_per_page'
    max_page_size = 100

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination