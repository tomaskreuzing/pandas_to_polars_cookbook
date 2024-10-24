# %%
import pandas as pd
import matplotlib.pyplot as plt
import polars as pl
import altair as alt

# Make the graphs a bit prettier, and bigger
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (15, 5)
plt.rcParams["font.family"] = "sans-serif"

# This is necessary to show lots of columns in pandas 0.12.
# Not necessary in pandas 0.13.
pd.set_option("display.width", 5000)
pd.set_option("display.max_columns", 60)

# %% Load the data
bikes = pd.read_csv(
    "../data/bikes.csv",
    sep=";",
    encoding="latin1",
    parse_dates=["Date"],
    dayfirst=True,
    index_col="Date",
)
bikes["Berri 1"].plot()
plt.show()


# TODO: Load the data using Polars
bikes = pl.read_csv(
    "../data/bikes.csv",
    has_header=True,  
    separator=";",    
    encoding="latin1", 
    try_parse_dates=True  
)

bikes.columns = [col.strip() for col in bikes.columns]

# Select the 'Date' and 'Berri 1' columns
bikes_filtered = bikes.select(["Date", "Berri 1"])

# Convert to NumPy arrays for plotting
dates = bikes_filtered["Date"].to_numpy()
berri_bikes = bikes_filtered["Berri 1"].to_numpy()

# Plot using Matplotlib
plt.figure(figsize=(15, 5))
plt.plot(dates, berri_bikes, label="Berri 1")
plt.xlabel("Date")
plt.legend()
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()  # Adjust layout for better fitting
plt.show()

# %% Plot Berri 1 data
# Next up, we're just going to look at the Berri bike path. Berri is a street in Montreal, with a pretty important bike path. I use it mostly on my way to the library now, but I used to take it to work sometimes when I worked in Old Montreal.

# So we're going to create a dataframe with just the Berri bikepath in it
berri_bikes = bikes[["Berri 1"]].copy()
berri_bikes[:5]

# TODO: Create a dataframe with just the Berri bikepath using Polars
# Hint: Use pl.DataFrame.select() and call the data frame pl_berri_bikes
berri_bikes = bikes.select(["Date", "Berri 1"])

# %% Add weekday column
# Next, we need to add a 'weekday' column. Firstly, we can get the weekday from the index. We haven't talked about indexes yet, but the index is what's on the left on the above dataframe, under 'Date'. It's basically all the days of the year.

berri_bikes.index

# You can see that actually some of the days are missing -- only 310 days of the year are actually there. Who knows why.

# Pandas has a bunch of really great time series functionality, so if we wanted to get the day of the month for each row, we could do it like this:
berri_bikes.index.day

# We actually want the weekday, though:
berri_bikes.index.weekday

# These are the days of the week, where 0 is Monday. I found out that 0 was Monday by checking on a calendar.

# Now that we know how to *get* the weekday, we can add it as a column in our dataframe like this:
berri_bikes.loc[:, "weekday"] = berri_bikes.index.weekday
berri_bikes[:5]

# TODO: Add a weekday column using Polars.
# Hint: Polars does not use an index.
berri_bikes = berri_bikes.with_columns(pl.col("Date").dt.weekday().alias("weekday"))

# %%
# Let's add up the cyclists by weekday
# This turns out to be really easy!

# Dataframes have a `.groupby()` method that is similar to SQL groupby, if you're familiar with that. I'm not going to explain more about it right now -- if you want to to know more, [the documentation](http://pandas.pydata.org/pandas-docs/stable/groupby.html) is really good.

# In this case, `berri_bikes.groupby('weekday').aggregate(sum)` means "Group the rows by weekday and then add up all the values with the same weekday".
weekday_counts = berri_bikes.groupby("weekday").aggregate(sum)
weekday_counts

# TODO: Group by weekday and sum using Polars
weekday_counts = (
    berri_bikes.group_by("weekday")
    .agg(pl.sum("Berri 1").alias("total_cyclists"))
)
print(weekday_counts)

# %% Rename index
weekday_counts.index = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

# TODO: Rename index using Polars, if possible.
weekday_names_dict = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday"
}
weekday_counts = weekday_counts.with_columns(
    pl.col("weekday").replace_strict(weekday_names_dict, default="unknown")  # Mapping with default
      .alias("weekday_name")
).select(["weekday_name", "total_cyclists"])

print(weekday_counts)

# %% Plot results
weekday_counts.plot(kind="bar")
plt.show()

# TODO: Plot results using Polars and matplotlib

chart = (
    alt.Chart(weekday_counts.to_pandas())
    .mark_bar()
    .encode(
        x=alt.X("weekday_name:O", title="Weekday"),
        y=alt.Y("total_cyclists:Q", title="Total Cyclists"),
        tooltip=["weekday_name", "total_cyclists"]
    )
    .properties(title="Total Cyclists by Weekday on Berri 1")
)

chart.display()
# %% Final message
print("Analysis complete!")