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


    def top_products(self) -> pd.DataFrame: 
        DATA = []
        sql = ExtractionQueries(yearClause=self.yearClause).top_products_script()
        try:
            print('Fetching top product data')
            for data in pd.read_sql(sql, self.conn, chunksize=10):
                DATA.append(data)
            df = pd.concat(DATA)
            
            df['product_name'] = df['product_name'].str.title().str.replace('_', ' ')
            return df
        
        except Exception as e:
            print('Could not fetch data for top products', e) 
            return pd.DataFrame(columns=['product_name', 'number_ordered'])
        
    def total_orders(self) -> int:
        sql = ExtractionQueries(yearClause=self.yearClause).total_order_script()
        print('orders sql', sql)
        df = pd.read_sql(sql, self.conn)
        orders = df['orders'][0]
        format_number = lambda x: f"{x/1000:.2f}K" if x < 1_000_000 else f"{x/1_000_000:.2f}M"
        formatted_orders = format_number(orders)
        return formatted_orders
    
    def total_sales(self) -> float:
        sql = ExtractionQueries(yearClause=self.yearClause).total_sales_script()
        df = pd.read_sql(sql, self.conn)
        sales = df['sales'][0]
        format_number = lambda x: f"{x/1000:.2f}K" if x < 1_000_000 else f"{x/1_000_000:.2f}M"
        formatted_sales = format_number(sales)
        return formatted_sales


