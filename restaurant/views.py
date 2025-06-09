from decimal import Decimal
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from django.db import transaction
from rest_framework.response import Response
from restaurant.models import Category, MenuItem, Order, OrderItem, Table
from restaurant.serializers import CategorySerializer, CreateOrderSerializer, OrderSerializer, TableSerializer

# Create your views here.

class MenuView(generics.ListAPIView):
    """GET MENU WITH ALL CATEGORIES AND ITMES"""
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_active= True)
    #mathi ko lew is_active jun row xa Category model True vako lai matrew return garxa

class TableDetailView(generics.RetrieveAPIView):
    """GET TABLE DETAILS BY QR CODE"""
    serializer_class = TableSerializer
    lookup_field = 'qr_code'
    queryset= Table.objects.all()

@api_view(['POST'])
def create_order(request):
    """create a new order"""
    serializer = CreateOrderSerializer(data=request.data)
    if serializer.is_valid():
        validated_data= serializer.validated_data

        try:
            with transaction.atomic():
                # Get table by QR code
                table = get_object_or_404(Table, qr_code=validated_data['table_qr_code'])
                
                # Create order
                order = Order.objects.create(
                    table=table,
                    customer_name=validated_data.get('customer_name', ''),
                    notes=validated_data.get('notes', '')
                )
                
                total_amount = Decimal('0.00')
                
                # Create order items
                for item_data in validated_data['items']:
                    menu_item = get_object_or_404(MenuItem, id=item_data['menu_item_id'])
                    quantity = int(item_data['quantity'])
                    
                    if not menu_item.is_available:
                        return Response(
                            {'error': f'{menu_item.name} is currently unavailable'}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    order_item = OrderItem.objects.create(
                        order=order,
                        menu_item=menu_item,
                        quantity=quantity,
                        price=menu_item.price,
                        special_instructions=item_data.get('special_instructions', '')
                    )
                    
                    total_amount += order_item.subtotal
                
                # Update order total
                order.total_amount = total_amount
                order.save()
                
                # Mark table as occupied
                table.is_occupied = True
                table.save()
                
                return Response(
                    OrderSerializer(order).data, 
                    status=status.HTTP_201_CREATED
                )
                
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def order_status(request, order_id):
    """Get order status"""
    order = get_object_or_404(Order, order_id=order_id)
    return Response(OrderSerializer(order).data)

@api_view(['POST'])
def update_order_status(request, order_id):
    """Update order status (for restaurant staff)"""
    order = get_object_or_404(Order, order_id=order_id)
    new_status = request.data.get('status')
    
    if new_status in dict(Order.ORDER_STATUS):
        order.status = new_status
        order.save()
        
        # Free table when order is served or cancelled
        if new_status in ['served', 'cancelled']:
            order.table.is_occupied = False
            order.table.save()
        
        return Response(OrderSerializer(order).data)
    
    return Response(
        {'error': 'Invalid status'}, 
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
def restaurant_orders(request):
    """Get all orders for restaurant staff"""
    orders = Order.objects.all().order_by('-created_at')
    return Response(OrderSerializer(orders, many=True).data)
       
