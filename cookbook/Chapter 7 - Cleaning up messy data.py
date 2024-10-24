# %%
# The usual preamble
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import polars as pl

# Make the graphs a bit prettier, and bigger
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (15, 5)
plt.rcParams["font.family"] = "sans-serif"


# %%
# One of the main problems with messy data is: how do you know if it's messy or not?
# We're going to use the NYC 311 service request dataset again here, since it's big and a bit unwieldy.
requests = pd.read_csv("../data/311-service-requests.csv", dtype="unicode")
requests.head()

#TODO: load the data with Polars

requests_pl = pl.read_csv("/Users/conorowens/Documents/Cambridge/MT/Fundamentals of Data Science/PS/pandas_to_polars_cookbook/data/311-service-requests.csv",
                       ignore_errors=True)

# Display the first few rows
requests_pl.head()

# %%
# How to know if your data is messy?
# We're going to look at a few columns here. I know already that there are some problems with the zip code, so let's look at that first.

# To get a sense for whether a column has problems, I usually use `.unique()` to look at all its values. If it's a numeric column, I'll instead plot a histogram to get a sense of the distribution.

# When we look at the unique values in "Incident Zip", it quickly becomes clear that this is a mess.

# Some of the problems:

# * Some have been parsed as strings, and some as floats
# * There are `nan`s
# * Some of the zip codes are `29616-0759` or `83`
# * There are some N/A values that pandas didn't recognize, like 'N/A' and 'NO CLUE'

# What we can do:

# * Normalize 'N/A' and 'NO CLUE' into regular nan values
# * Look at what's up with the 83, and decide what to do
# * Make everything strings

requests["Incident Zip"].unique()

# TODO: what's the Polars command for this?

requests_pl["Incident Zip"].unique()

# %%
# Fixing the nan values and string/float confusion
# We can pass a `na_values` option to `pd.read_csv` to clean this up a little bit. We can also specify that the type of Incident Zip is a string, not a float.
na_values = ["NO CLUE", "N/A", "0"]
requests = pd.read_csv(
    "../data/311-service-requests.csv", na_values=na_values, dtype={"Incident Zip": str}
)
requests["Incident Zip"].unique()

# TODO: please implement this with Polars

na_values_pl = ["NO CLUE", "N/A", "0", "NA"]
requests_pl = pl.read_csv("/Users/conorowens/Documents/Cambridge/MT/Fundamentals of Data Science/PS/pandas_to_polars_cookbook/data/311-service-requests.csv",
                       null_values=na_values_pl,
                       dtypes={"Incident Zip":pl.Utf8})

requests_pl["Incident Zip"].unique()

# %%
# What's up with the dashes?
rows_with_dashes = requests["Incident Zip"].str.contains("-").fillna(False)
len(requests[rows_with_dashes])
requests[rows_with_dashes]

# TODO: please implement this with Polars
rows_with_dashes_pl = requests_pl["Incident Zip"].str.contains("-").fill_null(False)
rows_with_dashes_pl_count = rows_with_dashes_pl.sum()
requests_dashed_incidentzip_pl = requests_pl.filter(rows_with_dashes_pl)
print(rows_with_dashes_pl_count)
print(requests_dashed_incidentzip_pl)

# %%
# I thought these were missing data and originally deleted them like this:
# `requests['Incident Zip'][rows_with_dashes] = np.nan`
# But then 9-digit zip codes are normal. Let's look at all the zip codes with more than 5 digits, make sure they're okay, and then truncate them.
long_zip_codes = requests["Incident Zip"].str.len() > 5
requests["Incident Zip"][long_zip_codes].unique()
requests["Incident Zip"] = requests["Incident Zip"].str.slice(0, 5)

# TODO: please implement this with Polars

long_zip_codes_pl = requests_pl["Incident Zip"].str.len_chars() > 5
unique_long_zips_pl = requests_pl.filter(long_zip_codes_pl)["Incident Zip"].unique()
requests_pl = requests_pl.with_columns(
    pl.col("Incident Zip").str.slice(0,5).alias("Incident Zip"))

# %%
#  I'm still concerned about the 00000 zip codes, though: let's look at that.
requests[requests["Incident Zip"] == "00000"]

zero_zips = requests["Incident Zip"] == "00000"
requests.loc[zero_zips, "Incident Zip"] = np.nan

# TODO: please implement this with Polars

requests_pl.filter(pl.col("Incident Zip")=="00000")
requests_pl = requests_pl.with_columns(
    pl.when(pl.col("Incident Zip") == None)
    .then(None)
    .otherwise(pl.col("Incident Zip"))
    .alias("Incident Zip")
)

# %%
# Great. Let's see where we are now:
unique_zips = requests["Incident Zip"].unique()
# Convert all values to strings, handling NaN values
unique_zips = requests["Incident Zip"].fillna("NaN").astype(str).unique()
unique_zips.sort()
unique_zips

# Amazing! This is much cleaner.

# TODO: please implement this with Polars
unique_zips_pl = requests_pl["Incident Zip"].unique()
unique_zips_pl = requests_pl["Incident Zip"].fill_null("NaN").cast(pl.Utf8).unique().sort()

unique_zips_pl.sort()
unique_zips_pl
# %%
# There's something a bit weird here, though -- I looked up 77056 on Google maps, and that's in Texas.
# Let's take a closer look:
zips = requests["Incident Zip"]
# Let's say the zips starting with '0' and '1' are okay, for now. (this isn't actually true -- 13221 is in Syracuse, and why?)
is_close = zips.str.startswith("0") | zips.str.startswith("1")
# There are a bunch of NaNs, but we're not interested in them right now, so we'll say they're False
is_far = ~(is_close) & zips.notnull()
zips[is_far]

# TODO: please implement this with Polars
# Step 1: Extract the "Incident Zip" column
zips_pl = requests_pl["Incident Zip"]

is_close_pl = zips_pl.str.starts_with("0") | zips_pl.str.starts_with("1")
is_far_pl = (~is_close_pl) & zips_pl.is_not_null()
far_zips_pl = requests_pl.filter(is_far_pl)

far_zips_pl

# %%
requests[is_far][["Incident Zip", "Descriptor", "City"]].sort_values("Incident Zip")
# Okay, there really are requests coming from LA and Houston! Good to know.

# TODO: please implement this with Polars
requests_pl.filter(is_far_pl).select(
    ["Incident Zip", "Descriptor", "City"]
).sort("Incident Zip")

# %%
# Filtering by zip code is probably a bad way to handle this -- we should really be looking at the city instead.
requests["City"].str.upper().value_counts()

# It looks like these are legitimate complaints, so we'll just leave them alone.

# TODO: please implement this with Polars
requests_pl.select(pl.col("City").str.to_uppercase().value_counts())

# %%
# Let's turn this analysis into a function putting it all together:
na_values = ["NO CLUE", "N/A", "0"]
requests = pd.read_csv(
    "../data/311-service-requests.csv", na_values=na_values, dtype={"Incident Zip": str}
)


def fix_zip_codes(zips):
    # Truncate everything to length 5
    zips = zips.str.slice(0, 5)

    # Set 00000 zip codes to nan
    zero_zips = zips == "00000"
    zips[zero_zips] = np.nan

    return zips


requests["Incident Zip"] = fix_zip_codes(requests["Incident Zip"])

requests["Incident Zip"].unique()

# TODO: please implement this with Polars
na_values_pl = ["NO CLUE", "N/A", "0", "NA"]
requests_pl = pl.read_csv("/Users/conorowens/Documents/Cambridge/MT/Fundamentals of Data Science/PS/pandas_to_polars_cookbook/data/311-service-requests.csv",
                          null_values=na_values_pl,
                          dtypes={"Incident Zip":pl.Utf8})

def fix_zip_codes_pl(zips_pl):
    zips_pl = zips_pl.str.slice(0, 5)
    zips_pl = zips_pl.fill_null("NaN")
    zips_pl = pl.when(zips_pl == "00000").then(None).otherwise(zips_pl)
    
    return zips_pl

requests_pl = requests_pl.with_columns(
    fix_zip_codes_pl(pl.col("Incident Zip")).alias("Incident Zip")
)

requests_pl["Incident Zip"].unique().sort()

# %%
