# %%
import pandas as pd

# %%
df = pd.read_csv('data/data.csv')

df.head()

# %%
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Convert 'Date and Time' to datetime
df['Date and Time'] = pd.to_datetime(df['Date and Time'])

# # Set as index (optional, but helpful)
# df.set_index('Date and Time', inplace=True)

# Resample to hourly average
hourly_pool = df['Pool'].resample('H').mean()

# Plot
plt.figure(figsize=(12,6))
hourly_pool.plot()
plt.title('Average Pool Occupancy per Hour')
plt.xlabel('Time')
plt.ylabel('Number of People')
plt.grid(True)
plt.show()
# %%
df.head()
# %%

import matplotlib.dates as mdates

# Plot
fig, ax = plt.subplots(figsize=(12,6))
ax.plot(hourly_pool.index, hourly_pool.values)

# Title and labels
ax.set_title('Average Pool Occupancy per Hour')
ax.set_xlabel('Time')
ax.set_ylabel('Number of People')

# Format x-axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
fig.autofmt_xdate()  # auto-rotate date labels

ax.grid(True)
plt.show()
# %%
peak_hours = hourly_pool.sort_values(ascending=False)
print(peak_hours.head(5))


# %%
df['day'] = df.index.date
df['hour'] = df.index.hour
pivot = df.pivot_table(values='Pool', index='day', columns='hour', aggfunc='mean')

import seaborn as sns
plt.figure(figsize=(15,6))
sns.heatmap(pivot, cmap="YlGnBu")
plt.title('Average Pool Occupancy: Day vs Hour')
plt.xlabel('Hour')
plt.ylabel('Day')
plt.show()

# %%
df['weekday'] = df.index.weekday  # Monday = 0, Sunday = 6
df['is_weekend'] = df['weekday'] >= 5
print(df.groupby('is_weekend')['Pool'].mean())


# %%
# Make sure datetime is index
df['weekday'] = df.index.weekday  # Monday = 0, Sunday = 6
df['hour'] = df.index.hour

# Filter: weekend and between 10:00 and 20:00
weekend_daytime = df[
    (df['weekday'] >= 5) & 
    (df['hour'] >= 10) &
    (df['hour'] <= 18)
]

weekend_daytime = weekend_daytime[weekend_daytime['Pool'] > 0]

# Find the time with the minimum Pool value
min_pool_time = weekend_daytime['Pool'].idxmin()
min_pool_value = weekend_daytime['Pool'].min()

print(f"The pool was emptiest at {min_pool_time} with {min_pool_value} people.")

# %%
# Get top 3 emptiest times
top3_emptiest = weekend_daytime['Pool'].nsmallest(3)

for time, value in top3_emptiest.items():
    print(f"At {time}, there were {value} people in the pool.")

# %%
# Prepare day and hour columns
df['day'] = df.index.date
df['hour'] = df.index.hour
df['weekday'] = df.index.weekday

# Create pivot table
pivot = df.pivot_table(values='Pool', index='day', columns='hour', aggfunc='mean')

# Create the heatmap
fig, ax = plt.subplots(figsize=(15,12))
sns.heatmap(pivot, cmap="YlGnBu", ax=ax)

# Set every date as a yticks manually
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels([str(d) for d in pivot.index])

# Bold and color weekends
for label in ax.get_yticklabels():
    day_dt = pd.to_datetime(label.get_text())
    if day_dt.weekday() >= 5:
        label.set_fontweight('bold')
        label.set_color('red')

ax.set_title('Average Pool Occupancy: Day vs Hour')
ax.set_xlabel('Hour')
ax.set_ylabel('Day')
plt.show()

# %%
