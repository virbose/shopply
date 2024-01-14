import pytest

from products.models import Product
from products.serializers import ProductSerializer

@pytest.mark.django_db
def test_product_creation():
    product = Product.objects.create(name="Test Product", description="Description", price=10.0, quantity_in_stock=100)
    assert product.name == "Test Product"
    assert product.description == "Description"
    assert product.price == 10.0
    assert product.quantity_in_stock == 100

@pytest.mark.django_db
def test_product_serializer():
    product_data = {'name': 'Test Product', 'description': 'Description', 'price': 10.0, 'quantity_in_stock': 100}
    serializer = ProductSerializer(data=product_data)
    assert serializer.is_valid()
    product = serializer.save()
    assert product.name == 'Test Product'