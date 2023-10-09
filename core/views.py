from django.shortcuts import render

from django.shortcuts import render, redirect ,reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import serializers
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

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

class FoodItemAPIView(APIView):
    def get(self, request):
        food_items = FoodItem.objects.all()
        serializer = FoodItemSerializer(food_items, many=True)
        return Response(serializer.data)
    

# def food_items_list(request):
#     context = {
#         "url": reverse('ajax_datatable_food_items_list'),  # Update the URL to match your URL configuration
#         "title": "Food Items",
#         "add_hx_button": [{"url": reverse('add_food_items'), "text": "Add Food Item"}],
#     }
#     return render(request, 'render_ajax_datatable.html', context)



# class FoodItemDatatableView(AjaxDatatableView):

#     model = FoodItem
#     title = "Food Items"
#     length_menu = [[10, 20, 30, 50], [10, 20, 30, 50]]
#     search_values_separator = '+'
#     column_defs = [
#         {'name': 'id', 'title': 'ID', 'visible': True, 'orderable': True},
#         {'name': 'name', 'title': 'Name', 'visible': True, 'orderable': True},
#         {'name': 'price', 'title': 'Price', 'visible': True, 'orderable': True},
#         {'name': 'is_available', 'title': 'Available', 'visible': True, 'orderable': True},
#         {'name': 'action', 'visible': True, 'placeholder': True, 'orderable': False, 'searchable': False},
#     ]

#     def customize_row(self, row, obj):
#         row['action'] = '''
#             <td class="text-end">
#                 <a href="#" class="btn btn-light btn-active-light-primary btn-sm" data-kt-menu-trigger="click" data-kt-menu-placement="bottom-end">Actions
#                 <span class="svg-icon svg-icon-5 m-0">
#                     <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
#                         <path d="M11.4343 12.7344L7.25 8.55005C6.83579 8.13583 6.16421 8.13584 5.75 8.55005C5.33579 8.96426 5.33579 9.63583 5.75 10.05L11.2929 15.5929C11.6834 15.9835 12.3166 15.9835 12.7071 15.5929L18.25 10.05C18.6642 9.63584 18.6642 8.96426 18.25 8.55005C17.8358 8.13584 17.1642 8.13584 16.75 8.55005L12.5657 12.7344C12.2533 13.0468 11.7467 13.0468 11.4343 12.7344Z" fill="currentColor"></path>
#                     </svg>
#                 </span>
#                 </a>
#                 <div class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-125px py-4" data-kt-menu="true" style="">
#                     <div class="menu-item px-3">
#                         <a href="%s" class="menu-link px-3">Edit</a>
#                     </div>
#                 </div>
#             </td>
#         ''' % reverse('food_item_edit', args=(obj.id,))

#     def get_initial_queryset(self, request, *args, **kwargs):
#         return self.model.objects.all()

from django import forms

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
        image = request.FILES.get('image')
        is_available = request.POST.get('is_available') == 'true'

        # Save the new food item to the database
        food_item = FoodItem.objects.create(name=name, price=price, is_available=is_available, image= image)
        food_item.save()

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


