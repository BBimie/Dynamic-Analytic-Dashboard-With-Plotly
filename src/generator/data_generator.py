from faker import Faker
from datetime import datetime
from uuid import uuid4
import random
import time
import pandas as pd


fake = Faker()

states = ['Abia', 'Adamawa', 'Akwa Ibom','Anambra', 'Bauchi', 'Bayelsa', 'Benue', 'Borno',
            'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'Gombe', 'Imo',
            'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos',
            'Nasarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers',
            'Sokoto', 'Taraba', 'Yobe', 'Zamfara']

products = {
            'Clothing': {'items':['Shirts', 'Trousers', 'Jumpsuits'],
                            'prices': [1500, 2000, 2500] }, 
            'Electronics' : {'items' : ['Air Conditioner'], 
                                'prices': [20000]},
            'Computer Accessories': {'items' : ['Bluetooth Speaker', 'CPU Air Coolers', 'Keyboard'],
                                    'prices': [4500, 6000, 4500]}, 
            'Home & Outdoors': {'items': ['Area Rugs', 'Mirrors'],
                                'prices': [12000, 3200]}, 
            'Skin Care' : {'items': ['Mositurizers', 'Toners', 'Cleansers'], 
                            'prices': [2500, 2500, 2300]}, 
            'Health & Sports': {'items': ['Treadmills', 'Dumbbells'], 
                                'prices': [100000, 5000]}, 
            }



class GenerateOrders():
    def __init__(self) -> None:
        pass

    def number_of_orders(self):
        number = random.randint(3000, 10000)
        return number

    def order_date(self):
        start_date = datetime.date(year=2022, month=1, day=1) #first order date always defaults to 2022
        date = fake.date_between(start_date=start_date, end_date='today')
        date = datetime.datetime.strftime(date, '%d-%m-%Y')
        return date

    def order_location(self):
        random_state = random.choice(states)
        return random_state

    def product_category(self):
        category = random.choice(products.keys())
        return category

    def item_ordered(self):
        category = self.product_category()
        item = random.choice(products[category]['items'])
        price = random.choice(products[category]['prices'])
        units = random.randint(1, 15)
        return {'category':category, 'item':item, 'price':price, 'units':units}
       


    def generate_order(self, start_date, prop):
        ORDER = []
        df = pd.DataFrame()
        for order in range(1, self.number_of_orders()):
            date = self.order_date()
            location = self.order_location()
            product_category = self.item_ordered['category']
            item_ordered = self.item_ordered['item']
            unit_price = self.item_ordered['price']
            total_units = self.item_ordered['units']
            #store_visit = {'order':order, 'date': date, 'location':location, 'category':product_category, item_ordered}



            