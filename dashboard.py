import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
day_df = pd.read_csv('day.csv', sep=";")  # Update path if necessary
hour_df = pd.read_csv('hour.csv', sep=";")  # Load hour dataset

# Convert date column to datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Sidebar filters
st.sidebar.header("Filter Options")
selected_year = st.sidebar.multiselect("Select Year", day_df['yr'].unique(), default=day_df['yr'].unique(), format_func=lambda x: f"2011" if x == 0 else "2012")
selected_season = st.sidebar.multiselect("Select Season", day_df['season'].unique(), default=day_df['season'].unique(), format_func=lambda x: ["Spring", "Summer", "Fall", "Winter"][x-1])

# Filtered Data
filtered_day_df = day_df[(day_df['yr'].isin(selected_year)) & (day_df['season'].isin(selected_season))]
filtered_hour_df = hour_df[(hour_df['yr'].isin(selected_year)) & (hour_df['season'].isin(selected_season))]

# Main Dashboard Title
st.title("🚴‍♂️ Bike Sharing Dashboard")

# Display Key Metrics
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Rentals", f"{filtered_day_df['cnt'].sum():,}")
col2.metric("Avg. Rentals per Day", f"{filtered_day_df['cnt'].mean():,.0f}")
col3.metric("Max Rentals in a Day", f"{filtered_day_df['cnt'].max():,}")

# Visualization 1: Correlation Heatmap - Factors Influencing Bike Rentals
st.subheader("📊 Factors Influencing Bike Rentals")

# Compute correlation matrix for the filtered dataset
correlation_matrix = filtered_day_df.corr()

# Select relevant columns
relevant_columns = ['temp', 'hum', 'windspeed', 'weathersit', 'season', 'cnt']
correlation_matrix = correlation_matrix[relevant_columns].loc[relevant_columns]

# Plot heatmap
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
ax.set_title(f"Correlation Heatmap: Bike Rentals vs. Other Factors\n(Filtered by Year & Season)")

st.pyplot(fig)

# Visualization 2: Peak Hours Analysis (Filtered)
st.subheader("⏰ Peak Hours for Bike Rentals")

# Aggregate rental counts per hour after filtering
peak_hours = filtered_hour_df.groupby("hr")["cnt"].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=peak_hours["hr"], y=peak_hours["cnt"], palette="coolwarm", ax=ax)
ax.set_xlabel("Hour of the Day")
ax.set_ylabel("Total Bike Rentals")
ax.set_title("Bike Rentals by Hour (Filtered by Year & Season)")
st.pyplot(fig)

# Footer
st.markdown("🚲 **Bike Sharing Analysis | Powered by Streamlit**")
