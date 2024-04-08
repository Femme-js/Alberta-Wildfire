# Import libs
from flask import Flask, config, render_template, request
import plotly
import plotly.express as px
import plotly.graph_objects as go
from keplergl import KeplerGl
import pandas as pd
import json
import numpy as np

# Setup Flask app
app = Flask(__name__, template_folder='/content/template')

#Open Data files
with open('./AB-Wildfires/Data/alberta_788.geojson', 'r') as f:
  boundaries = f.read()

with open('./AB-Wildfires/Data/fp-historical-wildfire-data-2006-2021(2)(1).csv', 'r') as f2:
  historical_fire = f2.read()

df = pd.read_csv("./AB-Wildfires/Data/fp-historical-wildfire-data-2006-2021(2)(1).csv")

#KeplerGL min config and setup layers
config = {
    'version': 'v1',
    'config': {
        'mapState': {
            'latitude': 54.1356608,
            'longitude': -112.6357456,
            'zoom': 4
        }
    }
}
map_1 = KeplerGl(config=config)
map_1.add_data(data=historical_fire, name='geojson_historical_fire')
map_1.add_data(data=boundaries, name='geojson_boundries')


# Flask Root page
@app.route("/")
def hello():
  return render_template('/kepler_load.html')

@app.route('/empty_map')
def empty_map():
    return map_1._repr_html_()

#Flask Year visualization
@app.route('/chart1')
def chart1():
    fig = go.Figure()
    fig.add_trace(go.Bar(x = np.sort(df.fire_year.unique()),
                    y = df['fire_year'].groupby([df.fire_year]).agg('count'),
                    name='Year of the wildfire',
                    marker_color='rgb(55, 83, 109)'
                    ))

    fig.update_layout(
        title='Wildfires per year from 2006 to 2021',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Count',
            titlefont_size=16,
            tickfont_size=14,
        ),
        xaxis=dict(
            title='Year',
            tickmode='linear'),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Wildfires per year"
    description = """
    We can visualize a downtrend in number of fires between the years 2006 and 2021.
    """
    return render_template('/notdash2.html', graphJSON=graphJSON, header=header,description=description)

#Flask size visualization
@app.route('/chart2')
def chart2():
    fig = px.pie(df['size_class'].groupby([df.size_class]).agg('count'), values='size_class', names=np.sort(df.size_class.unique()))
    fig.update_layout(
        title='Size class of the wildfire')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Size of Wildfires"
    description = """
    The size breakdown is as follows:
    A class = 0 to 0.1 ha
    B class > 0.1 ha to 4.0 ha
    C class > 4.0 ha to 40.0 ha
    D class > 40.0 ha to 200 ha
    E class > 200 ha
    """
    return render_template('/notdash2.html', graphJSON=graphJSON, header=header,description=description)

#Flask Origin visualization
@app.route('/chart3')
def chart3():
    fig = go.Figure()
    fig.add_trace(go.Bar(x = np.sort(df.general_cause_desc.unique()),
                y = df['general_cause_desc'].groupby([df.general_cause_desc]).agg('count'),
                name='Year of the wildfire',
                marker_color='rgb(55, 83, 109)'
                ))

    fig.update_layout(
    title='Cause of origin of Wildfires',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Count',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Cause of Origin"
    description = """
    We can see that the great moyority of Wildfires are caused by Lighting, follow by recreation (Camper, hunter) and residents.
    """
    return render_template('/notdash2.html', graphJSON=graphJSON, header=header,description=description)

#Flask Humidity visualization
@app.route('/chart4')
def chart4():
    fig = px.histogram(df, x='relative_humidity', nbins=20)
    fig.update_layout(
    title='Humidity at the start of Wildfire',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Count',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    )
  )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Humidity"
    description = """
    """
    return render_template('/notdash2.html', graphJSON=graphJSON, header=header,description=description)

#Flask Temperature visualization
@app.route('/chart5')
def chart5():
    fig = px.histogram(df, x='temperature', nbins=20)
    fig.update_layout(
    title='Temperature at the start of Wildfire',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Count',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    )
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Temperature"
    description = """
    """
    return render_template('/notdash2.html', graphJSON=graphJSON, header=header,description=description)

if __name__ == '__main__':
    app.run(port = port)