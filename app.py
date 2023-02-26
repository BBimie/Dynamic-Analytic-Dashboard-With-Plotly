from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
from src.data.database.connection import Database

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
# db = SQLAlchemy(app)
# ma = Marshmallow(app)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def entrypoint():
    pass

def get_data():
    pass


if __name__ == '__main__':
    app.run()