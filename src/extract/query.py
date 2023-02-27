
class Top10Products:
    def __init__(self) -> None:
        pass

    def script() -> str:
        return """ SELECT pt.product_category_name_english AS product_name, 
                            COUNT(oi.product_id) AS 'number_ordered'  FROM order_items oi
                    LEFT JOIN products p on p.id = oi.product_id
                    LEFT JOIN product_category_name_translation pt ON p.category_name = pt.product_category_name
                    GROUP BY p.category_name
                    ORDER BY 2 DESC 
                    LIMIT 10 """


class TotalSales:
    def __init__(self) -> None:
        pass

    def script() -> str:
        pass

class TotalProfits:
    def __init__(self) -> None:
        pass

    def script() -> str:
        pass

class TotalOrders:
    def __init__(self) -> None:
        pass

    def script() -> str:
        pass

class productData:
    def __init__(self) -> None:
        pass

    def script() -> str:
        pass

class productData:
    def __init__(self) -> None:
        pass

    def script() -> str:
        pass