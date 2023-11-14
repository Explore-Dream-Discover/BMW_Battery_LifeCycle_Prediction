import plotly.express as px
import dash
import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv("data\VehicleDataAnalysis.csv")

# Calculate the moving average using a rolling window
window_size = 3  # Adjust window size as needed
data['velocity_smoothed'] = data['Velocity [km/h]'].rolling(window=window_size, min_periods=1).mean()

# Plot original and smoothed data
plt.figure(figsize=(8, 6))


# Bar plot for original data
#plt.scatter(data['Time [s]'], data['Velocity [km/h]'], alpha=0.5, color='blue', label='Original Data')

# Bar plot for smoothed data
#plt.plot(data['Time [s]'], data['Velocity [km/h]'])#, alpha=0.002, color='orange', label='Smoothed Data')
# Plot histogram of smoothed data
# plt.hist(data['Velocity [km/h]'], bins=10, alpha=0.7, color='orange', label='Smoothed Data')
# Bar plot for smoothed data
plt.bar(data['Time [s]'], data['velocity_smoothed'], alpha=0.7, color='orange', label='Smoothed Data')





plt.show()









# # Create a line plot using Plotly
# fig = px.line(data, x='Time [s]', y='Velocity [km/h]', title='Time vs Velocity')

# # Show the plot
# fig.show()