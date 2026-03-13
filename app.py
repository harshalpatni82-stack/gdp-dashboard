import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Nassau Candy Logistics & Profitability", layout="wide")
st.title("🍭 Nassau Candy: Operational Intelligence Dashboard")

# --- 1. FACTORY DATA (From your Uploaded Table) ---
factory_data = {
    'Factory': ["Lot's O' Nuts", "Wicked Choccy's", "Sugar Shack", "Secret Factory", "The Other Factory"],
    'LATITUDE': [32.881893, 32.076176, 48.11914, 41.446333, 35.1175],
    'LONGITUDE': [-111.768036, -81.088371, -96.18115, -90.565487, -89.971107]
}
df_factories = pd.DataFrame(factory_data)

# --- 2. MOCK SALES DATA (Based on your Dataset Fields) ---
@st.cache_data
def load_sales_data():
    # In production, replace this with: df = pd.read_csv("nassau_orders.csv")
    data = {
        'Product Name': ['Wonka Bar - Nutty Crunch', 'Laffy Taffy', 'Nerds', 'Wonka Gum', 'Kazookles', 'Everlasting Gobstopper'],
        'Division': ['Chocolate', 'Sugar', 'Sugar', 'Other', 'Other', 'Sugar'],
        'Sales': [50000, 30000, 25000, 15000, 5000, 40000],
        'Cost': [42000, 15000, 10000, 12000, 4800, 18000],
        'Units': [1000, 2000, 2500, 500, 200, 1500],
        'Factory': ["Lot's O' Nuts", "Sugar Shack", "Sugar Shack", "Secret Factory", "The Other Factory", "Secret Factory"]
    }
    df = pd.DataFrame(data)
    df['Gross Profit'] = df['Sales'] - df['Cost']
    df['Gross Margin (%)'] = (df['Gross Profit'] / df['Sales']) * 100
    return df

df_sales = load_sales_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Dashboard Controls")
selected_div = st.sidebar.multiselect("Filter by Division", options=df_sales['Division'].unique(), default=df_sales['Division'].unique())
margin_cutoff = st.sidebar.slider("Margin Risk Threshold (%)", 0, 100, 25)

# --- APP LAYOUT ---
tab1, tab2 = st.tabs(["📈 Profitability Analysis", "🚚 Logistics & Factory Map"])

with tab1:
    st.header("Product Line Margin Performance")
    
    # KPI Row
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Sales", f"${df_sales['Sales'].sum():,}")
    c2.metric("Avg Margin", f"{df_sales['Gross Margin (%)'].mean():.1f}%")
    c3.metric("Underperforming Products", len(df_sales[df_sales['Gross Margin (%)'] < margin_cutoff]))

    # Scatter Plot: Cost vs Sales
    fig_scatter = px.scatter(df_sales, x="Sales", y="Cost", size="Gross Margin (%)", 
                 color="Division", hover_name="Product Name", title="Cost vs Sales (Bubble Size = Margin %)")
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab2:
    st.header("Factory Geographical Distribution")
    # Mapping the coordinates provided in the project prompt
    fig_map = px.scatter_geo(df_factories, lat='LATITUDE', lon='LONGITUDE', 
                             hover_name='Factory', scope='usa',
                             title="Factory Locations for Nationwide Delivery")
    fig_map.update_geos(projection_type="albers usa")
    st.plotly_chart(fig_map, use_container_width=True)
    st.table(df_factories)

st.success("Analysis Complete: Actionable insights generated for Nassau Candy.")
