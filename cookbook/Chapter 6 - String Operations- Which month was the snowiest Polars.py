# %%
import polars as pl
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import seaborn as sns
path = Path(__file__).parent.parent / "data" / "weather_2012_processed.csv"

plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (15, 3)
plt.rcParams["font.family"] = "sans-serif"


# %%
# We saw earlier that pandas is really good at dealing with dates. It is also amazing with strings! We're going to go back to our weather data from Chapter 5, here.
pl_weather_2012 = pl.read_csv(
    path, try_parse_dates=True
)
pl_weather_2012

# TODO: load the data using polars and call the data frame pl_wather_2012
#%%
#we want to keep all observations to plot for times within which it had snowed
pl_weather_description = pl_weather_2012.with_columns(
    is_snowing=pl.col("weather").str.contains("Snow")
)
pl_weather_description
#%%
# Let's plot when it snowed and when it did not:
sns.lineplot(data=pl_weather_description.to_pandas(), x="date/time (lst)", y="is_snowing")
# TODO: do the same with polars

# %%
# If we wanted the median temperature each month, we could use the `resample()` method like this:
pl_weather_2012_monthly = pl_weather_2012.group_by_dynamic("date/time (lst)", every="1mo").agg(pl.col("temperature_c").median())
pl_weather_2012_monthly.plot.line(x="date/time (lst)", y="temperature_c")
#july august warmest with 22-23 degrees median temp

# TODO: and now in Polars

# %%
pl_weather_description = pl_weather_description.group_by_dynamic("date/time (lst)", every="1mo").agg(pl.col("is_snowing").mean())
pl_weather_description.plot.bar(x="date/time (lst)", y="is_snowing")
# So now we know! In 2012, December was the snowiest month. Also, this graph suggests something that I feel -- it starts snowing pretty abruptly in November, and then tapers off slowly and takes a long time to stop, with the last snow usually being in April or May.
# TODO: please do the same in Polars
# %%
