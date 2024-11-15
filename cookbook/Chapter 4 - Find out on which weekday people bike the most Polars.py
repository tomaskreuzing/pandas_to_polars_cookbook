# %%
import pandas as pd
import polars as pl
import datetime as dt
import matplotlib.pyplot as plt
from pathlib import Path
path = Path(__file__).parent.parent / "data" / "bikes.csv"

# Make the graphs a bit prettier, and bigger
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (15, 5)
plt.rcParams["font.family"] = "sans-serif"

# This is necessary to show lots of columns in pandas 0.12.
# Not necessary in pandas 0.13.
pd.set_option("display.width", 5000)
pd.set_option("display.max_columns", 60)

# %% Load the data
pl_bikes = pl.read_csv(
    path,
    separator=";",
    encoding="latin1",
    try_parse_dates=True,
)
pl_bikes.select(["Date","Berri 1"]).plot.line(x="Date", y="Berri 1")

# TODO: Load the data using Polars

# %% Plot Berri 1 data
# Next up, we're just going to look at the Berri bike path. Berri is a street in Montreal, with a pretty important bike path. I use it mostly on my way to the library now, but I used to take it to work sometimes when I worked in Old Montreal.
# So we're going to create a dataframe with just the Berri bikepath in it
pl_berri_bikes = pl_bikes.select(["Date","Berri 1"])
pl_berri_bikes.head(5)

# TODO: Create a dataframe with just the Berri bikepath using Polars

# %% Add weekday column
# Next, we need to add a 'weekday' column. Firstly, we can get the weekday from the index. We haven't talked about indexes yet, but the index is what's on the left on the above dataframe, under 'Date'. It's basically all the days of the year.

pl_berri_bikes = pl_berri_bikes.with_columns(
    (pl.col("Date").dt.weekday().alias("weekday"))
)
print(pl_berri_bikes)
#sunday is 7, monday is 1
#first day of 2012 indeed sunday

# TODO: Add a weekday column using Polars.

# %%
# Let's add up the cyclists by weekday
# This turns out to be really easy!
# Dataframes have a `.groupby()` method that is similar to SQL groupby, if you're familiar with that. I'm not going to explain more about it right now -- if you want to to know more, [the documentation](http://pandas.pydata.org/pandas-docs/stable/groupby.html) is really good.
pl_weekday_counts = pl_berri_bikes.group_by("weekday").sum().sort(by="Berri 1", descending=True)
print(pl_weekday_counts)
#thursday has the most people 

# TODO: Group by weekday and sum using Polars
# %%
weekdays = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday",
}
pl_weekday_counts = pl_weekday_counts.with_columns(
    pl.col("weekday").replace_strict(weekdays).alias("weekday_renamed")
)
print(pl_weekday_counts)
#more efficient than regular map elements process
#creating a separate column just in case
# TODO: Rename index using Polars, if possible.


# %% Plot results
pl_weekday_counts.plot.bar(x="weekday_renamed", y="Berri 1")
# TODO: Plot results using Polars and matplotlib

# %% Final message
print("Analysis complete!")