# import pandas as pd 
import pickle
import datetime
import streamlit as st
st.title('Recommendation System')

final_df = pickle.load(open('final_df.pkl','rb'))


def recommend_items(cust_id,date):
    
    customer_details = final_df[(final_df['CustomerID'] == int(cust_id)) & (final_df['InvoiceDate'] == date)]
    if len(customer_details) == 0 :
        return f"There is no entry for customer {cust_id}"
    
    # extracting purchased items by customer on given date
    cust_items = customer_details['StockCode'].to_list()
    
    # extracting cust who purchased same item
    similiar_items_cust = final_df[final_df['StockCode'].isin(cust_items)]['CustomerID'].unique()
    
    # Recommending items on their occurance count
    recommended_items = final_df[(final_df['CustomerID'].isin(similiar_items_cust) 
                                  & 
                                  (~ final_df['StockCode'].isin(cust_items)))]['Description'].value_counts()
    
    top_5_recommendations = recommended_items[:5].index
    
    
    return top_5_recommendations



cust_id = st.text_input('Enter Customer ID')

date = st.date_input(
    "Please Enter Date",
    datetime.date(2019, 7, 6))

if st.button('Recommend'):
    top_reco_items =recommend_items(cust_id,date.strftime('%Y-%m-%d'))
    for i in top_reco_items:
        st.write(i)
