# Serializers define the API representation.
from rest_framework import serializers

from customers.models import Customer


class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Customer
        fields = [
            'url', 
            'username', 
            'email', 
            'contact_number',
            'first_name', 
            'last_name', 
            'street_1',
            'street_2',
            'city',
            'state',
            'country',
            'is_staff', ]
