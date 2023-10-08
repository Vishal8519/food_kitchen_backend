from django.shortcuts import render

from django.shortcuts import render, redirect ,reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import serializers
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django import forms

from ajax_datatable.views import AjaxDatatableView
from .models import *
from django.http import JsonResponse

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('/dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a superuser.')

    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


#Api for foodkitchen

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FoodItem
from .models import FoodItem

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'

    
@api_view(['GET'])
def FoodItems(request):
    food_items = FoodItem.objects.all()
    serializers = FoodItemSerializer(food_items, many =True)
    return Response(serializers.data)

class CartItemSerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer()  # Use FoodItemSerializer for the food_item field

    class Meta:
        model = CartItem
        fields = ['id', 'food_item', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ['id', 'items']


# @csrf_exempt
# @api_view(['POST'])
# def add_to_cart(request):
#     if request.method == 'POST':
#         food_item_id = request.data.get('item_id')

#         try:
#             food_item = FoodItem.objects.get(id=food_item_id)
#         except FoodItem.DoesNotExist:
#             return Response({'error': 'Food item not found'}, status=status.HTTP_404_NOT_FOUND)

#         cart, _ = Cart.objects.get_or_create(pk=1)  # Assuming there's only one cart

#         # Create or update the cart item
#         cart_item, created = CartItem.objects.get_or_create(cart=cart, food_item=food_item)
#         if not created:
#             cart_item.quantity += 1
#             cart_item.save()

#         # Serialize the cart item with the correct serializer
#         serializer = CartItemSerializer(cart_item)
#         return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_to_cart(request):
    if request.method == 'POST':
        food_item_id = request.data.get('item_id')

        try:
            food_item = FoodItem.objects.get(id=food_item_id)
        except FoodItem.DoesNotExist:
            return Response({'error': 'Food item not found'}, status=status.HTTP_404_NOT_FOUND)

        # Assuming there's only one cart
        cart, created = ShoppingCart.objects.get_or_create(pk=1)

        # Create a new cart item for the food item
        cart_item = CartItem.objects.create(cart=cart, food_item=food_item)

        # Serialize the cart item with the correct serializer
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# @csrf_exempt
# @api_view(['POST'])
# def remove_from_cart(request):
#     if request.method == 'POST':
#         food_item_id = request.data.get('item_id')

#         try:
#             food_item = FoodItem.objects.get(id=food_item_id)
#         except FoodItem.DoesNotExist:
#             return Response({'error': 'Food item not found'}, status=status.HTTP_404_NOT_FOUND)

#         cart, _ = Cart.objects.get_or_create(pk=1)  # Assuming there's only one cart

#         try:
#             cart_item = CartItem.objects.get(cart=cart, food_item=food_item)
#         except CartItem.DoesNotExist:
#             return Response({'error': 'Food item not in cart'}, status=status.HTTP_404_NOT_FOUND)

#         if cart_item.quantity > 1:
#             cart_item.quantity -= 1
#             cart_item.save()
#         else:
#             cart_item.delete()

#         # Serialize the cart item with the correct serializer
#         serializer = CartItemSerializer(cart_item)
#         return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def remove_from_cart(request):
    if request.method == 'POST':
        food_item_id = request.data.get('item_id')

        try:
            food_item = FoodItem.objects.get(id=food_item_id)
        except FoodItem.DoesNotExist:
            return Response({'error': 'Food item not found'}, status=status.HTTP_404_NOT_FOUND)

        # Assuming there's only one cart
        cart, _ = ShoppingCart.objects.get_or_create(pk=1)

        try:
            # Try to get the cart item for the specified food item
            cart_item = CartItem.objects.filter(cart=cart, food_item=food_item).first()

            if cart_item:
                # If the cart item exists, delete it
                cart_item.delete()
                return Response({'message': 'Food item removed from cart'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Food item not in cart'}, status=status.HTTP_404_NOT_FOUND)

        except CartItem.DoesNotExist:
            return Response({'error': 'Food item not in cart'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def cart_list(request):
    try:
        cart = ShoppingCart.objects.get(pk=1)  # Assuming there's only one cart
    except ShoppingCart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the cart and its items
    cart_serializer = CartSerializer(cart)
    cart_data = cart_serializer.data

    # Get cart items for the cart and serialize them
    cart_items = cart.cartitem_set.all()
    cart_item_serializer = CartItemSerializer(cart_items, many=True)

    # Add the serialized cart items to the cart data
    cart_data['items'] = cart_item_serializer.data

    return Response(cart_data)


def cart_count(request):
    try:
        # Assuming there's only one cart for simplicity
        cart = ShoppingCart.objects.get(pk=1)
        cart_count = cart.cartitem_set.count()  # Count the cart items
        return JsonResponse({'cart_count': cart_count})
    except ShoppingCart.DoesNotExist:
        return JsonResponse({'cart_count': 0})
    
# DASH BOARD
class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'image', 'price', 'is_available']
        widgets = {
            'image': forms.ClearableFileInput(),
        }

def food_item_add_edit_view(request, food_item_id=None):
    # If food_item_id is provided, edit an existing FoodItem
    if food_item_id:
        food_item = FoodItem.objects.get(id=food_item_id)
        form = FoodItemForm(request.POST or None, request.FILES or None, instance=food_item)
    else:
        form = FoodItemForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            food_item = form.save(commit=False)
            # Customize any additional fields if needed
            # food_item.custom_field = custom_value
            food_item.save()
            return redirect('food_items_list')  # Redirect to the list view for food items

    return render(request, 'food_item_add_edit.html', {'form': form})


@csrf_exempt
def add_food_item(request):
    if request.method == 'POST':
        # Get data from the AJAX request
        name = request.POST.get('name')
        price = request.POST.get('price')
        is_available = request.POST.get('is_available') == 'true'

        # Save the new food item to the database
        food_item = FoodItem.objects.create(name=name, price=price, is_available=is_available)

        # Return a JSON response indicating success
        return JsonResponse({'success': True, 'message': 'Food item added successfully.'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})

from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers

def food_items_list(request):
    # Get the list of food items
    food_items = FoodItem.objects.all()

    return render(request, 'fooditemlist.html', {'form': food_items})
from django.template.loader import render_to_string

def load_content(request, menu_id):
    # Depending on the menu_id, fetch the appropriate data
    # Example: Fetch food items for "all_food_items" menu
    if menu_id == 'all_food_items':
        food_items = FoodItem.objects.all()
        html_content = render_to_string('fooditemlist.html', {'food_items': food_items})

    elif menu_id == 'add_food_item':
        if request.method == 'POST':
            # If a POST request, process the form data
            form = FoodItemForm(request.POST, request.FILES)
            if form.is_valid():
                # Create a new food item from the form data
                new_food_item = form.save(commit=False)
                new_food_item.save()
                html_content = 'Food item added successfully.'
            else:
                html_content = render_to_string('add_food_item_form.html', {'form': form})
        else:
            # If a GET request, render the empty form
            form = FoodItemForm()
            html_content = render_to_string('add_food_item_form.html', {'form': form})
    else:
        html_content = ''  # Handle other menu IDs accordingly

    return JsonResponse({'html_content': html_content})




