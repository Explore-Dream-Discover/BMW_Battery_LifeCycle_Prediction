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

print(battery.columns)
downsampled_bt = battery.sample(n=1000)
downsampled_dt = data.sample(n=1000)
print(data["Speed"].value_counts())
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server
img = r"assets\data-collection.png"
img1 = r"assets\channels.png"
img2 = r"assets\vehicle ran time.jpg"
img3 = r"assets\voltage.gif"
img4 = r"assets\current.png"
img5 = r"assets\throttle.png"
img6 = r"assets\brake.png"


##############KPI##################################
# Define the content of the KPI card with an online image
kpi_card_no_of_samples = dbc.Card(
    dbc.CardBody(
        [
            dbc.CardImg(src=img, style={"width": "100px", "height": "100px"}),
            html.H4("No of samples", className="card-title"),
            html.P(f"{len(data)}", className="card-text"),
        ]
    ),
)


kpi_card_vehicle_RanTime = (
    dbc.Card(
        dbc.CardBody(
            [
                dbc.CardImg(src=img2, style={"width": "100px", "height": "100px"}),
                html.H4("vehicle ran time", className="card-title"),
                html.P(
                    "{:.2f}".format(data["Time [s]"].max() / 3600),
                    className="card-text",
                ),
            ]
        ),
    ),
)


# Define the content of the KPI card with an online image
kpi_card_no_of_channels = (
    dbc.Card(
        dbc.CardBody(
            [
                dbc.CardImg(src=img1, style={"width": "100px", "height": "100px"}),
                html.H4("No of Channels", className="card-title"),
                # Hard coding column names
                html.P(f"{48}", className="card-text"),
            ]
        ),
    ),
)


kpi_card_no_of_max_volt = dbc.Card(
    dbc.CardBody(
        [
            dbc.CardImg(src=img3, style={"width": "100px", "height": "100px"}),
            html.H4("Max Elevation", className="card-title"),
            html.P(
                "{:.2f}".format(max(data["Elevation [m]"].value_counts())),
                className="card-text",
            ),
        ]
    ),
)


kpi_card_no_of_max_speed = dbc.Card(
    dbc.CardBody(
        [
            dbc.CardImg(src=img6, style={"width": "100px", "height": "100px"}),
            html.H4(" Regen Braking Active", className="card-title"),
            html.P(
                "{:.2f}".format((data["Regenerative Braking Signal "] == 1).sum()),
                className="card-text",
            ),
        ]
    ),
)


cards = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(kpi_card_no_of_samples),
                dbc.Col(kpi_card_no_of_channels),
                dbc.Col(kpi_card_vehicle_RanTime),
                dbc.Col(kpi_card_no_of_max_volt),
                dbc.Col(kpi_card_no_of_max_speed),
            ]
        ),  # Adjust the width as needed
    ],
    fluid=True,
)
##############KPI##################################


########Gauge
# Create custom gauge component (e.g., using Plotly)
def create_gauge(value, title):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            gauge={
                "axis": {"range": [None, 500], "tickwidth": 1, "tickcolor": "darkblue"},
                "bar": {"color": "darkblue"},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "gray",
                "steps": [
                    {"range": [0, 250], "color": "cyan"},
                    {"range": [250, 400], "color": "royalblue"},
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 490,
                },
            },
        )
    )
    fig.update_layout(height=250)
    return fig


def create_gauge_speed(value, title):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            gauge={
                "axis": {"range": [None, 200], "tickwidth": 1, "tickcolor": "darkblue"},
                "bar": {"color": "darkblue"},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "gray",
                "steps": [
                    {"range": [0, 100], "color": "cyan"},
                    {"range": [100, 200], "color": "royalblue"},
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 200,
                },
            },
        )
    )
    fig.update_layout(height=250)
    return fig


Analog_plots = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="gauge1",
                        figure=create_gauge_speed(
                            max(data["Velocity [km/h]"].unique()), "Vehicle Top Speed"
                        ),
                    )
                ),
                dbc.Col(
                    dcc.Graph(
                        id="gauge2",
                        figure=create_gauge(
                            max(data["Motor Torque [Nm]"].unique()),
                            "Maximum Motor Torque",
                        ),
                    )
                ),
                dbc.Col(
                    dcc.Graph(
                        id="gauge3",
                        figure=create_gauge(
                            max(data["Throttle [%]"].unique()), "Throttle"
                        ),
                    )
                ),
            ]
        )
    ]
)


# Create histogram traces
trace1 = go.Histogram(x=data["Velocity [km/h]"], name="Speed", opacity=0.75, nbinsx=20)
trace2 = go.Histogram(
    x=data["Motor Torque [Nm]"], name="Motor Torque", opacity=0.75, nbinsx=30
)
trace3 = go.Histogram(
    x=data["Elevation [m]"], name="Elevation", opacity=0.75, nbinsx=30
)


# Create a scatter plot
#  chart trace
# Callback to update the line plot based on slider value
@app.callback(
    Output("torque-time-graph", "figure"),
    Output("Longitude_acceleration-time-graph", "figure"),
    [Input("category-slider", "value")],
)
def update_figure(selected_category_index):
    selected_category = data["Speed"].unique()[selected_category_index]
    filtered_data = data[data["Speed"] == selected_category]

    fig = px.scatter(
        filtered_data,
        x="Throttle [%]",
        y="Motor Torque [Nm]",
        title=f"Torque vs Time at Category: {selected_category}",
    )
    fig1 = px.scatter(
        filtered_data,
        x="Throttle [%]",
        y="Longitudinal Acceleration [m/s^2]",
        title=f"Torque vs Time at Category: {selected_category}",
    )

    fig.update_layout(height=400, width=800)
    fig1.update_layout(height=400, width=800)
    return fig, fig1


# Create a figure with subplots in a row
# Create figures for each histogram
fig1 = go.Figure(data=[trace1])
fig1.update_layout(
    title="Speed Distribution", xaxis_title="Speed", yaxis_title="Frequency"
),

fig2 = go.Figure(data=[trace2])
fig2.update_layout(
    title="Torque Distribution", xaxis_title="Torque", yaxis_title="Frequency"
),


fig3 = go.Figure(data=[trace3])
fig3.update_layout(title="Elevation", xaxis_title="Elevation", yaxis_title="Frequency"),


histogram_plots = dbc.Container(
    [
        dbc.Row(
            [
                dcc.Graph(
                    id="speed-histogram-1",
                    figure=fig1,
                    style={"width": "33%", "display": "inline-block"},
                ),
                dcc.Graph(
                    id="speed-histogram-2",
                    figure=fig2,
                    style={"width": "33%", "display": "inline-block"},
                ),
                dcc.Graph(
                    id="speed-histogram-3",
                    figure=fig3,
                    style={"width": "33%", "display": "inline-block"},
                ),
            ]
        )
    ]
)


pie_plots = dbc.Container(
    [
        dbc.Row(
            [
                html.H1("Throttle Response"),
                dcc.Slider(
                    id="category-slider",
                    min=0,
                    max=len(data["Speed"].unique()) - 1,
                    value=0,
                    marks={i: cat for i, cat in enumerate(data["Speed"].unique())},
                    step=1,
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="torque-time-graph",
                            config={"displayModeBar": False},  # Hide the plotly toolbar
                            style={"width": "38%", "display": "inline-block"},
                        ),
                        dcc.Graph(
                            id="Longitude_acceleration-time-graph",
                            config={"displayModeBar": False},  # Hide the plotly toolbar
                            style={"width": "38%", "display": "inline-block"},
                        ),
                    ]
                ),
            ]
        )
    ]
)




twoD_histogram_plots =dbc.Container([
    dbc.Row([
             
             dbc.Col(dcc.Graph(
        id='2d-histogram12',
        figure=px.density_heatmap(x=data['Motor Torque [Nm]'], y=data['Elevation [m]'], nbinsx=20, nbinsy=20))),
        dbc.Col( dcc.Graph(id='histogram',
                           figure=px.histogram(x=data['Motor Torque [Nm]'], nbins=30)  ))
    ]),])
#


# figure.update_layout(title='2D Histogram', xaxis_title='X Axis', yaxis_title='Y Axis', height=400, width=500),
#         dbc.Col( dcc.Graph(id='histogram',
#                            figure=px.histogram(x=data['Motor Torque [Nm]'], nbins=30)  ))
#     ]),])


curr_vs_Volt =dbc.Container([
    dbc.Row([
             dbc.Col(    dcc.Graph(
        id='bar-plot',
        figure={
            'data': [go.Bar(
                x=downsampled_bt['Battery Voltage [V]'],
                y=downsampled_bt['Battery Current [A]'],
                marker=dict(color='blue'),  # Set color of bars as needed
                name='Bar Plot (Current vs. Voltage)',base=0
            )],
            'layout': go.Layout(
                xaxis={'title': 'Voltage (V)'},
                yaxis={'title': 'Current (A)'},
                title='Current Vs Volatge Distribution'
            )
        }
    )),

    ])
])

print(downsampled_bt.columns,"*"*40)
radar_speed_volt =dbc.Container([
    dbc.Row([
             dbc.Col(dcc.Graph(id = "radar-plot",
                figure={
            'data': [go.Barpolar(
                r=downsampled_bt['Battery Voltage [V]'],
                theta=downsampled_dt['Speed'],
                marker_color='blue',  # Customize marker color
                name='Temperature vs. Velocity Bar Polar Plot'
            )],
            'layout': go.Layout(
                polar=dict(radialaxis=dict(title='Velocity')),
                title='Temperature vs. Velocity Bar Polar Plot'
            )
        }))
    ])
])



radar_soc_tmp =dbc.Container([
    dbc.Row([
             dbc.Col(dcc.Graph(
        id='pie-chart',
        figure={
            'data': [go.Pie(labels=downsampled_bt['Battery_Temp_Cat'], values=downsampled_bt['Battery Temperature [�C]'])],
            'layout': {
                'title': 'Battery Temperature'
            }
        }
             ))
])

            
    ])
                 
                 
                 
                 
   




                
    





sunburst_soc_tmp =dbc.Container([
    dbc.Row([
             dbc.Col(dcc.Graph(id = "sunburst-plot",
                              figure={'data': [go.Bar(
                                                            x=downsampled_dt["Time [s]"],
                                                            y=downsampled_bt['SoC [%]'],
                                                            # mode='lines+markers',
                                                            name='SOC'
                                                        )
                                                ],
                                        'layout': {
                                            'title': 'Time vs SOC[State Of Discharge]',
                                            'xaxis': {'title': 'Time'},
                                            'yaxis': {'title': 'SOC'}
                                        },
        }
          
           
        
    ))])
    ])

        
    

    




# heatmapFRcrVsvt = dbc.Container([
#     dbc.Row([
#              dbc.Col(    dcc.Graph(
#         id='bar-plot',
#         figure={
           
#             'data': [px.density_heatmap(
#                 x=downsampled_df['Battery Voltage [V]'],y=downsampled_df['Battery Current [A]'],
#                 name='Bar Plot (Current vs. Voltage)'
#             )],
#             'layout': go.Layout(
#                 xaxis={'title': 'Voltage (V)'},
#                 yaxis={'title': 'Current (A)'},
#                 title='Current Vs Volatge Distribution'
#             )
#         }
#     ))
#     ])
# ])


app.layout = html.Div(
    [  # title
        html.H1(
            "BATTERY  HEATING DATA IN REAL DRIVING CYCLES", className="dashboard-title"
        ),
        html.Div(
            cards,
            style={
                "display": "flex",
                "backgroundColor": "lightblue",
                "padding": "35px",
            },
        ),
        html.Div(html.H3("1.Vehicle Data Analysis")),
        html.Div(
            Analog_plots,
            style={
                "display": "flex",
                "backgroundColor": "lightblue",
                "padding": "35px",
            },
        ),
        html.Div(html.H3("2.Histogram plots for Vehicle data")),
        html.Div(
            histogram_plots,
            style={
                "display": "flex",
                "backgroundColor": "lightblue",
                "padding": "45px",
            },
        ),
        html.Div(html.H3("3.Scatter plots for Vehicle data")),
        html.Div(
            pie_plots,
            style={
                "display": "flex",
                "backgroundColor": "lightblue",
                "padding": "35px",
            },
        ),
        html.Div(html.H3("4.Density Heat map Vs histogram for Torque Distribution")),
        html.Div(
            twoD_histogram_plots,
            style={
                "display": "flex",
                "backgroundColor": "lightblue",
                "padding": "35px",
            },
        ),
        # html.Div(html.H3("5.Battery Data analysis")),
        #         html.Div(
        #     [curr_vs_Volt,
        #     radar_speed_volt],
            
        #     style={
        #         "display": "flex",
        #         "backgroundColor": "lightblue",
        #         "padding": "35px",
        #     },),

       
        # html.Div(
        #     [radar_soc_tmp,sunburst_soc_tmp],
            
        #     style={
        #         "display": "flex",
        #         "backgroundColor": "lightblue",
        #         "padding": "35px",
        #     },)    







        # # html.Div(Bullet_plots,style={'display': 'flex','backgroundColor': 'lightblue', 'padding': '10px'}),
        # html.H3("3.Time vs. Temperature"),
        # html.Div(temp_plot_container,style={'display': 'flex','backgroundColor': 'lightblue', 'padding': '10px'}),
        # html.H3("4.Time vs. Other"),
        # html.Div(TimeVsOther,style={'display': 'flex','backgroundColor': 'lightblue', 'padding': '10px'}),
        # html.H3("5.Funnel Chart"),
        # html.Div(line_plot7,style={'display': 'flex','backgroundColor': 'lightblue', 'padding': '10px'}),
    ]
)

if __name__ == "__main__":
    # Get the HTML content of the Dash app

    app.run_server(debug=True)
