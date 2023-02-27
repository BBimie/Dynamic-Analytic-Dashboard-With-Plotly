from data.database.connection import Database
from query import Top10Products
import pandas as pd

class GenerateData:
    def __init__(self) -> None:
        pass

    def top_products(self): 
        DATA = []
        sql = Top10Products().script()
        for data in pd.read_sql(sql, Database(db_name='ecommerce').connect(), chunksize=10):
            DATA.append(data)
        df = pd.concat(DATA)
        try:
            df['product_name'] = df['product_name'].str.title().str.replace('_', ' ')
            return df
        except:
            return df


