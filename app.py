import pandas as pd
import streamlit as st
from data.database.connection import Database
from extract.handler import FetchData, FilterValues
from charts import DashboardCharts
import matplotlib.pyplot as plt


# # Create SQLite Database
database_name = "data/database/db/ecommerce"


# def start_database():
#     resp = Database(database_name).create_tables()
#     if resp:
#         return "Database successfully created"
#     else:
#         return "Database creation failed"

st.set_page_config(page_title="Charty Netflix", page_icon="📊", layout="wide")

# dash header
c1, c2 = st.columns([7, 3])
with c1:
    st.subheader("OLIST Ecommerce Dashboard")
with c2:
    # filters
    year_option = st.selectbox(
        "Filter by Year", FilterValues(database_name).year_filter()
    )


# CARDS
card1, card2, card3, card4, card5 = st.columns(5)

with card1:
    st.plotly_chart(
        DashboardCharts(year=year_option, db=database_name).customers_card_data(),
        use_container_width=True,
    )
with card2:
    st.plotly_chart(
        DashboardCharts(year=year_option, db=database_name).sellers_card_data(),
        use_container_width=True,
    )
with card3:
    st.plotly_chart(
        DashboardCharts(year=year_option, db=database_name).products_card_data(),
        use_container_width=True,
    )
with card4:
    st.plotly_chart(
        DashboardCharts(year=year_option, db=database_name).sales_card_data(),
        use_container_width=True,
    )
with card5:
    st.plotly_chart(
        DashboardCharts(year=year_option, db=database_name).orders_card_data(),
        use_container_width=True,
    )

st.write("---")

# barcharts
bar1, bar2 = st.columns(2)

with bar1:
    st.plotly_chart(
        DashboardCharts(year=year_option, db=database_name).top_product_data(),
        use_container_width=True,
    )
with bar2:
    st.plotly_chart(
        DashboardCharts(year=year_option, db=database_name).payment_type_pie_chart(),
        use_container_width=True,
    )
st.write("---")
st.plotly_chart(
    DashboardCharts(year=year_option, db=database_name).daily_revenue_trend(),
    use_container_width=True,
)

st.write("---")
st.plotly_chart(
    DashboardCharts(year=year_option, db=database_name).product_heatmap(),
    use_container_width=True,
)
