from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd
import numpy as np

app = Flask(__name__)

def load_data():
    df = px.data.gapminder()
    # preprocess data ...
    return df


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graphs')
def view_graphs():
    return render_template('graphs.html')

@app.route('/analysis', methods=['GET', 'POST'])
def view_analysis1():
    df = load_data()
    country = 'India'
    if request.method == 'POST':
        country = request.form['ctry']
    cdf = df.query('country == @country').copy()
    countries = df['country'].unique()
    if cdf.shape[0] == 0: 
        print('No data for country: {}'.format(country))
    else:
        fig = px.bar(cdf, x="year", y="pop")
        fig2 = px.line(cdf, x="year", y="lifeExp")
        fig3 = px.scatter(cdf, x="gdpPercap", y="lifeExp")
        return render_template('analysis.html', 
                                figure1=fig.to_html(),
                                figure2=fig2.to_html(),
                                figure3=fig3.to_html(),
                                country=country,
                                countries=countries)
    return render_template('analysis.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)



 