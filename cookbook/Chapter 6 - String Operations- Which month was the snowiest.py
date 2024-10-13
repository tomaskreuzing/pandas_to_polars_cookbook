# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (15, 3)
plt.rcParams["font.family"] = "sans-serif"


# %%
# We saw earlier that pandas is really good at dealing with dates. It is also amazing with strings! We're going to go back to our weather data from Chapter 5, here.
weather_2012 = pd.read_csv(
    "../data/weather_2012.csv", parse_dates=True, index_col="date_time"
)
weather_2012[:5]

# TODO: load the data using polars and call the data frame pl_wather_2012


# %%
# You'll see that the 'Weather' column has a text description of the weather that was going on each hour. We'll assume it's snowing if the text description contains "Snow".
# Pandas provides vectorized string functions, to make it easy to operate on columns containing text. There are some great examples: "http://pandas.pydata.org/pandas-docs/stable/basics.html#vectorized-string-methods" in the documentation.
weather_description = weather_2012["weather"]
is_snowing = weather_description.str.contains("Snow")

# Let's plot when it snowed and when it did not:
is_snowing = is_snowing.astype(float)
is_snowing.plot()
plt.show()

# TODO: do the same with polars


# %%
# If we wanted the median temperature each month, we could use the `resample()` method like this:
weather_2012["temperature_c"].resample("M").apply(np.median).plot(kind="bar")
plt.show()

# Unsurprisingly, July and August are the warmest.

# TODO: and now in Polars


# %%
# So we can think of snowiness as being a bunch of 1s and 0s instead of `True`s and `False`s:
is_snowing.astype(float)[:10]

# and then use `resample` to find the percentage of time it was snowing each month
is_snowing.astype(float).resample("M").apply(np.mean).plot(kind="bar")
plt.show()

# So now we know! In 2012, December was the snowiest month. Also, this graph suggests something that I feel -- it starts snowing pretty abruptly in November, and then tapers off slowly and takes a long time to stop, with the last snow usually being in April or May.

# TODO: please do the same in Polars
