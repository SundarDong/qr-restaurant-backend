from rest_framework import serializers

from restaurant.models import Category, MenuItem, Order, OrderItem, Table

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'image', 'is_vegetarian', 
                 'is_vegan', 'is_available', 'preparation_time', 'rating']
        
class CategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only= True)
    #Yesma category ko serializer lida menuitems ko detials ni erne
    class Meta:
        model = Category
        fields = ['id', 'name', 'display_name', 'description', 'items']

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'table_number', 'qr_code', 'capacity', 'is_occupied']

class OrderItemSerializer(serializers.ModelSeriazlizer):
    menu_items_name = serializers.CharField(source='menu_items.name',read_only=True)
    subtotal= serializers.ReadOnlyField()
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'quantity', 'price', 
                 'special_instructions', 'subtotal']
        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    table_number = serializers.CharField(source='table.table_number', read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'order_id', 'table', 'table_number', 'customer_name', 
                 'status', 'total_amount', 'notes', 'items', 'created_at']
        read_only_fields = ['order_id', 'total_amount']

class CreateOrderSerializer(serializers.Serializer):
    table_qr_code = serializers.CharField()
    customer_name = serializers.CharField(max_length=100, required=False)
    notes = serializers.CharField(required=False)
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must contain at least one item")
        
        for item in value:
            if 'menu_item_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError("Each item must have menu_item_id and quantity")
        
        return value
