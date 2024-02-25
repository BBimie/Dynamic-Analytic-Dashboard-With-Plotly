class FilterQueries:
    def __init__(self) -> None:
        pass

    def year_filter_script(self):
        return """SELECT DISTINCT strftime('%Y', order_purchase_timestamp) AS year FROM orders """


# WHERE strftime('%Y', order_purchase_timestamp) =


class ExtractionQueries:
    def __init__(self, yearClause) -> None:
        self.yearClause = yearClause

    def total_sales_script(self) -> str:
        return f""" SELECT SUM(payment_value) AS 'sales' FROM order_payments op 
                    LEFT JOIN orders o ON o.id = op.order_id
                    WHERE strftime('%Y', order_purchase_timestamp) {self.yearClause}
                      """

    def total_order_script(self) -> str:
        return f""" SELECT COUNT(id) AS 'orders' FROM orders 
                    WHERE strftime('%Y', order_purchase_timestamp) {self.yearClause}
                      """

    def total_customers_script(self) -> str:
        return """ SELECT count(id) AS customers FROM customer """

    def total_product_script(self) -> str:
        return """ SELECT count(id) AS product FROM products """

    def total_sellers_script(self) -> str:
        return """ SELECT count(seller_id) as sellers from seller """

    def total_delivered_order_script(self) -> str:
        return """ SELECT COUNT(id) AS 'orders' FROM orders WHERE order_status = 'delivered' """

    def monthly_sales(self) -> str:
        return """  """

    def top_products_script(self) -> str:
        return f""" SELECT pt.product_category_name_english AS 'Product Name', 
                            SUM(oi.price)  AS 'Revenue' 
                    FROM order_items oi
                    LEFT JOIN products p on p.id = oi.product_id
                    LEFT JOIN product_category_name_translation pt ON p.category_name = pt.product_category_name
                    LEFT JOIN orders o ON o.id = oi.order_id
                    WHERE strftime('%Y', order_purchase_timestamp) {self.yearClause}
                    GROUP BY 1
                    ORDER BY 2 DESC
                    LIMIT 10  """

    def products_distribution_script(self) -> str:
        return f""" SELECT pt.product_category_name_english AS 'Product Name', 
                            SUM(oi.price)  AS 'Revenue' 
                    FROM order_items oi
                    LEFT JOIN products p on p.id = oi.product_id
                    LEFT JOIN product_category_name_translation pt ON p.category_name = pt.product_category_name
                    LEFT JOIN orders o ON o.id = oi.order_id
                    WHERE strftime('%Y', order_purchase_timestamp) {self.yearClause}
                    GROUP BY 1
                    ORDER BY 2 DESC
                     """

    def payment_types_script(self) -> str:  # pie chart
        return f""" SELECT payment_type, COUNT(order_id) AS number_of_entries
                    FROM order_payments op 
                    LEFT JOIN orders o ON o.id = op.order_id
                    WHERE strftime('%Y', order_purchase_timestamp) {self.yearClause}
                    AND payment_type != 'not_defined'
                    GROUP BY payment_type """

    def daily_sales_script(self):
        return f""" SELECT DATE(order_purchase_timestamp) AS date, 
                            COUNT(id) AS num_orders FROM orders,
                            SUM()
                    WHERE strftime('%Y', order_purchase_timestamp) {self.yearClause}
                    GROUP BY 1"""

    def top_state_revenue_script(self):
        return f""" SELECT c.state, sum(payment_value) AS revenue 
                    FROM order_payments op 
                        LEFT JOIN orders o ON o.id = op.order_id
                        LEFT JOIN customer c ON c.id = o.customer_id
                    GROUP BY c.state 
                    ORDER BY 2 DESC 
                    LIMIT 10 """

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
