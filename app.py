from flask import Flask, render_template_string
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Load the CSV file into a pandas DataFrame
def load_parquet(file_path):
    parquet_df = pd.read_parquet(file_path)
    return parquet_df

@app.route('/companies-per-sector')
def companies_per_sector():
    fig = px.bar(df['setor'].value_counts().reset_index(), x='count', y='setor', title='Bar Plot of Companies per Sector')
    fig.update_layout(
        xaxis_title='Number of Companies',
        yaxis_title='Sector',
    )

    plot_html = fig.to_html(full_html=False)
    return render_template_string("""
        <html>
            <head>
                <title>Companies per Sector</title>
                <style>
                    body {
                        font-family: 'Poppins', sans-serif;
                        background-color: #f4f4f9;
                        color: #333;
                        text-align: center;
                    }
                    h1 {
                        color: #ff7e5f;
                        margin-top: 50px;
                    }
                    .plot-container {
                        display: flex;
                        justify-content: center;
                        margin-top: 30px;
                    }
                    footer {
                        position: absolute;
                        bottom: 20px;
                        width: 100%;
                        font-size: 1em;
                        color: #333;
                    }
                </style>
            </head>
            <body>
                <h1>Number of Companies per Sector</h1>
                <div class="plot-container">
                    {{ plot_html | safe }}
                </div>
            </body>
        </html>
    """, plot_html=plot_html)


def generate_plot(parquet_df):
    # Create a Plotly plot (customize this based on your data)
    results = parquet_df.groupby('setor').agg({'energia_kwh': 'mean', 'agua_m3': 'mean', 'co2_emissoes': 'mean'}).reset_index()
    plots_html = []
    for col in results.columns[1:]:
        fig = px.bar(results.sort_values(col), x='setor', y=col, title=f'Bar Plot of average {col} spending by sector')
        plot_html = fig.to_html(full_html=False)
        plots_html.append(plot_html)
    return plots_html

def generate_plots(parquet_df):
    plots_html = []
    for col in parquet_df.select_dtypes(include=['number']).columns:
        fig = px.histogram(parquet_df, x=col, nbins=30, title=f'Histogram of {col}')
        plot_html = fig.to_html(full_html=False)
        plots_html.append(plot_html)
    return plots_html

def generate_kpis(parquet_df):
    kpis = {
        'Company with Lowest CO2 Emissions': parquet_df[parquet_df.co2_emissoes == parquet_df.co2_emissoes.min()],
        'Company with Highest CO2 Emissions': parquet_df[parquet_df.co2_emissoes == parquet_df.co2_emissoes.max()],
        'Company with Lowest Water Usage': parquet_df[parquet_df.agua_m3 == parquet_df.agua_m3.min()],
        'Company with Highest Water Usage': parquet_df[parquet_df.agua_m3 == parquet_df.agua_m3.max()],
        'Company with Lowest Energy Consumption': parquet_df[parquet_df.energia_kwh == parquet_df.energia_kwh.min()],
        'Company with Highest Energy Consumption': parquet_df[parquet_df.energia_kwh == parquet_df.energia_kwh.max()]
    }
    kpi_html = """
    <html><head><title>Company KPIs</title>
    <style>
        body { font-family: 'Poppins', sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); color: #333; padding: 20px; }
        h1 { text-align: center; color: #fff; }
        .kpi-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; }
        .kpi-card { background: #fff; border-radius: 15px; padding: 30px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); width: 600px; transition: transform 0.3s; }
        .kpi-card:hover { transform: translateY(-5px); }
        h3 { margin-top: 0; color: #ff6f61; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 1.1em; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #ff6f61; color: white; }
    </style></head><body>
    <h1>Which Company Consumes More or Less?</h1>
    <div class="kpi-container">
    """
    for key, value in kpis.items():
        styled_table = value.to_html(index=False, classes='styled-table')
        kpi_html += f'<div class="kpi-card"><h3>{key}</h3>{styled_table}</div>'
    kpi_html += "</div></body></html>"
    return kpi_html

@app.route('/')
def landing_page():
    return render_template_string("""
        <html>
            <head>
                <title>Welcome to the Dashboard</title>
                <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
                <style>
                    body {
                        font-family: 'Poppins', sans-serif;
                        background: linear-gradient(135deg, #ff7e5f, #feb47b);
                        color: #fff;
                        margin: 0;
                        padding: 0;
                        text-align: center;
                    }
                    h1 {
                        font-family: 'Roboto', sans-serif;
                        font-size: 3em;
                        margin-top: 100px;
                        color: #fff;
                        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
                    }
                    p {
                        font-size: 1.5em;
                        margin-top: 20px;
                        color: #fff;
                    }
                    ul {
                        list-style-type: none;
                        padding: 0;
                        margin-top: 30px;
                    }
                    li {
                        margin: 20px 0;
                    }
                    a {
                        font-size: 1.2em;
                        color: #fff;
                        background-color: #333;
                        padding: 15px 30px;
                        border-radius: 30px;
                        text-decoration: none;
                        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
                        transition: background-color 0.3s, transform 0.3s;
                    }
                    a:hover {
                        background-color: #feb47b;
                        transform: scale(1.05);
                    }
                    footer {
                        position: absolute;
                        bottom: 20px;
                        width: 100%;
                        font-size: 1em;
                        color: #fff;
                    }
                </style>
            </head>
            <body>
                <h1>Welcome to the Q&A of Greenflow</h1>
                <p>What question are you interested in?</p>
                <ul>
                    <li><a href="/table">What does the data look like?</a></li>
                    <li><a href="/companies-per-sector">What is the number of companies per sector?</a></li>
                    <li><a href="/plots">What is the distribution of the energy, water and CO2 consumption?</a></li>
                    <li><a href="/plot">What are the sectors which have a higher consumption of energy, water and CO2?</a></li>
                    <li><a href="/kpis">Companies with more and less usage of energy, water and CO2?</a></li>
                </ul>
                <footer>
                    <p>Created with 💻 by Beatriz Freitas for DataOps</p>
                </footer>
            </body>
        </html>
    """)


parquet_file_path = 'data/dados_sensores_5000.parquet'

# Load the CSV data at the start of the application
df = load_parquet(parquet_file_path)

def generate_table(df):
    return render_template_string('''
    <html><head><title>Data Table</title>
    <style>
        body { font-family: 'Poppins', sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); color: #333; padding: 20px; }
        h1 { text-align: center; color: #fff; margin-bottom: 30px; }
        .table-container { background: #fff; border-radius: 20px; padding: 40px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); width: 100%; max-width: 1200px; margin: 0 auto; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 1.4em; }
        th, td { border: 2px solid #ddd; padding: 25px; text-align: left; }
        th { background-color: #ff6f61; color: white; font-size: 1.5em; }
        td { background-color: #fdfdfd; }
        tr:nth-child(even) { background-color: #f7f7f7; }
        caption { caption-side: top; font-size: 1.8em; margin-bottom: 10px; font-weight: bold; }
    </style></head><body>
    <h1>Data Table</h1>
    <div class="table-container">{{ table | safe }}</div>
    </body></html>''', table=df.to_html(index=False, classes='table table-striped table-bordered', border=0))

@app.route('/plot')
def plot():
    plot_html = generate_plot(df)
    return render_template_string("""
        <html>
            <head>
                <title>Multiple Plots</title>
                <style>
                    body {
                        font-family: 'Poppins', sans-serif;
                        background-color: #f4f4f9;
                        color: #333;
                        text-align: center;
                    }
                    h1 {
                        color: #ff7e5f;
                        margin-top: 50px;
                    }
                    .plot-container {
                        display: flex;
                        flex-wrap: wrap;
                        justify-content: center;
                        gap: 40px;
                        margin-top: 30px;
                    }
                    .plot-container > div {
                        width: 45%;
                        margin-bottom: 20px;
                    }
                    footer {
                        position: absolute;
                        bottom: 20px;
                        width: 100%;
                        font-size: 1em;
                        color: #333;
                    }
                </style>
            </head>
            <body>
                <h1>What are the sectors which have a higher consumption of energy, water and CO2?</h1>
                <div class="plot-container">
                    {% for plot in plots_html %}
                        <div>{{ plot | safe }}</div>
                    {% endfor %}
            </body>
        </html>
    """, plots_html=plot_html)

@app.route('/plots')
def plots():
    plots_html = generate_plots(df)
    return render_template_string("""
        <html>
            <head>
                <title>Multiple Plots</title>
                <style>
                    body {
                        font-family: 'Poppins', sans-serif;
                        background-color: #f4f4f9;
                        color: #333;
                        text-align: center;
                    }
                    h1 {
                        color: #ff7e5f;
                        margin-top: 50px;
                    }
                    .plot-container {
                        display: flex;
                        flex-wrap: wrap;
                        justify-content: center;
                        gap: 40px;
                        margin-top: 30px;
                    }
                    .plot-container > div {
                        width: 45%;
                        margin-bottom: 20px;
                    }
                    footer {
                        position: absolute;
                        bottom: 20px;
                        width: 100%;
                        font-size: 1em;
                        color: #333;
                    }
                </style>
            </head>
            <body>
                <h1>Whats the distribution of the different categories?</h1>
                <div class="plot-container">
                    {% for plot in plots_html %}
                        <div>{{ plot | safe }}</div>
                    {% endfor %}
            </body>
        </html>
    """, plots_html=plots_html)

# New endpoint for KPIs
@app.route('/kpis')
def kpis():
    return generate_kpis(df)

# Define an endpoint to return the table
@app.route('/table')
def table():
    table_html = generate_table(df)
    return table_html

if __name__ == '__main__':
    app.run(debug = True)
