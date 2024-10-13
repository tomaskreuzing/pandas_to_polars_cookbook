# %%
import pandas as pd
import matplotlib.pyplot as plt
import polars as pl

# %%
# We're going to use a new dataset here, to demonstrate how to deal with larger datasets. This is a subset of the of 311 service requests from [NYC Open Data](https://nycopendata.socrata.com/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9).
# because of mixed types we specify dtype to prevent any errors
complaints = pd.read_csv("../data/311-service-requests.csv", dtype="unicode")
complaints.head()

# %%
# TODO: rewrite the above using the polars library and call the data frame pl_complaints

# %%
# Selecting columns:
complaints["Complaint Type"]

# %%
# TODO: rewrite the above using the polars library

# %%
# Get the first 5 rows of a dataframe
complaints[:5]

# %%
# TODO: rewrite the above using the polars library

# %%
# Combine these to get the first 5 rows of a column:
complaints["Complaint Type"][:5]

# %%
# TODO: rewrite the above using the polars library


# %%
# Selecting multiple columns
complaints[["Complaint Type", "Borough"]]

# %%
# TODO: rewrite the above using the polars library

# %%
# What's the most common complaint type?
complaint_counts = complaints["Complaint Type"].value_counts()
complaint_counts[:10]

# %%
# TODO: rewrite the above using the polars library

# %%
# Plot the top 10 most common complaints
complaint_counts[:10].plot(kind="bar")
plt.title("Top 10 Complaint Types")
plt.xlabel("Complaint Type")
plt.ylabel("Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# %%
# TODO: check if the code to plot the 10 most common complaints works also with your polars data frame
