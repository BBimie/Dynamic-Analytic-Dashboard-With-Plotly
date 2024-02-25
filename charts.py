import pandas as pd
from data.database.connection import Database
from extract.query import ExtractionQueries, FilterQueries
from extract.handler import FetchData, FilterValues
import plotly.graph_objs as go
import numpy as np


database_name = "data/database/db/ecommerce"


class FilterParams:
    def __init__(self) -> None:
        pass

    def year(self):
        pass


class DashboardCharts:
    def __init__(self, year, db) -> None:
        self.year = year
        self.db = db

        if year == "All":
            self.yearClause = " IS NOT NULL "
        else:
            self.yearClause = f" = '{year}' "

        self.conn = Database(db_name=self.db).connect()
        self.extraction_queries = ExtractionQueries(yearClause=self.yearClause)

    def card_chart(self, title, value):
        # Create the figure
        fig = go.Figure()

        # Add a number card trace
        fig.add_trace(
            go.Indicator(
                value=value,
                title={
                    "text": title,
                    "font": {"size": 16},
                },
                number={
                    "font.size": 25,
                },
            )
        )
        fig.update_xaxes(visible=False, fixedrange=True)
        fig.update_yaxes(visible=False, fixedrange=True)
        fig.update_layout(
            margin=dict(t=30, b=0),
            showlegend=False,
            height=100,
        )
        return fig

    ## ------ AGGREGATES ------- #
    def sales_card_data(self):
        sql = self.extraction_queries.total_sales_script()
        df = pd.read_sql(sql, self.conn)
        sales = df["sales"][0]
        fig = self.card_chart(title="TOTAL SALES", value=sales)
        return fig

    def orders_card_data(self):
        sql = self.extraction_queries.total_order_script()
        df = pd.read_sql(sql, self.conn)
        orders = df["orders"][0]
        fig = self.card_chart(title="TOTAL ORDERS", value=orders)
        return fig

    def products_card_data(self):
        sql = self.extraction_queries.total_product_script()
        df = pd.read_sql(sql, self.conn)
        products = df["product"][0]
        fig = self.card_chart(title="TOTAL PRODUCTS", value=products)
        return fig

    def customers_card_data(self):
        sql = self.extraction_queries.total_customers_script()
        df = pd.read_sql(sql, self.conn)
        customers = df["customers"][0]
        fig = self.card_chart(title="TOTAL CUSTOMERS", value=customers)
        return fig

    def sellers_card_data(self) -> dict:
        sql = self.extraction_queries.total_sellers_script()
        df = pd.read_sql(sql, self.conn)
        sellers = df["sellers"][0]
        fig = self.card_chart(title="TOTAL SELLERS", value=sellers)
        return fig

    def top_product_data(self):
        DATA = []
        sql = self.extraction_queries.top_products_script()
        try:
            print("Fetching top product data")
            for data in pd.read_sql(sql, self.conn, chunksize=10):
                DATA.append(data)
            df = pd.concat(DATA)

            df["Product Name"] = df["Product Name"].str.title().str.replace("_", " ")
            df = df.sort_values(by="Revenue", ascending=False)

            trace = go.Bar(x=df["Product Name"], y=df["Revenue"])
            layout = go.Layout(title="Top 10 Products")
            fig = go.Figure(data=[trace], layout=layout)

            return fig

        except Exception as e:
            print("Could not fetch data for top products", e)
            return pd.DataFrame(columns=["Product Name", "Order Quantity"])

    def product_heatmap(self):
        DATA = []
        sql = self.extraction_queries.products_distribution_script()
        try:
            print("Fetching product revenue distribution")
            for data in pd.read_sql(sql, self.conn, chunksize=10):
                DATA.append(data)
            df = pd.concat(DATA)

            df["Product Name"] = df["Product Name"].str.title().str.replace("_", " ")

            # Set shades of blue
            colors = ["#00A5FF", "#0077CC", "#004488", "#001155"]

            # Create heatmap
            fig = go.Figure(
                go.Treemap(
                    labels=df["Product Name"],
                    parents=[""] * len(df["Product Name"]),
                    values=df["Revenue"],
                    marker_colors=colors,
                    textinfo="label+value+percent entry",
                )
            )
            fig.update_layout(
                title="Product Revenue",
                treemapcolorway=["blue"],
            )
            return fig

        except Exception as e:
            print("Could not fetch data for top products", e)
            return pd.DataFrame(columns=["Product Name", "Order Quantity"])

    def payment_type_pie_chart(self):
        DATA = []
        sql = self.extraction_queries.payment_types_script()

        for data in pd.read_sql(sql, self.conn, chunksize=10):
            DATA.append(data)
        df = pd.concat(DATA)
        df["payment_type"] = df["payment_type"].str.replace("_", "").str.title()

        # Create pie chart
        fig = go.Figure(
            data=[go.Pie(labels=df["payment_type"], values=df["number_of_entries"])]
        )

        # Update layout
        fig.update_layout(title="Pie Chart Example")
        return fig

    def daily_revenue_trend(self):
        DATA = []
        sql = self.extraction_queries.daily_sales_script()

        for data in pd.read_sql(sql, self.conn, chunksize=10):
            DATA.append(data)
        df = pd.concat(DATA)

        # Create trace
        trace = go.Scatter(x=df["date"], y=df["num_orders"], mode="lines")

        # Create layout
        layout = go.Layout(title="Line Chart Example")

        # Create figure
        fig = go.Figure(data=[trace], layout=layout)
        return fig
