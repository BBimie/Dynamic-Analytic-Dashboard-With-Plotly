from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
from data.database.connection import Database
from extract.handler import FetchData, FilterValues
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots

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
    payment_type_json = json.dumps(payment_methods(), cls=PlotlyJSONEncoder)
    revenue_growth_json = json.dumps(revenue_growth_fig(), cls=PlotlyJSONEncoder)
    print(type(product_json), 'typee')
    return render_template('dashboard.html', 
                            filters=dashboard_filters(), 
                            product_plot=product_json, 
                            card=card_data(year=year),
                            payment_type_plot=payment_type_json,
                            revenue_growth_plot=revenue_growth_json)

    # elif request.method == 'POST':
    #     year = request.form.get('year')
    #     product_json = json.dumps(top_product_data(year=year), cls=PlotlyJSONEncoder)
    #     return product_json


def top_product_data(year):
    df = FetchData(year=None, db=database_name).top_products()

    fig = px.bar(df.tail(10), y='Product Name', x='Revenue', barmode='group', orientation='h', title='Plot 1')
    return fig
    # layout = go.Layout(xaxis=dict(tickangle=-50),title='Plot 1')
    # return go.Figure(data=data, layout=layout)

def card_data(year) -> dict:
    fetch = FetchData(year=year,  db=database_name)

    orders = fetch.total_orders()
    sales = fetch.total_sales()
    customers = fetch.total_customers()
    products = fetch.total_number_of_products()

    return {'orders':orders, 'sales':sales, 'customers':customers, 'products':products}

def payment_methods():
    df = FetchData(year=2018, db=database_name).payment_types()
    fig = px.pie(df, values='Number of Entries', names='Payment Type', hole=.5, title='Plot 2')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def revenue_growth_fig():
    df = FetchData(year=2018, db=database_name).revenue_growth()
    #fig = px.line(df, x="Date", y="Revenue", title='Revenue Growth')

    # Create the bar chart subplot
    bar_fig = px.bar(df, x="Date", y="Order Quantity", title='Order Quantity')
    bar_fig.update_traces(yaxis='y1', name="Order Quantity")  # Set yaxis to y1

    # Create the line chart subplot
    line_fig = px.line(df, x="Date", y="Revenue", title='Revenue Growth',)
    line_fig.update_traces(yaxis='y2', line = dict(color = 'red', width = 4), name="Revenue")  # Set yaxis to y2


    # Combine the two subplots into one figure
    combined_fig = bar_fig
    combined_fig.add_traces(line_fig.data)

    # Update the layout of the combined figure
    combined_fig.update_layout(
        title='Revenue Growth and Order Quantity',
        xaxis_title='Date',
        yaxis=dict(
            title='Order Quantity',
            side='left',
            position=0.1  # Adjust the position of the left y-axis
        ),
        yaxis2=dict(
            title='Revenue',
            side='right',
            overlaying='y',
            position=1.0  # Adjust the position of the right y-axis
        )
    )


    return combined_fig


def dashboard_filters() -> dict:
    year = FilterValues(db=database_name).year_filter()

    return {'year':year}


if __name__ == '__main__':
    app.run(debug=True)