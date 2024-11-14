# %%
import pandas as pd
import matplotlib.pyplot as plt
import polars as pl
from pathlib import Path
path = Path(__file__).parent.parent / "data" / "311-service-requests.csv"

# Make the graphs a bit prettier, and bigger
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (15, 5)

# This is necessary to show lots of columns in pandas 0.12.
# Not necessary in pandas 0.13.
pd.set_option("display.width", 5000)
pd.set_option("display.max_columns", 60)

#rewrite using polars, to be done once run into plotting problems

# %%
# Let's continue with our NYC 311 service requests example.
# because of mixed types we specify dtype to prevent any errors
pl_complaints = pl.read_csv(path, infer_schema_length = 0)
# TODO: rewrite the above using the polars library (you might have to import it above) and call the data frame pl_complaints

# %%
# 3.1 Selecting only noise complaints
# I'd like to know which borough has the most noise complaints. First, we'll take a look at the data to see what it looks like:
pl_complaints.head(5)
# TODO: rewrite the above in polars

# %%
# To get the noise complaints, we need to find the rows where the "Complaint Type" column is "Noise - Street/Sidewalk".
pl_noise_complaints = pl_complaints.filter(
    pl.col("Complaint Type") == "Noise - Street/Sidewalk"
)
print(pl_noise_complaints)
# TODO: rewrite the above in polars


# %%
# Combining more than one condition
pl_brooklyn_noise_complaints = pl_complaints.filter(
    pl.col("Complaint Type") == "Noise - Street/Sidewalk",
    pl.col("Borough") == "BROOKLYN"
).head(5)
print(pl_brooklyn_noise_complaints)
#pretty neat that you can specify two filtering conditions within the filter method 
# TODO: rewrite the above using the Polars library. In polars these conditions are called Expressions.


# %%
# If we just wanted a few columns:
pl_brooklyn_noise_complaints.select(["Complaint Type", "Borough", "Created Date", "Descriptor"]).head(10)
#selecting only four columns to be printed then applying head to limit to first ten values
# TODO: rewrite the above using the polars library


# %%
# 3.3 So, which borough has the most noise complaints?
pl_borough_comparison = pl_noise_complaints.select("Borough")
#reusing old var where we selected all complaints related to loud noise
pl_borough_comparison.to_series().value_counts(sort=True)
#manhattan seems to have by far the most noise complaints
# TODO: rewrite the above using the polars library

# %%
pl_noise_complaints_counts = pl_borough_comparison.to_series().value_counts(sort=True)
pl_complaint_counts = pl_complaints.select("Borough").to_series().value_counts(sort=True)
pl_merged = pl_noise_complaints_counts.join(pl_complaint_counts, on="Borough", how="inner")
pl_merged_ratio = pl_merged.with_columns(
    ((pl.col("count") / pl.col("count_right")).alias("Complaint ratio"))
)
print(pl_merged_ratio)
# TODO: rewrite the above using the polars library


# %%
pl_merged_ratio.plot.bar(x="Borough", y="Complaint ratio")
# TODO: rewrite the above using the polars library. NB: polars' plotting method is sometimes unstable. You might need to use seaborn or matplotlib for plotting.