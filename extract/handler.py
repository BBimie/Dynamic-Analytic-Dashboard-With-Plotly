from data.database.connection import Database
from extract.query import ExtractionQueries, FilterQueries
import pandas as pd


class FilterValues:
    def __init__(self, db) -> None:
        self.db = db
        self.conn = self.conn = Database(db_name=self.db).connect()

    def year_filter(self) -> list:
        sql = FilterQueries().year_filter_script()
        df = pd.read_sql(sql, self.conn)
        years:list = list(df['year'])
        return years


class FetchData:
    def __init__(self, year, db) -> None:
        #self.product = product
        self.year = year
        self.db = db
        if year != None:
            self.yearClause = f" WHERE strftime('%Y', order_purchase_timestamp) =  '{self.year}' "
        else:
            self.yearClause = ""
        self.conn = Database(db_name=self.db).connect()

    def _format_number(self, num):
        format_number = f"{num/1000:.2f}K" if num < 1_000_000 else f"{num/1_000_000:.2f}M"
        return format_number

    def top_products(self) -> pd.DataFrame: 
        DATA = []
        sql = ExtractionQueries(yearClause=self.yearClause).top_products_script()
        try:
            print('Fetching top product data')
            for data in pd.read_sql(sql, self.conn, chunksize=10):
                DATA.append(data)
            df = pd.concat(DATA)
            
            df['Product Name'] = df['Product Name'].str.title().str.replace('_', ' ')
            df=df.sort_values(by='Revenue', ascending=True)
            return df
        
        except Exception as e:
            print('Could not fetch data for top products', e) 
            return pd.DataFrame(columns=['Product Name', 'Order Quantity'])
        
    def total_orders(self) -> int:
        sql = ExtractionQueries(yearClause=self.yearClause).total_order_script()
        print('orders sql', sql)
        df = pd.read_sql(sql, self.conn)
        orders = df['orders'][0]
        formatted_orders = self._format_number(orders)
        return formatted_orders
    
    def total_sales(self) -> float:
        sql = ExtractionQueries(yearClause=self.yearClause).total_sales_script()
        df = pd.read_sql(sql, self.conn)
        sales = df['sales'][0]

        formatted_sales = self._format_number(sales)
        return formatted_sales
    
    def total_customers(self) -> float:
        sql = ExtractionQueries(yearClause=self.yearClause).total_customers_script()
        df = pd.read_sql(sql, self.conn)
        customers = df['customers'][0]

        customers = self._format_number(customers)
        return customers
    
    def total_delivered_orders(self) -> float:
        sql = ExtractionQueries(yearClause=self.yearClause).total_delivered_order_script()
        df = pd.read_sql(sql, self.conn)
        orders = df['orders'][0]

        orders = self._format_number(orders)
        return orders
    
    def total_number_of_products(self) -> float:
        sql = ExtractionQueries(yearClause=self.yearClause).total_product_script()
        df = pd.read_sql(sql, self.conn)
        orders = df['product'][0]

        orders = self._format_number(orders)
        return orders
    
    def payment_types(self) -> pd.DataFrame:
        sql = ExtractionQueries(yearClause=self.yearClause).payment_types()
        df = pd.read_sql(sql, self.conn)
        df['Payment Type'] = df['Payment Type'].str.replace('_', ' ').str.title()
        return df
    
    def revenue_growth(self)-> pd.DataFrame:
        sql = ExtractionQueries(yearClause=self.yearClause).revenue_growth_script()
        df = pd.read_sql(sql, self.conn)
        return df


