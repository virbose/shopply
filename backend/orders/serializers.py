from rest_framework import serializers
from products.models import Product
from products.serializers import ProductSerializer
from orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ('url','id', 'product', 'quantity')

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('url', 'id', 'created', 'customer', 'total_price', 'items',)
        read_only_fields = ('created', 'customer', 'total_price',)

    def validate_items(self):
        items = self.context['request'].data.get('items')
        if not items:
            raise serializers.ValidationError("No products selected. Please add some products to the order.")
        return self
    
    def create(self, validated_data):
        if not 'items' in validated_data:
            raise serializers.ValidationError("No products selected. Please add some products to the order.")
        
        items_data = validated_data.pop('items')

        # Check if there are no items
        if not items_data:
            raise serializers.ValidationError("No products selected. Please add some products to the order.")

        total_price = 0
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            product_id = item_data['product']
            quantity = item_data['quantity']

            # Check if quantity is not an integer
            try:
                quantity = int(quantity)
            except ValueError:
                order.delete()
                raise serializers.ValidationError("Incorrect order format; please correct and try again")
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                order.delete()
                raise serializers.ValidationError("Incorrect order format; please correct and try again")
            # Check if there is enough stock
            if product.quantity_in_stock >= quantity:
                order_item = OrderItem.objects.create(order=order, product=product, quantity=quantity)
                total_price += order_item.product.price * order_item.quantity
                product.quantity_in_stock -= quantity
                product.save()
            else:
                # Rollback the order creation if there is not enough stock
                order.delete()
                raise serializers.ValidationError(f"Not enough stock for product {product.name}")

        # Check if there are valid items in the order
        if total_price == 0:
            order.delete()
            raise serializers.ValidationError("No valid items in the order. Please add valid products and try again.")

        order.total_price = total_price
        order.save()

        return order