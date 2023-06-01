from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
from src.data.database.connection import Database
from src.extract.handler import GenerateData, FilterValues
import plotly
import plotly.graph_objs as go

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
# db = SQLAlchemy(app)
# ma = Marshmallow(app)

app = Flask(__name__)

@app.route('/her', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        year = request.form.get('year')
        product_json = top_product_data(year=year).to_json()
        return render_template('dashboard.html', filters=dashboard_filters(), product_plot=product_json, card=card_data(year=year))
    else:
        year = None
        product_json = top_product_data(year=year).to_json()
        return render_template('dashboard.html', filters=dashboard_filters(), product_plot=product_json, card=card_data(year=year))
    
    


# @app.route('/', methods=['GET', 'POST'])
# def dashboard():
#     year = request.form.get('year')
#     product_json = top_product_data(year=year).to_json()
#     return render_template('dashboard.html', filters=dashboard_filters(), product_plot=product_json, card=card_data(year=year))


def top_product_data(year):
    df = GenerateData(year=2018).top_products()
    print(year, 'sent year')
    data = [go.Bar(x=df['product_name'].str.title().str.replace('_', ' '), y=df['number_ordered'])]
    layout = go.Layout(xaxis=dict(tickangle=-50),title='Plot 1')
    return go.Figure(data=data, layout=layout)

def card_data(year) -> dict:
    orders = GenerateData(year=2018).total_orders()
    sales = GenerateData(year=year).total_sales()

    return {'orders':orders, 'sales':sales}

def dashboard_filters() -> dict:
    year = FilterValues().year_filter()

    return {'year':year}


if __name__ == '__main__':
    app.run(debug=True)