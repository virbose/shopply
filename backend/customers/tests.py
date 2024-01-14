# customers/tests/test_customers.py
from django.test import RequestFactory
import pytest
from rest_framework.test import APIClient
from customers.models import Customer
from customers.serializers import CustomerSerializer

@pytest.mark.django_db
def test_create_customer():
    customer = Customer.objects.create(username='testuser', email='testuser@example.com')
    assert customer.username == 'testuser'
    assert customer.email == 'testuser@example.com'
    assert customer.contact_number is None  # Assuming null=True in the model field

@pytest.mark.django_db
def test_customer_view_set():
    client = APIClient()

    # Create a customer and a shop admin
    admin =  Customer.objects.create(username='testadmin', email='testadmin@example.com', is_staff=True)
    customer = Customer.objects.create(username='testuser', email='testuser@example.com')

    # List no customers as unauthenticated
    response = client.get('/api/customers/')
    assert response.status_code == 200
    assert len(response.data) == 0


    client.force_authenticate(admin)
    # List all customers as admin
    response = client.get('/api/customers/')
    assert response.status_code == 200
    assert len(response.data) == 2
    # Logout admin
    client.force_authenticate(user=None)

    client.force_authenticate(customer)
    # List all customers as admin
    response = client.get('/api/customers/')
    assert response.status_code == 200
    assert len(response.data) == 1

    # Retrieve own customer data
    response = client.get(f'/api/customers/{customer.id}/')
    assert response.status_code == 200
    assert response.data['username'] == 'testuser'

    client.force_authenticate(user=None)
    # Attempt to create a customer without authentication
    response = client.post('/api/customers/', {'username': 'newuser', 'email': 'newuser@example.com'})
    assert response.status_code == 201  # Should succeed

    

@pytest.mark.django_db
def test_customer_serializer():
    customer = Customer.objects.create(username='testuser', email='testuser@example.com')

    request = RequestFactory().get('/api/customers/')

    serializer = CustomerSerializer(instance=customer, context={'request': request})
    assert serializer.data['username'] == 'testuser'
    assert serializer.data['email'] == 'testuser@example.com'
    assert 'contact_number' in serializer.data  # Assuming the contact_number field is included