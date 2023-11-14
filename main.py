import plotly.express as px
import dash
import pandas as pd
data = pd.read_csv("data\Vehicle_data.csv")
print(data)
# Create a line plot using Plotly
# fig = px.line(data, x='Time [s]', y='Throttle [%]', title='Time vs Velocity')

# # Show the plot
# fig.show()
