import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Helper function untuk menyiapkan berbagai dataframe
def prepare_delivery_time_dataframe(orders_df):
    delivery_time = orders_df["order_estimated_delivery_date_only"] - orders_df["order_delivered_customer_date_only"]
    delivery_time_seconds = delivery_time.apply(lambda x: x.total_seconds())
    orders_df["delivery_time"] = round(delivery_time_seconds / 86400)
    
    return orders_df

def prepare_state_order_count_dataframe(all_df):
    statecount_df = all_df.groupby(by="customer_state").order_id.nunique().reset_index()
    statecount_df.rename(columns={"order_id": "order_count"}, inplace=True)
    return statecount_df

# Load data dari file CSV
all_df = pd.read_csv("all_data.csv")

datetime_columns = ["order_delivered_customer_date_only", "order_estimated_delivery_date_only"]
all_df.sort_values(by="order_delivered_customer_date_only", inplace=True)
all_df.reset_index(drop=True, inplace=True)

# Mengonversi kolom ke format datetime
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["order_delivered_customer_date_only"].min()
max_date = all_df["order_delivered_customer_date_only"].max()

with st.sidebar:
    # Menambahkan logo perusahaan 
    st.image("https://raw.githubusercontent.com/zerogravty/submission/main/e-comm.png")

    # Mengambil start_date & end_date dari date_input    
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_delivered_customer_date_only"] >= pd.to_datetime(start_date)) & 
                 (all_df["order_delivered_customer_date_only"] <= pd.to_datetime(end_date))]

# Menggunakan helper function untuk mempersiapkan data delivery time dan state order count
main_df = prepare_delivery_time_dataframe(main_df)
statecount_df = prepare_state_order_count_dataframe(main_df)

# Header di Streamlit
st.header('Dashboard of E-Commerce Public :sparkles:')
st.text('Oleh: Ghita Aisha Rahmasari')

# Subheader untuk menampilkan distribusi waktu pengiriman
st.subheader("Distribution of Order Delivery Time")

# Plot distribusi waktu pengiriman
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=main_df, x="delivery_time", bins=30, kde=True, color="skyblue", ax=ax)
ax.set_title('Distribution of Order Delivery Time', fontsize=16)
ax.set_ylabel('Number of Orders', fontsize=12)
plt.xlabel(None)
st.pyplot(fig)

# Subheader untuk menampilkan most and least orders by customer state
st.subheader("Most and Least Order by Customer State")

# Plot order count berdasarkan customer state
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Bar plot untuk most orders
sns.barplot(x="order_count", y="customer_state", data=statecount_df.sort_values(by="order_count", ascending=False).head(14), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Most Order Customers", loc="center", fontsize=18)
ax[0].tick_params(axis='y', labelsize=15)

# Bar plot untuk least orders
sns.barplot(x="order_count", y="customer_state", data=statecount_df.sort_values(by="order_count", ascending=True).head(13), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Least Order Customers", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

# Menampilkan plot
st.pyplot(fig)
