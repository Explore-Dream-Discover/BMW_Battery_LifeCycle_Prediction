import plotly.express as px
import pandas as pd
df = px.data.wind()


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
mean_value=battery['SoC [%]'].mean() 
battery['SoC [%]'].fillna(mean_value, inplace=True) 

print((battery['SoC [%]'].value_counts()))




fig = px.scatter_polar( r=battery['SoC [%]'], theta=battery['Battery_Temp_Cat'],
                       color=battery['Battery_Temp_Cat'], symbol=data['Regenerative Braking Signal '], size=battery['SoC [%]'],
                       color_discrete_sequence=px.colors.sequential.Aggrnyl)
fig.show()