import plotly.graph_objects as go
import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px



data = pd.read_csv(r"data/VehicleDataAnalysis.csv")
battery = pd.read_csv(r"data/Battery Data Analysis.csv")
heatData = pd.read_csv(r"data/HeatDataAnalysis.csv")

print(battery.columns)
print(("*" * 50))
print((data["Regenerative Braking Signal "] == 1).sum())

# Perform equal width binning
# Define the number of bins
num_bins = 3
num_bins_temp = 5
bin_labels_temp = ['Cool','Normal','High','Too High','Extreme']
bin_labels = ["Low", "Medium", "Top"]
data["Speed"] = pd.cut(data["Velocity [km/h]"], bins=num_bins, labels=bin_labels)
data["Torque"] = pd.cut(data["Motor Torque [Nm]"], bins=num_bins, labels=bin_labels)
battery['Battery_Temp_Cat'] = pd.cut(battery['Battery Temperature [�C]'], bins=num_bins_temp, labels=bin_labels_temp)
mean_value=battery['SoC [%]'].mean() 
battery['SoC [%]'].fillna(mean_value, inplace=True) 


# Map speed categories to different symbols
speed_to_symbol = {'Low': 'circle', 'Medium': 'square', 'Top': 'diamond'}
# Create the Symbol column based on the Speed column
data['Symbol'] = data['Speed'].map(speed_to_symbol)

downsampled_bt = battery.sample(n=1000)
downsampled_dt = data.sample(n=1000)








# Create the scatter plot using Plotly Express
fig = px.scatter( x=downsampled_bt['Battery Temperature [�C]'], y=downsampled_bt['SoC [%]'], color=downsampled_bt['Battery_Temp_Cat'], symbol=downsampled_dt['Symbol'],
                 title='Categorical vs. Continuous Scatter Plot with Symbols based on Speed',
                 labels={'X': 'X-axis', 'Y': 'Y-axis'})

# Dash app layout
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Categorical vs. Continuous Scatter Plot with Symbols based on Speed Example"),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)