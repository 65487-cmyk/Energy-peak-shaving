import streamlit as st
import pandas as pd
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Energy consumption", page_icon=":charts_with_upward_trend:", layout="wide")
st.title(":chart_with_upwards_trend: Peak shaving solar sizing")
st.markdown('<style>div.block-container;</style>',unsafe_allow_html=True)

#loading data used
df=pd.read_csv(r"C:\Users\vasey\Downloads\Solardashboard\Peak shaving energy.csv")

col1, col2 = st.columns((2))
df["Date"]= pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M").dt.to_timestamp()

#Get the min and max date
Startdate =df["Date"].min()
Enddate = df["Date"].max()


with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", Startdate))
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", Enddate))

df=df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()

#Filter sidebar
#choose year
st.sidebar.header("Choose year")
df["Year"]=df["Date"].dt.year
Year=st.sidebar.multiselect("Pick year",df["Year"].unique())
if not Year:
    df2=df.copy()
else:
    df2=df[df['Year'].isin(Year)]

#select monthly or daily
period=st.sidebar.radio('Period',['Daily','Monthly'])

if period == 'Monthly':
    x_axis="Month"
else:
    x_axis="Date"

#Filter data based on year

filtered_df=df2.groupby(x_axis)['AEP_MW'].agg(Daily_Average='mean',Daily_Max='max').reset_index()

absolute_peak = filtered_df['Daily_Max'].max()
threshold = absolute_peak * 0.90

#time series analysis
st.subheader("Average and Maximum Daily energy consumption (MW)")
linechart=pd.DataFrame(filtered_df)
fig1=px.line(linechart, x=x_axis, y=['Daily_Average','Daily_Max'], height=500, width=1000, 
             template='gridon',
             labels={x_axis: "Month", "value": "Energy Consumption (MW)", "variable": "Metrics"})

fig1.update_xaxes(tickmode='linear', dtick="M1", tickformat="%b %Y")

fig1.add_hline(y= threshold,line_dash="dash", line_color="red", line_width=2)

#the days exceeding threshold value and maximum demand to be shaved
days_above_threshold = (df2['AEP_MW'] > threshold).sum()
highest_spike = df2['AEP_MW'].max() - threshold

col_kpi1, col_kpi2 = st.columns(2)
with col_kpi1:
    st.metric(label="🚨 Days Over Threshold", value=f"{days_above_threshold}")
with col_kpi2:
    st.metric(label="🔋 Max Solar Power Needed to Shave", value=f"{highest_spike:,.0f} MW")

# Calculate total energy above the threshold
excess_df = df2[df2['AEP_MW'] > threshold]
total_shaving_energy_mwh = (excess_df['AEP_MW'] - threshold).sum()

st.subheader("🔋 Battery Deployment Target")
st.write(f"To successfully shave all peaks in this period, your solar storage system must deliver a total of **{total_shaving_energy_mwh:,.2f} MWh** of offset energy.")

st.plotly_chart(fig1,width= "stretch")





