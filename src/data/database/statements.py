import sqlalchemy

class DatabaseSetup:
    def __init__(self):
        pass

    def customer_table(self):
        return { "file" : "customer.csv", 
                  "create_query" : """ CREATE TABLE  IF NOT EXISTS  customer (
                                        id VARCHAR NOT NULL PRIMARY KEY,
                                        unique_id VARCHAR NOT NULL,
                                        zip_code_prefix VARCHAR,
                                        city VARCHAR,
                                        state VARCHAR
                                            ); """,
                    "insert_query": """ INSERT INTO customer (id, unique_id, zip_code_prefix, city, state) 
                                        VALUES (?, ?, ?, ?, ?)  """ 
                }

    def orders_table(self):
        return { "file" : "orders.csv", 
                  "create_query" :""" CREATE TABLE  IF NOT EXISTS  orders (
                        id VARCHAR NOT NULL PRIMARY KEY,
                        customer_id VARCHAR REFERENCES customer,
                        order_status VARCHAR,
                        order_purchase_timestamp TEXT,
                        order_approved_at TEXT,
                        order_delivered_carrier_date TEXT,
                        order_delivered_customer_date TEXT,
                        order_estimated_delivery_date TEXT
                    );""",
                    "insert_query": """ INSERT INTO orders (id, customer_id, order_status, order_purchase_timestamp, order_approved_at, 
                                                        order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date ) 
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)  """  }

    def order_items_table(self):
        return { "file" : "order_items.csv", 
                  "create_query" :""" CREATE TABLE  IF NOT EXISTS  order_items (
                        order_id VARCHAR REFERENCES orders NOT NULL,
                        order_item_id INTEGER NOT NULL,
                        product_id VARCHAR REFERENCES products NOT NULL,
                        seller_id VARCHAR REFERENCES sellers NOT NULL,
                        shipping_limit_date TEXT,
                        price REAL NOT NULL, 
                        freight_value REAL
                    );""",
                    "insert_query": """ INSERT INTO order_items (order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value) 
                                        VALUES (?, ?, ?, ?, ?, ?, ?)  """ }

    def order_payments_table(self):
        return { "file" : "order_payments.csv", 
                  "create_query" :""" CREATE TABLE  IF NOT EXISTS order_payments (
                        order_id VARCHAR REFERENCES orders NOT NULL,
                        payment_sequential INTEGER NOT NULL,
                        payment_type VARCHAR,
                        payment_installments INTEGER,
                        payment_value REAL NOT NULL
                    );""",
                    "insert_query": """ INSERT INTO order_payments (order_id, payment_sequential, payment_type, payment_installments, payment_value) 
                                        VALUES (?, ?, ?, ?, ?)  """}

    def order_reviews_table(self):
        return { "file" : "order_reviews.csv", 
                  "create_query" :""" CREATE TABLE IF NOT EXISTS order_reviews (		
                        id VARCHAR NOT NULL PRIMARY KEY,
                        order_id VARCHAR REFERENCES orders,
                        review_score INTEGER NOT NULL,
                        review_creation_date TEXT,
                        review_answer_timestamp TEXT
                    );""",
                "insert_query": """ INSERT INTO order_reviews ( id, order_id, review_score, review_creation_date, review_answer_timestamp ) 
                                        VALUES (?, ?, ?, ?, ?)  """}

    def products_table(self):
        return { "file" : "products.csv", 
                  "create_query" : """ CREATE TABLE  IF NOT EXISTS  products ( 				
                        id VARCHAR NOT NULL PRIMARY KEY,
                        category_name VARCHAR NOT NULL,
                        product_name_length REAL,
                        description_length REAL,
                        product_photos_qty REAL,
                        product_weight_g REAL,
                        product_length_cm REAL,
                        product_height_cm REAL,
                        product_width_cm REAL
                    );""",
                    "insert_query": """ INSERT INTO products (id, category_name, product_name_length, description_length, product_photos_qty, product_weight_g,
                                                        product_length_cm, product_height_cm, product_width_cm) 
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  """ }

    def product_name_translation_table(self):
        return { "file" : "product_category_name_translation.csv", 
                  "create_query" : """ CREATE TABLE  IF NOT EXISTS  product_category_name_translation ( 	
                        product_category_name VARCHAR NOT NULL PRIMARY KEY,
                        product_category_name_english VARCHAR NOT NULL
                    );""",
                    "insert_query": """ INSERT INTO product_category_name_translation ( product_category_name, product_category_name_english )
                                        VALUES (?, ?) ; """ }

    def sellers_table(self):
        return { "file" : "seller.csv", 
                "create_query" : """ CREATE TABLE IF NOT EXISTS  seller ( 		
                            seller_id VARCHAR NOT NULL PRIMARY KEY,
                            seller_zip_code_prefix INTEGER,
                            seller_city VARCHAR,
                            seller_state VARCHAR
                            );""",
                    "insert_query": """ INSERT INTO seller (seller_id, seller_zip_code_prefix, seller_city, seller_state) 
                                        VALUES (?, ?, ?, ?)  """
            }

    def all_tables(self):
        return [self.customer_table(), 
             self.sellers_table(), 
             self.products_table(),
             self.orders_table(), 
             self.order_items_table(),
             self.order_payments_table(), 
             #self.order_reviews_table(),
             self.product_name_translation_table() ]