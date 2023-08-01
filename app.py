import streamlit as st
import pandas as pd
import plotly.express as px
API_KEY='a45d27d3-5b49-448d-9959-c3950744a918'
import requests
import io
import base64
import folium
import pydeck as pdk



#####################################
#            HOME PAGE              #
#####################################
st. set_page_config(layout="wide")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
user_input=st.text_input(label="Please Enter",placeholder='Paste your Zillow Link Here', help="Enter your zillow link")
css = """
    <style>
        body {
            background-color: black;
        }
    </style>
"""
st.markdown(css, unsafe_allow_html=True)

if user_input==None:
    st.write("Please provide a link to proceed")

# if user_input is not None and user_input !="":
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
        # df=pd.read_csv(data.csv)
        
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
        st.markdown("<h1 style='text-align: center; color: white;'>Property Metrics 🏙️</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,1,1])


        with col1:
          col1.metric('Total Number of Comps Gathered',  df.shape[0],  help='Number of properties in search')


        with col2:          
          col2.metric('Avg Price of Comp', "${:,}".format(df['price'].mean()).split(',')[0] + 'K', 
          help='Average sale price of properties in search')

        with col3:
          col3.metric('Avg Lot Acreage of Comp ', "{:,}".format(int(df['LOT_ACREAGE'].mean())), 
          help='Average Lot Acreage of properties in search')

          


        # #####################################
        # #             CHARTS                #
        # #####################################
        # with st.expander('Charts', expanded=True):
        #   st.markdown("## Charts 📈")

        #   c1,c2, c3, c4, c5=st.columns(5)
        #   fig_a = px.box(df, x="price", title="Price Box Plot Chart")
        #   c1.plotly_chart(fig_a, use_container_width=True)

        #   fig_b = px.histogram(df, x="LOT_ACREAGE", title="Lots Distribution by size in the county")
        #   c2.plotly_chart(fig_b, use_container_width=True)

        #   fig_c = px.histogram(df, x="LOT_ACREAGE", title="Lots Distribution by size in the county")
        #   c3.plotly_chart(fig_c, use_container_width=True)

        #   fig_d = px.histogram(df, x="LOT_ACREAGE", title="Lots Distribution by size in the county")
        #   c4.plotly_chart(fig_d, use_container_width=True)

        #   with c5:
        #      st.dataframe(df,width=500) 

        #   st.title("Map Plot with Streamlit")
          

        #   st.subheader("Data")



        #   df['LAT']=df["latLong.latitude"]
        #   df['LON']=df["latLong.longitude"]
                          
        #   df_map=df[['LAT','LON']]

          
        #   st.map(df[['LAT','LON']], )



    #     def download_csv(df):
    #     # Create a link to download the CSV file
    #       csv_file = df.to_csv(index=False)
    #       b64 = base64.b64encode(csv_file.encode()).decode()
    #       href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Click here to download CSV file</a>'
    #       st.markdown(href, unsafe_allow_html=True)


    #     if st.button('Download CSV'):
    #     # Call the function to download the CSV file
    #       download_csv(df)
    except KeyError:
        a=6


    def download_csv(df):
      # Create a link to download the CSV file
      csv_file = df.to_csv(index=False)
      b64 = base64.b64encode(csv_file.encode()).decode()
      # href = f'<a  href="data:file/csv;base64,{b64}" download="data.csv">Click here to download CSV file</a>'
      href = f'<a style="display: block; text-align: center;" href="data:file/csv;base64,{b64}" download="data.csv">Click here to download CSV file</a>'
      st.markdown(href, unsafe_allow_html=True)
    st.write("<style>div.stButton > button:first-child {margin: 0 auto; display: block;}</style>", unsafe_allow_html=True)
    if st.button('Gather Data to a CSV'):

      try:
          # Call the function to download the CSV file
          download_csv(df)
      except KeyError:
         a=10

          # st.write("No data found for the provided link. Please check the link and try again.")







    


