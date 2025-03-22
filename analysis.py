# %%
import pandas as pd

# %%
df = pd.read_csv('data.csv')

df.head()
# %%
# We want to create synthetic data / prediction for the time range 5-6
# waterpark guests is not necessary for now.
df[df['Time'] <= '2025-03-11 09:18:39']
# %%
