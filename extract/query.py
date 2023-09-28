
class FilterQueries:
    def __init__(self) -> None:
        pass

    def year_filter_script(self):
        return """SELECT DISTINCT strftime('%Y', order_purchase_timestamp) AS year FROM orders """


class ExtractionQueries:
    def __init__(self, yearClause) -> None:
        self.yearClause = yearClause

    def top_products_script(self) -> str:
        return f""" SELECT pt.product_category_name_english AS 'Product Name', 
                            SUM(oi.price)  AS 'Revenue' 
                    FROM order_items oi
                    LEFT JOIN products p on p.id = oi.product_id
                    LEFT JOIN product_category_name_translation pt ON p.category_name = pt.product_category_name
                    LEFT JOIN orders o ON o.id = oi.order_id
                    GROUP BY 1
                    ORDER BY 2 DESC
                    LIMIT 10  """
    
    def top_state_revenue_script(self):
        return f""" SELECT c.state, sum(payment_value) AS revenue 
                    FROM order_payments op 
                        LEFT JOIN orders o ON o.id = op.order_id
                        LEFT JOIN customer c ON c.id = o.customer_id
                    GROUP BY c.state 
                    ORDER BY 2 DESC 
                    LIMIT 10 """
    
    def payment_types(self)-> str:  #pie chart
        return f""" SELECT payment_type as 'Payment Type', count(*) AS 'Number of Entries'
                    FROM order_payments
                    GROUP BY payment_type """
    
    def total_sellers_script(self)  -> str:
        return """ """
    
    def total_sales_script(self) -> str:
        return """ SELECT SUM(payment_value) AS 'sales' FROM order_payments op 
                    LEFT JOIN orders o ON o.id = op.order_id  """

    def total_order_script(self) -> str:
        return f""" SELECT COUNT(id) AS 'orders' FROM orders
                      """
    
    def total_delivered_order_script(self) -> str:
        return """ SELECT COUNT(id) AS 'orders' FROM orders WHERE order_status = 'delivered' """
    
    def total_customers_script(self) -> str:
        return """ SELECT count(id) AS customers FROM customer """
    
    def total_product_script(self) -> str:
        return """ SELECT count(id) AS product FROM products """
    
    def monthly_sales(self) -> str:
        return """  """
    
    def revenue_growth_script(self) -> str:
        return """ SELECT strftime('%Y-%m', order_approved_at) AS Date,
                   SUM(payment_value) AS Revenue,
                   COUNT(o.id) AS 'Order Quantity'
            FROM orders o
            JOIN order_payments op ON op.order_id = o.id
            WHERE DATE(order_approved_at) IS NOT NULL
            GROUP BY Date
            ORDER BY Date """
    
    def number_products_sold() -> str:
        return """ """
    
    def min_delivery_period(self) -> str:
        return """ """
    
    
    