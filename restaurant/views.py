##restaurant/views.py
## description: write view functions to handle URL requests for restaurant app
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random 
import ast


def main_func(request): 
    template_name = 'restaurant/main.html'
    return render(request,template_name)

def orders(request):
    template_name = 'restaurant/order.html'
    menu_items = [
        {"item": "Daily Special", "value": "daily_special", "price": 12.00},
        {"item": "Lentil Soup", "value": "lentil", "price": 6.00},
        {"item": "Breakfast Burrito", "value": "burrito", "price": 11.00},
        {"item": "Grain Bowl", "value": "grains", "price": 11.00},
        {"item": "Pizza", "value": "pizza", "price": 15.00, "toppings": [
            {"item": "Extra Cheese", "value": "extra_cheese", "price": 1.00},
            {"item": "Pepperoni", "value": "pepperoni", "price": 1.00},
            {"item": "Mushrooms", "value": "mushrooms", "price": 1.00},
        ]}
    ]
    noras_cafe_menu = [
        {"item": "Avocado Toast", "price": 12.00},
        {"item": "Eggs Benedict", "price": 7.00},
        {"item": "Grilled Cheese Sandwich", "price": 7.00},
        {"item": "Chicken Caesar Salad", "price": 7.00},
        {"item": "Bacon Cheeseburger", "price": 13.00},
        {"item": "Veggie Wrap", "price": 10.00},
        {"item": "Spaghetti Carbonara", "price": 15.00},
        {"item": "Lemon Pepper Chicken", "price": 15.00},
        {"item": "Classic French Toast", "price": 6.00},
        {"item": "Fish Tacos", "price": 3.00},  # Note: $3.00 per item
        {"item": "Mushroom Risotto", "price": 10.00},
        {"item": "Steak Frites", "price": 15.00},
        {"item": "Turkey Panini", "price": 12.00},
        {"item": "Margherita Pizza", "price": 15.00},
        {"item": "Blueberry Pancakes", "price": 10.00}
    ]
    daily_special = random.choice(noras_cafe_menu)
    context = {
        "daily_special": daily_special,
        "menu_items": menu_items
    }
    return render(request,template_name,context)

def submit(request):
    '''Handle the form submission.
    Read the form data from the request,
    and send it back to a template
    '''
    template_name = "restaurant/confirmation.html"
    # read the form data into python variables:
    print(request.POST)
    orders = []
    if request.POST:
        selected_items = request.POST.getlist('menu')
        dicts = [ast.literal_eval(item) for item in selected_items]
        total_price = sum(item['price'] for item in dicts)
        for item in dicts:
            orders.append(f"{item['item']}: ${item['price']}<br>")
        
        final_string = ''.join(orders)
            
        # orders = []
        # print(selected_items)
        # for dish in selected_items:
        #     print(dish)
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        special = request.POST['special']
        current_time = time.time()
        random_seconds = random.randint(30 * 60, 60 * 60)
        ready_time_in_seconds = current_time + random_seconds
        ready_time_struct = time.localtime(ready_time_in_seconds)
        ready_time = time.strftime('%I:%M %p', ready_time_struct)
        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'menu': final_string,
            'special': special,
            'price': total_price,
            'ready_time': ready_time,

        }
        return render(request, template_name, context=context)