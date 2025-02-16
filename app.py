from flask import Flask, jsonify, send_file, render_template_string
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Function to load the Parquet file into a DataFrame
def load_parquet(file_path):
    parquet_df = pd.read_parquet(file_path)
    return parquet_df

# Generate a single Plotly bar plot for companies per sector
def generate_plot(parquet_df):
    fig = px.bar(parquet_df['setor'].value_counts().reset_index(), x='count', y='setor', title='Bar Plot of Sector')
    return fig.to_html(full_html=False)

# Generate multiple Plotly histogram plots for numerical columns
def generate_plots(parquet_df):
    plots_html = []
    for col in parquet_df.select_dtypes(include=['number']).columns:
        fig = px.histogram(parquet_df, x=col, nbins=30, title=f'Histogram of {col}')
        plots_html.append(fig.to_html(full_html=False))
    return plots_html

# Landing page with navigation links@app.route('/')
def landing_page():
    return render_template_string("""
        <html>
            <head>
                <title>Dashboard</title>
                <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
                <style> /* CSS styles for the landing page */ </style>
            </head>
            <body>
                <h1>Welcome to the Dashboard</h1>
                <p>What question are you interested in?</p>
                <ul>
                    <li><a href="/plot">Number of companies per sector</a></li>
                    <li><a href="/table">Data table</a></li>
                    <li><a href="/plots">Distribution of numerical categories</a></li>
                </ul>
                <footer>Created by Beatriz Freitas for DataOps</footer>
            </body>
        </html>
    """)

# Load data at application startup
parquet_file_path = 'data/dados_sensores_5000.parquet'
df = load_parquet(parquet_file_path)

# Generate an HTML table from the DataFrame
def generate_table():
    return df.to_html()

# Endpoint to display a single plot@app.route('/plot')
def plot():
    plot_html = generate_plot(df)
    return plot_html

# Endpoint to display multiple plots@app.route('/plots')
def plots():
    plots_html = generate_plots(df)
    return render_template_string("""
        <html>
            <head><title>Multiple Plots</title></head>
            <body>
                <h1>Histograms of Numerical Data</h1>
                <div class="plot-container">
                    {% for plot in plots_html %}
                        <div>{{ plot | safe }}</div>
                    {% endfor %}
                </div>
            </body>
        </html>
    """, plots_html=plots_html)

# Endpoint to display the data table@app.route('/table')
def table():
    return generate_table()

if __name__ == '__main__':
    app.run(debug=True)
