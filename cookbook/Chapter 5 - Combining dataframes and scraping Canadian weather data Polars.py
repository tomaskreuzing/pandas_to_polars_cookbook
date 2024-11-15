# %%
import polars as pl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pathlib import Path
path = Path(__file__).parent.parent / "data" / "weather_2012.csv"

plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (15, 3)
plt.rcParams["font.family"] = "sans-serif"


# %%
#altair cant handle this many rows, need seaborn 
pl_weather_2012_final = pl.read_csv(path, try_parse_dates=True)
#datetime column in correct format now
sns.lineplot(data=pl_weather_2012_final, x="date_time", y="temperature_c")
#hig var winter months high temps summer months
# TODO: rewrite using Polars

# %%
# Okay, let's start from the beginning.
# We're going to get the data for March 2012, and clean it up

url_template = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=5415&Year={year}&Month={month}&timeframe=1&submit=Download+Data"

year = 2012
month = 3
url_march = url_template.format(month=3, year=2012)
pl_weather_mar2012 = pl.read_csv(
    url_march,
    try_parse_dates=True,
    encoding="latin1",
    null_values= ""
)
pl_weather_mar2012.head()
# TODO: rewrite using Polars. Polars can handle URLs similarly.

# %%
null_columns = [
    col for col in pl_weather_mar2012.columns
    if pl_weather_mar2012[col].null_count() > 0
]
pl_weather_mar2012 = pl_weather_mar2012.drop(null_columns)
print(pl_weather_mar2012)
#pl_weather_mar2012[col] accesses data within that particular column
# TODO: rewrite using Polars

# %%
# Let's get rid of columns that we do not need.
# For example, the year, month, day, time columns are redundant (we have Date/Time (LST) column).
# Let's get rid of those. The `axis=1` argument means "Drop columns", like before. The default for operations like `dropna` and `drop` is always to operate on rows.
pl_weather_mar2012 = pl_weather_mar2012.drop(["Year", "Month", "Day", "Time (LST)"])
pl_weather_mar2012.head()
# TODO: redo this using polars

# %%
# When you look at the data frame, you see that some column names have some weird characters in them.
# Let's clean this up, too.
# Let's print the column names first:
pl_weather_mar2012.columns
# %%
pl_weather_mar2012 = pl_weather_mar2012.rename(
    lambda col: col.replace('ï»¿"', '')
)
pl_weather_mar2012 = pl_weather_mar2012.rename(
    lambda col: col.replace('"', '')
)
pl_weather_mar2012 = pl_weather_mar2012.rename(
    lambda col: col.replace('Â', '')
)
pl_weather_mar2012.columns
# TODO: rewrite using Polars

# %%
# Optionally, you can also rename columns more manually for specific cases:
pl_weather_mar2012 = pl_weather_mar2012.rename(
    {
        "Longitude (x)": "Longitude",
        "Latitude (y)": "Latitude",
        "Station Name": "Station_Name",
        "Climate ID": "Climate_ID",
        "Temp (°C)": "Temperature_C",
        "Dew Point Temp (°C)": "Dew_Point_Temp_C",
        "Rel Hum (%)": "Relative_Humidity",
        "Wind Spd (km/h)": "Wind_Speed_kmh",
        "Visibility (km)": "Visibility_km",
        "Stn Press (kPa)": "Station_Pressure_kPa",
        "Weather": "Weather",
    }
)
# Check the new column names
print(pl_weather_mar2012.columns)

# %%
pl_weather_mar2012.columns = [
    col.lower() for col in pl_weather_mar2012.columns 
]
print(pl_weather_mar2012.columns)
#making all column name characters lowercase
# TODO: redo this using polars

# %%
# Notice how it goes up to 25° C in the middle there? That was a big deal. It was March, and people were wearing shorts outside.
pl_weather_mar2012.plot.line(x="date/time (lst)", y="temperature_c")
# TODO: redo this using polars

# %%
# This one's just for fun -- we've already done this before, using groupby and aggregate! We will learn whether or not it gets colder at night. Well, obviously. But let's do it anyway.
pl_daily_temperatures = pl_weather_mar2012.select(["date/time (lst)","temperature_c"])
pl_daily_temperatures = pl_daily_temperatures.with_columns(
    pl.col("date/time (lst)").dt.hour().alias("hour")
)
pl_daily_temperatures = pl_daily_temperatures.group_by("hour").agg(
    pl.col("temperature_c").median().alias("median_temperature")
)
pl_daily_temperatures.sort("hour")
pl_daily_temperatures.plot.line(x="hour", y="median_temperature")
#it looks like the time with the highest median temperature is 14 o clock
# TODO: redo this using polars

null_columns = [
    col for col in pl_weather_mar2012.columns
    if pl_weather_mar2012[col].null_count() > 0
]
pl_weather_mar2012 = pl_weather_mar2012.drop(null_columns)


#%%
# Okay, so what if we want the data for the whole year? Ideally the API would just let us download that, but I couldn't figure out a way to do that.
# First, let's put our work from above into a function that gets the weather for a given month.
def clean_data(data):
    null_columns = [
    col for col in data.columns
    if data[col].null_count() > 0
    ]
    data = data.drop(null_columns)
    data = data.drop(["Year", "Month", "Day", "Time (LST)"])
    data = data.rename(
    lambda col: col.replace('ï»¿"', '')
    )
    data = data.rename(
    lambda col: col.replace('"', '')
    )
    data = data.rename(
    lambda col: col.replace('Â', '')
    )
    data = data.rename({
            "Longitude (x)": "Longitude",
            "Latitude (y)": "Latitude",
            "Station Name": "Station_Name",
            "Climate ID": "Climate_ID",
            "Temp (°C)": "Temperature_C",
            "Dew Point Temp (°C)": "Dew_Point_Temp_C",
            "Rel Hum (%)": "Relative_Humidity",
            "Wind Spd (km/h)": "Wind_Speed_kmh",
            "Visibility (km)": "Visibility_km",
            "Stn Press (kPa)": "Station_Pressure_kPa",
            "Weather": "Weather",
        }
    )
    data.columns = [
    col.lower() for col in data.columns 
    ]
    return data

year = 2012
month = 3
url_march = url_template.format(month=3, year=2012)
pl_weather_mar2012 = pl.read_csv(
    url_march,
    try_parse_dates=True,
    encoding="latin1",
    null_values= ""
)
pl_weather_mar2012.head()

def download_weather_month(year, month):
    url_template = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=5415&Year={year}&Month={month}&timeframe=1&submit=Download+Data"
    url = url_template.format(year=year, month=month)
    weather_data = pl.read_csv(
        url_march,
        try_parse_dates=True,
        encoding="latin1",
        null_values= ""
    )
    weather_data_clean = clean_data(weather_data)
    return weather_data_clean
# TODO: redefine these functions using polars and your code above

# %%
download_weather_month(2012, 1).head(5)
#actually works and provides output as required
#function arguably not pretty but it does the job

# %%
# Now, let's use a list comprehension to download all our data and then just concatenate these data frames
# This might take a while
data_by_month = [download_weather_month(2012, i) for i in range(1, 13)]
pl_weather_2012 = pl.concat(data_by_month)
pl_weather_2012.head()
# TODO: do the same with polars
# %%
pl_weather_2012

# %%
# Now, let's save the data.
pl_weather_2012.write_csv(path)
# TODO: use polars to save the data.