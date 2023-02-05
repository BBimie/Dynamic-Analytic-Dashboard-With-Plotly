from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

app = Flask(__name__)

app.route('/')
def index():
    return render_template('dashboard.html')