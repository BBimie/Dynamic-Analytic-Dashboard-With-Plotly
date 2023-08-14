from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly
import plotly.express as px
from data.database.connection import Database
from extract.handler import FetchData, FilterValues
import plotly
import plotly.graph_objs as go

import json
from plotly.utils import PlotlyJSONEncoder

app = Flask(__name__)

database_name = 'data/database/db/ecommerce'


@app.route('/setup_database', methods=['GET', 'POST'])
def start_database():
    resp = Database(database_name).create_tables()
    if resp:
        return 'Database successfully created'
    else:
        return 'Database creation failed'



@app.route('/', methods=['GET', 'POST'])
def index():
    year = None
    product_json = json.dumps(top_product_data(year=year), cls=PlotlyJSONEncoder)
    print(type(product_json), 'typee')
    return render_template('dashboard.html', filters=dashboard_filters(), product_plot=product_json, card=card_data(year=year))

    # elif request.method == 'POST':
    #     year = request.form.get('year')
    #     product_json = json.dumps(top_product_data(year=year), cls=PlotlyJSONEncoder)
    #     return product_json


def top_product_data(year):
    df = FetchData(year=2018, db=database_name).top_products()
    print(df, 'shape')
    print(year, 'sent year')
    #data = [go.Bar(x=df['product_name'].str.title().str.replace('_', ' '), y=df['number_ordered'])]

    fig = px.bar(df, x='product_name', y='number_ordered', barmode='group')
    return fig
    # layout = go.Layout(xaxis=dict(tickangle=-50),title='Plot 1')
    # return go.Figure(data=data, layout=layout)

def card_data(year) -> dict:
    orders = FetchData(year=year, db=database_name).total_orders()
    sales = FetchData(year=year,  db=database_name).total_sales()

    return {'orders':orders, 'sales':sales}

def dashboard_filters() -> dict:
    year = FilterValues(db=database_name).year_filter()

    return {'year':year}


if __name__ == '__main__':
    app.run(debug=True)