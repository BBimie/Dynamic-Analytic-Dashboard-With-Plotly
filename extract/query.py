
class FilterQueries:
    def __init__(self) -> None:
        pass

    def year_filter_script(self):
        return """SELECT DISTINCT strftime('%Y', order_purchase_timestamp) AS year FROM orders """


class ExtractionQueries:
    def __init__(self, yearClause) -> None:
        self.yearClause = yearClause

    def top_products_script(self) -> str:
        return f""" SELECT pt.product_category_name_english AS product_name, 
                            COUNT(oi.product_id) AS 'number_ordered' 
                    FROM order_items oi
                    LEFT JOIN products p on p.id = oi.product_id
                    LEFT JOIN product_category_name_translation pt ON p.category_name = pt.product_category_name
                    LEFT JOIN orders o ON o.id = oi.order_id
                    { self.yearClause }
                    GROUP BY p.category_name
                    ORDER BY 2 DESC 
                    LIMIT 10 """
    
    def payment_types(self)-> str:  #pie chart
        return f""" SELECT payment_type, count(*)  
                    FROM order_payments
                    GROUP BY payment_type """
    
    def monthly_sales(self) -> str:
        return """  """
    
    def order_growth_script(self) -> str:
        return """  """


    def total_sales_script(self) -> str:
        return """ SELECT SUM(payment_value) AS 'sales' FROM order_payments op 
                    LEFT JOIN orders o ON o.id = op.order_id  """

    def total_order_script(self) -> str:
        return f""" SELECT COUNT(id) AS 'orders' FROM orders
                    {self.yearClause}  """
    
    def total_delivered_order_script(self) -> str:
        return """ SELECT COUNT(id) AS 'orders' FROM orders WHERE order_status = 'delivered' """
    
    def number_products_sold() -> str:
        return """ """
    
    def min_delivery_period(self) -> str:
        return """ """
    
    
    