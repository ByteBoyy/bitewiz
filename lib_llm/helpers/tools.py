import os
import json
import requests
from collections import defaultdict
import datetime
import uuid

def call_api(path: str, method: str = "GET", headers: dict = None, data: dict = None, params: dict = None):
    API_BASE_URL = os.getenv("API_BASE_URL")
    endpoint = f"{API_BASE_URL.rstrip('/')}/{path.lstrip('/')}"
    method = method.upper()
    headers = headers or {}
    
    try:
        response = requests.request(
            method=method,
            url=endpoint,
            headers=headers,
            json=data,
            params=params
        )
        response.raise_for_status()
        print(f"Response from {method} {endpoint}: Successfull")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Response: {response.text}")
        return None
    except Exception as err:
        print(f"Other error occurred: {err}")
        return None

def search_restaurants(args):
    """Search for restaurants that match specific moods and preferences"""
    mood = args.get("mood", "").lower()
    lat, long = args.get("lat"), args.get("long")
    preference = args.get("preference", "").lower()
    cuisine = args.get("cuisine", "").lower()
    source = args.get("source", "device")
    
    url_path = f"/device/{lat}/{long}"
    api_response = call_api(url_path, method="GET")
    
    if not api_response:
        return {
            "is_llm_needed": True,
            "data": "No restaurants found for your search"
        }
    
    restaurants = api_response.get("restaurants", [])
    
    # Filter restaurants based on cuisine if provided, otherwise show all
    if cuisine:
        cuisine_lower = cuisine.lower()
        matching_restaurants = [
            r for r in restaurants
            if any(c.lower() == cuisine_lower for c in r.get("cuisines", []))
        ]
    else:
        matching_restaurants = restaurants  # Show all restaurants if no cuisine specified
    
    print(matching_restaurants, '\n\n\n\n')
    
    # Initialize variables
    additional_info = ""
    device_instruction = ""
    
    if len(matching_restaurants) >= 5:
        display_restaurants = matching_restaurants[:3]
        if source == "device":
            device_instruction = "Tell the user they can refer to the kiosk screen for the full list of restaurants."
        elif source == "phone":
            device_instruction = "Tell the user they have SMS with link to the full list of available restaurants."
    else:
        display_restaurants = matching_restaurants[:5]
        additional_info = "Would you like to know more about any of these restaurants' menus?"
    
    result = "Based on what you're in the mood for, I've found these great options:\n\n"
    for restaurant in display_restaurants:
        result += f"• {restaurant['name']} \n"
    
    # Add additional info and device instruction only if they exist
    if additional_info:
        result += f"\n{additional_info}"
    if device_instruction:
        result += f". Also {device_instruction}"
    
    return {
        "data": result,
        "type": "restaurants",
        "is_llm_needed": False,
        "api_data": matching_restaurants
    }

def search_cuisines(args):
    """Search for cuisines that match specific moods and preferences"""
    cuisine = args.get("cuisine", "").lower()
    lat, long = args.get("lat"), args.get("long")
    source = args.get("source", "device")
    
    url_path = f"/device/cuisine-dietary/{lat}/{long}"
    api_response = call_api(url_path, method="GET")
    
    if not api_response:
        return {
            "is_llm_needed": True,
            "data": "No cuisines found for your search"
        }
    
    matching_cuisines = api_response.get("cuisines", [])
    
    # Initialize variables
    additional_info = ""
    device_instruction = ""
    
    if len(matching_cuisines) >= 5:
        print("more than 5")
        display_cuisines = matching_cuisines[:3]
        if source == "device":
            device_instruction = "Tell the user they can refer to the kiosk screen for the full list of available cuisines."
        elif source == "phone":
            device_instruction = "Tell the user they have SMS with link to the full list of available cuisines."
    else:
        display_cuisines = matching_cuisines
        additional_info = "Would you like to know more about any of these restaurants' menus?"
    
    result = "Based on your preferred cuisines, I've found these great options:\n\n"
    for cuisine in display_cuisines:
        result += f"• {cuisine} \n"
    
    # Add additional info and device instruction only if they exist
    if additional_info:
        result += f"\n{additional_info}"
    if device_instruction:
        result += f". Also {device_instruction}"
    
    print(result)
    
    return {
        "data": result,
        "type": "cuisines",
        "is_llm_needed": False,
        "api_data": matching_cuisines
    }

def get_dietary_preferences(args):
    """Search for available dietary preferences"""
    lat, long = args.get("lat"), args.get("long")
    source = args.get("source", "device")
    
    url_path = f"/device/cuisine-dietary/{lat}/{long}"
    api_response = call_api(url_path, method="GET")
    
    if not api_response:
        return {
            "is_llm_needed": True,
            "data": "No dietary preferences found for your search"
        }
    
    matching_dietary = api_response.get("dietary", [])
    print(matching_dietary, "[ MATCHING_DIETRY ]")
    
    # Initialize variables
    additional_info = ""
    device_instruction = ""
    
    if len(matching_dietary) >= 8:
        display_dietary = matching_dietary[:5]
        if source == "device":
            device_instruction = "Tell the user they can refer to the kiosk screen for the full list of available dietary preferences."
        elif source == "phone":
            device_instruction = "Tell the user they have SMS with link to the full list of available dietary preferences."
    else:
        display_dietary = matching_dietary
    
    result = "These are the available dietary preferences:\n\n"
    for dietary_preference in display_dietary:
        result += f"• {dietary_preference} \n"
    
    # Add additional info and device instruction only if they exist
    if additional_info:
        result += f"\n{additional_info}"
    if device_instruction:
        result += f" Also {device_instruction}"
    
    return {
        "data": result,
        "type": "dietary_preferences",
        "is_llm_needed": False,
        "api_data": matching_dietary
    }

def get_restaurant_menu(args):
    """Fetch menu for a specific restaurant with flavor profiles highlighted"""
    restaurant_name = args.get("restaurant_name")
    lat, long = args.get("lat"), args.get("long")
    
    if not restaurant_name:
        return {
            "is_llm_needed": True,
            "data": "I couldn't find that restaurant in our system. Would you like me to recommend something else?"
        }
    
    url_path = f"/device/{lat}/{long}"
    api_response = call_api(url_path, method="GET")
    
    if not api_response:
        return {
            "is_llm_needed": True,
            "data": "No restaurant menu found for your search"
        }
    
    matching_restaurants = api_response.get("restaurants", [])
    
    # Find the restaurant details
    restaurant = next((r for r in matching_restaurants if r["name"].lower() == restaurant_name.lower()), None)
    print(f"Restaurant Found: {restaurant}. Restaurant Name: {restaurant_name}")
    
    if not restaurant:
        return {
            "is_llm_needed": True,
            "data": "I couldn't find information about that restaurant. Let me suggest something else."
        }
    
    # Group items by category
    category_map = defaultdict(list)
    for item in restaurant.get("items", []):
        for category in item.get("categories", []):
            category_name = category.get("name", "Uncategorized")
            category_map[category_name].append(item)
    
    # Format the menu
    formatted_menu = f"📋 Here's the menu for *{restaurant_name}*:\n\n"
    for category_name in sorted(category_map.keys()):
        formatted_menu += f"*{category_name}*\n"
        for item in category_map[category_name]:
            name = item["name"]
            price = f"${item['current_price']:.2f}"
            description = item.get("description", "No description available.")
            formatted_menu += f"• {name} — {price}\n\n"
        formatted_menu += "\n"
    formatted_menu += "When you're ready to order, I can help connect you with their ordering system."
    
    return {
        "type": "menu",
        "data": formatted_menu,
        "is_llm_needed": False,
        "api_data": category_map
    }

def save_order(args):
    """Save the order details to a consolidated JSON file"""
    restaurant_name = args.get("restaurant_name")
    lat, long = args.get("lat"), args.get("long")
    items = args.get("items", [])
    user_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()
    
    if not restaurant_name or not items:
        return {
            "is_llm_needed": True,
            "data": "I need to know which restaurant and what items you want to order."
        }
    
    # Calculate total bill
    total_bill = 0
    for item in items:
        quantity = item.get("quantity", 1)
        price = item.get("price", 0)
        total_bill += quantity * price
    
    # Create order object
    order = {
        "order_id": str(uuid.uuid4()),
        "user_id": user_id,
        "restaurant_name": restaurant_name,
        "items": items,
        "total_bill": total_bill,
        "timestamp": timestamp
    }
    
    # Path to the orders JSON file
    orders_file = "orders/orders.json"
    os.makedirs(os.path.dirname(orders_file), exist_ok=True)
    
    # Load existing orders or create new array
    try:
        with open(orders_file, "r") as f:
            orders = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        orders = []
    
    # Add new order and save back to file
    orders.append(order)
    
    with open(orders_file, "w") as f:
        json.dump(orders, f, indent=4)
    
    formatted_items = ', '.join([f"{item.get('quantity', 1)}x {item.get('name')}" for item in items])
    
    return {
        "is_llm_needed": False,
        "data": f"Great! I've saved your order from {restaurant_name}. Your order includes: {formatted_items}. The total comes to ${total_bill:.2f}. Your order ID is {order['order_id']}."
    }