import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
day_df = pd.read_csv('day.csv', sep=";")  # Update path if necessary

# Convert date column to datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Sidebar filters
st.sidebar.header("Filter Options")
selected_year = st.sidebar.selectbox("Select Year", day_df['yr'].unique(), format_func=lambda x: f"2011" if x == 0 else "2012")
selected_season = st.sidebar.multiselect("Select Season", day_df['season'].unique(), default=day_df['season'].unique(), format_func=lambda x: ["Spring", "Summer", "Fall", "Winter"][x-1])

# Filtered Data
filtered_df = day_df[(day_df['yr'] == selected_year) & (day_df['season'].isin(selected_season))]

# Main Dashboard Title
st.title("🚴‍♂️ Bike Sharing Dashboard")

# Display Key Metrics
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Rentals", f"{filtered_df['cnt'].sum():,}")
col2.metric("Avg. Rentals per Day", f"{filtered_df['cnt'].mean():,.0f}")
col3.metric("Max Rentals in a Day", f"{filtered_df['cnt'].max():,}")

# Visualization 1: Rentals Over Time
st.subheader("📈 Rentals Over Time")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered_df, x='dteday', y='cnt', ax=ax, color='b')
ax.set_title("Daily Bike Rentals Trend")
ax.set_xlabel("Date")
ax.set_ylabel("Rental Count")
st.pyplot(fig)

# Visualization 2: Rentals vs. Weather Condition
st.subheader("🌦️ Impact of Weather on Rentals")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=filtered_df, x='weathersit', y='cnt', ax=ax, palette="coolwarm")
ax.set_xticklabels(["Clear", "Mist", "Light Rain/Snow", "Heavy Rain/Snow"])
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Rental Count")
ax.set_title("Bike Rentals by Weather Condition")
st.pyplot(fig)

# Show Processed Data
st.subheader("🔍 Processed Data")
st.dataframe(filtered_df[['dteday', 'season', 'weathersit', 'cnt']])

# Footer
st.markdown("🚲 **Bike Sharing Analysis | Powered by Streamlit**")