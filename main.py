import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Generating sample data (replace this with your dataset)
np.random.seed(0)
categories = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
values = np.random.randint(1, 10, size=len(categories))
df = pd.DataFrame({'Categories': categories, 'Values': values})


data = pd.read_csv(r"data/VehicleDataAnalysis.csv")
battery = pd.read_csv(r"data/Battery Data Analysis.csv")
heatData = pd.read_csv(r"data/HeatDataAnalysis.csv")



# Define the number of bins
num_bins = 3
num_bins_temp = 5
bin_labels = ["Low", "Medium", "Top"]
bin_labels_temp = ['Cool','Normal','High','Too High','Extreme']
data["Speed"] = pd.cut(data["Velocity [km/h]"], bins=num_bins, labels=bin_labels)
data["Torque"] = pd.cut(data["Motor Torque [Nm]"], bins=num_bins, labels=bin_labels)
battery['Battery_Temp_Cat'] = pd.cut(battery['Battery Temperature [�C]'], bins=num_bins_temp, labels=bin_labels_temp)


downsampled_bt = battery.sample(n=1000)
downsampled_dt = data.sample(n=1000)


# Create a Dash application
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Graph(
        id='radar-plot',
        figure={
            'data': [go.Scatterpolar(
                r=battery['SoC [%]'],
                theta=battery['Battery_Temp_Cat'],
                mode='lines',  # Change to 'markers' for marker points
                line=dict(color='blue', width=5),  # Customize line color and width
                fill='toself',  # Fill area inside radar chart
                name='Radar Plot'
            )],
            'layout': go.Layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 10])),  # Customize radial axis
                showlegend=True,
                title='Radar Plot'
            )
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(port=8060,debug=True)
