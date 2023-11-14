import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import os
print(os.getcwd())


data =pd.read_csv(r"data/VehicleDataAnalysis.csv")
print(data.columns)

# Perform equal width binning
# Define the number of bins
num_bins = 3
bin_labels = ['Low', 'Medium', 'Top']
data["Speed"] = pd.cut(data['Velocity [km/h]'], bins=num_bins, labels=bin_labels)
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
 
server=app.server
img = r"assets\data-collection.png"
img1 = r"assets\channels.png"
img2 = r'assets\vehicle ran time.jpg'
img3 = r'assets\voltage.gif'
img4 = r'assets\current.png'
img5 = r'assets\throttle.png'
img6 = r'assets\brake.png'





##############KPI##################################
# Define the content of the KPI card with an online image
kpi_card_no_of_samples = dbc.Card(
    dbc.CardBody(
        [
            dbc.CardImg(src=img, style={"width": "100px", "height": "100px"}),
            html.H4('No of samples', className="card-title"),
            html.P(f"{len(data)}", className="card-text"),
        ]
    ),)





kpi_card_vehicle_RanTime = dbc.Card(
    dbc.CardBody(
        [
            dbc.CardImg(src=img2, style={"width": "100px", "height": "100px"}),
            html.H4('vehicle ran time', className="card-title"),
            html.P("{:.2f}".format(data['Time [s]'].max()/ 3600), className="card-text"),
        ]
    ),),





# Define the content of the KPI card with an online image
kpi_card_no_of_channels = dbc.Card(
    dbc.CardBody(
        [
            dbc.CardImg(src=img1, style={"width": "100px", "height": "100px"}),
            html.H4('No of Channels', className="card-title"),
            #Hard coding column names
            html.P( f"{48}", className="card-text"),
        ]
    ),),




kpi_card_no_of_max_volt = dbc.Card(
    dbc.CardBody(
        [
            dbc.CardImg(src=img3, style={"width": "100px", "height": "100px"}),
            html.H4('Max Elevation', className="card-title"),
            html.P("{:.2f}".format(max(data['Elevation [m]'].unique())), className="card-text"),
        ]
    ),)
    


kpi_card_no_of_max_speed = dbc.Card(
    dbc.CardBody(
        [
            dbc.CardImg(src=img6, style={"width": "100px", "height": "100px"}),
            html.H4('Regenerative Braking Signal', className="card-title"),
            html.P("{:.2f}".format(max(data['Regenerative Braking Signal '].unique())), className="card-text"),
        ]
    ),)



cards = dbc.Container(
    [
        dbc.Row([dbc.Col(kpi_card_no_of_samples),
                 dbc.Col(kpi_card_no_of_channels),
                 dbc.Col(kpi_card_vehicle_RanTime),
                 dbc.Col(kpi_card_no_of_max_volt),
                 dbc.Col(kpi_card_no_of_max_speed)]),  # Adjust the width as needed
        
    ],
    fluid=True,
)
##############KPI##################################



########Gauge
# Create custom gauge component (e.g., using Plotly)
def create_gauge(value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge = {
        'axis': {'range': [None, 500], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 250], 'color': 'cyan'},
            {'range': [250, 400], 'color': 'royalblue'}],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 490}}
    ))
    fig.update_layout(height=250) 
    return fig

def create_gauge_speed(value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge = {
        'axis': {'range': [None, 200], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 100], 'color': 'cyan'},
            {'range': [100, 200], 'color': 'royalblue'}],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 200}}
    ))
    fig.update_layout(height=250)
    return fig


Analog_plots =dbc.Container([
    dbc.Row([
             
             dbc.Col(dcc.Graph(id='gauge1', figure=create_gauge_speed(max(data['Velocity [km/h]'].unique()), "Vehicle Top Speed"))),
            dbc.Col(dcc.Graph(id='gauge2', figure=create_gauge(max(data['Motor Torque [Nm]'].unique()), "Maximum Motor Torque"))),
            dbc.Col(dcc.Graph(id='gauge3', figure=create_gauge(max(data['Throttle [%]'].unique()), "Throttle"))),
    
   
            
            
            ])
])






app.layout = html.Div([#title
                        html.H1('BATTERY  HEATING DATA IN REAL DRIVING CYCLES', className='dashboard-title'),
                        html.Div(cards,style={'display': 'flex','backgroundColor': 'lightblue', 'padding': '10px'}),
                        html.Div(html.H3('1.Vehicle Speed Analysis')),
                        html.Div(Analog_plots,style={'display': 'flex','backgroundColor': 'lightblue', 'padding': '10px'}),
                        # html.Div(html.H3('2.Battery Current and Voltage Analysis')),
                        # html.Div(Bullet_plots,style={'display': 'flex','backgroundColor': 'lightblue', 'padding': '10px'}),
                        # html.H3("3.Time vs. Temperature"),
                        # html.Div(temp_plot_container,style={'display': 'flex','backgroundColor': 'lightblue', 'padding': '10px'}),
                        # html.H3("4.Time vs. Other"),
                        # html.Div(TimeVsOther,style={'display': 'flex','backgroundColor': 'lightblue', 'padding': '10px'}),
                        # html.H3("5.Funnel Chart"),
                        # html.Div(line_plot7,style={'display': 'flex','backgroundColor': 'lightblue', 'padding': '10px'}),

                      ])

if __name__ == '__main__':
    # Get the HTML content of the Dash app
    

    app.run_server(debug=True)
