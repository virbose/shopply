from django.db import IntegrityError
from django.urls import reverse
import pytest
from django.contrib.auth import get_user_model
from products.models import Product
from orders.models import Order, OrderItem
from rest_framework import status
from rest_framework.test import APIClient

Customer = get_user_model()

@pytest.mark.django_db
def test_order_creation():
    customer = Customer.objects.create(username="test_user")
    order = Order.objects.create(customer=customer, total_price=50.0)
    assert order.customer == customer
    assert order.total_price == 50.0

@pytest.mark.django_db
def test_order_creation_no_total():
    customer = Customer.objects.create(username="test_user")
    order = Order.objects.create(customer=customer)
    assert order.customer == customer
    assert order.total_price == 0.0

@pytest.mark.django_db
def test_order_creation_no_customer():
    with pytest.raises(IntegrityError):
        Order.objects.create()

@pytest.mark.django_db
def test_order_item_creation():
    customer = Customer.objects.create(username="test_user")
    product = Product.objects.create(name="Test Product", description="Description", price=10.0, quantity_in_stock=100)
    order = Order.objects.create(customer=customer, total_price=20.0)
    order_item = OrderItem.objects.create(order=order, product=product, quantity=2)
    assert order_item.order == order
    assert order_item.product == product
    assert order_item.quantity == 2

@pytest.mark.django_db
def test_create_order_via_endpoint():
    client = APIClient()
    user = Customer.objects.create(username="test_user")
    product = Product.objects.create(name="Test Product", description="Description", price=10.0, quantity_in_stock=100)
    client.force_authenticate(user=user)
    
    data = {'items': [{'product': product.id, 'quantity': 2}]}
    response = client.post(reverse('order-list'), data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Order.objects.count() == 1
    assert OrderItem.objects.count() == 1
    
@pytest.mark.django_db
def test_create_order_via_endpoint_unauthenticated():
    client = APIClient()

    product = Product.objects.create(name="Test Product", description="Description", price=10.0, quantity_in_stock=100)
    
    data = {'items': [{'product': product.id, 'quantity': 2}]}
    response = client.post(reverse('order-list'), data, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_create_no_items_order_via_endpoint():
    client = APIClient()
    user = Customer.objects.create(username="test_user")
    client.force_authenticate(user=user)

    response = client.post(reverse('order-list'), {'items': []}, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert str(response.data[0]) == "No products selected. Please add some products to the order."

@pytest.mark.django_db
def test_create_empty_order_via_endpoint():
    client = APIClient()
    user = Customer.objects.create(username="test_user")
    client.force_authenticate(user=user)

    response = client.post(reverse('order-list'), {}, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert str(response.data[0]) == "No products selected. Please add some products to the order."

@pytest.mark.django_db
def test_create_order_via_endpoint_bad_qty():
    client = APIClient()
    user = Customer.objects.create(username="test_user")
    product = Product.objects.create(name="Test Product", description="Description", price=10.0, quantity_in_stock=10)
    client.force_authenticate(user=user)
    
    data = {'items': [{'product': product.id, 'quantity': 'bad_qty'}]}
    response = client.post(reverse('order-list'), data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert str(response.data[0]) == "Incorrect order format; please correct and try again"

@pytest.mark.django_db
def test_create_order_via_endpoint_not_enough_stock():
    client = APIClient()
    user = Customer.objects.create(username="test_user")
    product = Product.objects.create(name="Test Product", description="Description", price=10.0, quantity_in_stock=10)
    client.force_authenticate(user=user)
    
    data = {'items': [{'product': product.id, 'quantity': 20}]}
    response = client.post(reverse('order-list'), data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert str(response.data[0]) == f"Not enough stock for product {product.name}"


@pytest.mark.django_db
def test_retrieve_order_via_endpoint():
    user = Customer.objects.create(username="test_user")
    product = Product.objects.create(name="Test Product", description="Description", price=10.0, quantity_in_stock=100)
    
    order = Order.objects.create(customer=user, total_price=20.0)
    oi = OrderItem.objects.create(order=order, product=product, quantity=2)
    
    client = APIClient()
    client.force_authenticate(user=user)
    
    response = client.get(reverse('order-detail', kwargs={'pk': order.id}))
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['total_price'] == '20.00'
    assert response.data['items'][0] == oi.pk