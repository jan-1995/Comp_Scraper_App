import streamlit as st
import pandas as pd
import plotly.express as px
API_KEY='97fcae0b-41e4-4588-9361-0675ba8348d7'
import requests
import io
import base64
import folium
import pydeck as pdk
import plost

# with open ('style.css') as f:

#    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)




#####################################
#            HOME PAGE              #
#####################################
st. set_page_config(layout="wide")
user_input=st.text_input('Enter Here')
css = """
    <style>
        body {
            background-color: black;
        }
    </style>
"""
st.markdown(css, unsafe_allow_html=True)

if user_input==None:
    st.write("Please provide a Zillow Listings Page link to proceed.")

if user_input is not None and user_input !="":
    
    
    url = "https://app.scrapeak.com/v1/scrapers/zillow/listing"
    querystring = {
        "api_key": API_KEY,
        "url": user_input
    }

    listing_response = requests.request("GET", url, params=querystring)

    try:
        
        data = listing_response.json()['data']['cat1']['searchResults']['mapResults']
        df = pd.json_normalize(data)
        st.dataframe(df)
        df['price']=df['hdpData.homeInfo.price']
        df['price']=df['price'].astype(str)
        df['price']=df['price'].str.replace(',','')
        df['price']=df['price'].astype(float)


        df['LOT_ACREAGE']=df['lotAreaString']
        df['LOT_ACREAGE']=df['LOT_ACREAGE'].str.strip()
        df['LOT_ACREAGE']=df['LOT_ACREAGE'].astype(str)
        df['LOT_ACREAGE']=df['LOT_ACREAGE'].str.replace('acres','')
        df['LOT_ACREAGE']=df['LOT_ACREAGE'].astype(float)

        #####################################
        #              METRICS              #
        #####################################
        st.markdown("## Property Metrics 🏙️")
        col1, col2, col3 = st.columns([1,1,1])


        with col1:
          col1.metric('Total',  df.shape[0],  help='Number of properties in search')

        with col2:          
          col2.metric('Avg Price', "${:,}".format(df['price'].mean()).split(',')[0] + 'K', 
          help='Average sale price of properties in search')

        with col3:
          col3.metric('Avg ', "{:,}".format(int(df['LOT_ACREAGE'].mean())), 
          help='Average Lot Acreage of properties in search')
          


        #####################################
        #             CHARTS                #
        #####################################
        with st.expander('Charts', expanded=True):
          st.markdown("## Charts 📈")

          c1,c2, c3, c4=st.columns(4)
          fig_a = px.box(df, x="price", title="Price Box Plot Chart")
          c1.plotly_chart(fig_a, use_container_width=True)

          fig_b = px.histogram(df, x="LOT_ACREAGE", title="Lots Distribution by size in the county")
          c2.plotly_chart(fig_b, use_container_width=True)

          fig_c = px.histogram(df, x="LOT_ACREAGE", title="Lots Distribution by size in the county")
          c3.plotly_chart(fig_c, use_container_width=True)

          fig_d = px.histogram(df, x="LOT_ACREAGE", title="Lots Distribution by size in the county")
          c4.plotly_chart(fig_d, use_container_width=True)

          st.title("Map Plot with Streamlit")
          

          st.subheader("Data")



          df['LAT']=df["latLong.latitude"]
          df['LON']=df["latLong.longitude"]
                          
          df_map=df[['LAT','LON']]

          
          st.map(df[['LAT','LON']], )



        def download_csv(df):
        # Create a link to download the CSV file
          csv_file = df.to_csv(index=False)
          b64 = base64.b64encode(csv_file.encode()).decode()
          href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Click here to download CSV file</a>'
          st.markdown(href, unsafe_allow_html=True)


        if st.button('Download CSV'):
        # Call the function to download the CSV file
          download_csv(df)
    except KeyError:
        st.write("No data found for the provided link. Please check the link and try again.")

    


