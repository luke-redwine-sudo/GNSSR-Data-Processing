import CustomGoogleMapPlotter
import pandas as pd

WeatherStationData = pd.read_csv(r"C:\Users\redwi\Downloads\WeatherStation_16.csv")
DroneGPSData = pd.read_csv(r"C:\Users\redwi\Downloads\Flight_GPS_data.csv")

day_adjust = 55
hour_adjust = -17
minute_adjust = -14
second_adjust = -57
grouping_tolerance = '200 milliseconds'
initial_zoom = 18
color_map = "GnBu"
dot_size = 1

# Correct Time of Day
WeatherStationData['AdjustedDateTime'] = pd.to_datetime(WeatherStationData['DateTime']) + pd.Timedelta(hours=hour_adjust, minutes=minute_adjust, seconds=second_adjust)

# Correct Date
WeatherStationData['AdjustedDateTime'] = WeatherStationData['AdjustedDateTime'] + pd.Timedelta(hours=day_adjust*24, minutes=0, seconds=0)

DroneGPSData['DATE'] = pd.to_datetime(DroneGPSData['DATE'])

# Switch Datetime to index
WeatherStationData.index = WeatherStationData['AdjustedDateTime']
DroneGPSData.index = DroneGPSData['DATE']

tol = pd.Timedelta(grouping_tolerance)

CorrelatedData = pd.merge_asof(left=WeatherStationData,right=DroneGPSData,right_index=True,left_index=True,direction='nearest',tolerance=tol)

CorrelatedData = CorrelatedData[(CorrelatedData['AdjustedDateTime'] >= '2023-07-08 07:17:06.516253') & (CorrelatedData['AdjustedDateTime'] < '2023-07-08 07:18:36.890021')]

gmap = CustomGoogleMapPlotter.CustomGoogleMapPlotter(CorrelatedData["LAT"].iloc[100], CorrelatedData["LON"].iloc[100], initial_zoom, map_type='satellite')
gmap.color_scatter(CorrelatedData["LAT"], CorrelatedData["LON"], CorrelatedData["Temperature"], colormap=color_map, size=dot_size)

gmap.draw("GNSSRDataMap.html")
