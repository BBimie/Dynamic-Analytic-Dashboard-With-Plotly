# Dynamic-Analytic-Dashboard-With-Plotly
A dynamic dashboard built with plotly, the data is stored in a database and the webapp is built with FastAPI


- CSV data > SQL database (with maybe ORM?)  > queries to get the data out > data rendered into plotly dashboard


Note that the |safe filter is used to mark the JSON data as safe for rendering in the HTML template. This is important for security reasons.

With these steps, you should be able to render multiple Plotly graphs in an HTML file using Flask.
