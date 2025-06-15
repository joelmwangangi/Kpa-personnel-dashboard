import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("kpa_personnel_dataset_final.csv")
    return df

df = load_data()

st.title("KPA Personnel Dashboard")

# Sidebar filters (single selection)
st.sidebar.header("Filters")
company_filter = st.sidebar.selectbox("Select Company", options=sorted(df['Company'].unique()))
location_filter = st.sidebar.selectbox("Select Work Location", options=sorted(df['Work Location'].unique()))
shift_filter = st.sidebar.selectbox("Select Shift", options=sorted(df['Shift'].unique()))
status_filter = st.sidebar.selectbox("Select Active Status", options=sorted(df['Active Status'].unique()))

# Apply filters
filtered_df = df[
    (df['Company'] == company_filter) &
    (df['Work Location'] == location_filter) &
    (df['Shift'] == shift_filter) &
    (df['Active Status'] == status_filter)
]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Employees", filtered_df.shape[0])
col2.metric("Active Employees", filtered_df[filtered_df['Active Status'] == 'Active'].shape[0])
col3.metric("Average Experience (Years)", round(filtered_df['Years of Experience'].mean(), 1))

# Role Distribution
st.subheader("Role Distribution")
role_counts = filtered_df['Role'].value_counts()
fig1, ax1 = plt.subplots()
role_counts.plot(kind='bar', ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)

# Company Distribution
st.subheader("Company Distribution")
company_counts = filtered_df['Company'].value_counts()
fig2, ax2 = plt.subplots()
company_counts.plot(kind='bar', color='skyblue', ax=ax2)
plt.xticks(rotation=45)
st.pyplot(fig2)

# Work Location Distribution
st.subheader("Work Location Distribution")
location_counts = filtered_df['Work Location'].value_counts()
fig3, ax3 = plt.subplots()
location_counts.plot(kind='bar', color='orange', ax=ax3)
plt.xticks(rotation=45)
st.pyplot(fig3)

# Shift Distribution
st.subheader("Shift Distribution")
shift_counts = filtered_df['Shift'].value_counts()
fig4, ax4 = plt.subplots()
ax4.pie(shift_counts, labels=shift_counts.index, autopct='%1.1f%%', startangle=140)
ax4.axis('equal')
st.pyplot(fig4)

# Country Distribution
st.subheader("Country Distribution")
country_counts = filtered_df['Country'].value_counts()
fig5, ax5 = plt.subplots()
country_counts.plot(kind='bar', color='green', ax=ax5)
plt.xticks(rotation=45)
st.pyplot(fig5)

# Mostly Used Gate
st.subheader("Mostly Used Gate")
gate_counts = filtered_df['Mostly Used Gate'].value_counts()
fig6, ax6 = plt.subplots()
gate_counts.plot(kind='bar', color='purple', ax=ax6)
plt.xticks(rotation=45)
st.pyplot(fig6)

# Most Congested Gate (Per Driver)
st.subheader("Most Congested Gate (Per Driver)")
congested_gate_counts = filtered_df['Most Congested Gate (Per Driver)'].value_counts()
fig7, ax7 = plt.subplots()
congested_gate_counts.plot(kind='bar', color='red', ax=ax7)
plt.xticks(rotation=45)
st.pyplot(fig7)

# Display data
st.subheader("Personnel Data Table")
st.dataframe(filtered_df)

# Download option
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

downloadable_csv = convert_df(filtered_df)
st.download_button(
    label="Download filtered data as CSV",
    data=downloadable_csv,
    file_name='filtered_kpa_personnel.csv',
    mime='text/csv'
)
