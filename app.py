import streamlit as st
import pandas as pd
import plotly.express as px
API_KEY='97fcae0b-41e4-4588-9361-0675ba8348d7'
import requests
import io
import base64
import folium
import pydeck as pdk


#####################################
#            HOME PAGE              #
#####################################
st. set_page_config(layout="wide")

primaryColor="#F63366"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#262730"
font="sans serif"


############# TITLE ####################

st.title('Property Data Zillow 🏠')
st.markdown('The purpose of this app is to provide summary stats 📊 based on your Zillow data search.')
st.markdown("#### {0} :point_down:".format('Enter your Zillow search link here please'))
user_input=st.text_input('Enter Here')



if user_input is None:
    st.write("Please provide a Zillow Listings Page link to proceed.")

if user_input is not None:
    
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
    except KeyError:
        st.write("No data found for the provided link. Please check the link and try again.")


    ################# WRNAGLING #########
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
      # fig = px.histogram(df, x="DAYS ON MARKET", title="Days on Market Histogram Chart")
      # st.plotly_chart(fig, use_container_width=True)
      c1,c2, c3, c4=st.columns(4)
      fig_a = px.box(df, x="price", title="Price Box Plot Chart")
      c1.plotly_chart(fig_a, use_container_width=True)

      fig_b = px.histogram(df, x="LOT_ACREAGE", title="Lots Distribution by size in the county")
      c2.plotly_chart(fig_b, use_container_width=True)

      fig_c = px.histogram(df, x="LOT_ACREAGE", title="Lots Distribution by size in the county")
      c3.plotly_chart(fig_c, use_container_width=True)

      fig_d = px.histogram(df, x="LOT_ACREAGE", title="Lots Distribution by size in the county")
      c4.plotly_chart(fig_d, use_container_width=True)
      # c1, c2 = st.columns([1,1])
      # st.markdown("## Charts 📈")
      # # fig = px.histogram(df, x="DAYS ON MARKET", title="Days on Market Histogram Chart")
      # # st.plotly_chart(fig, use_container_width=True)
      # with c1:
      #   c1 = px.box(df, x="price", title="Price Box Plot Chart")
      #   st.plotly_chart(c1)
      # with c2:
      #   c2 = px.histogram(df, x="LOT_ACREAGE", title="Lots Distribution by size in the county")
      #   st.plotly_chart(c2)


    #############################
      st.title("Map Plot with Streamlit")
      
      # Display the DataFrame with latitude and longitude
      st.subheader("Data")


      # Create a folium map centered on the first point
      df['LAT']=df["latLong.latitude"]
      df['LON']=df["latLong.longitude"]
                      
      df_map=df[['LAT','LON']]
    #####################################
      
      st.map(df[['LAT','LON']], )
    ##############

    ##############


    def download_csv(df):
    # Create a link to download the CSV file
      csv_file = df.to_csv(index=False)
      b64 = base64.b64encode(csv_file.encode()).decode()
      href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Click here to download CSV file</a>'
      st.markdown(href, unsafe_allow_html=True)


    if st.button('Download CSV'):
    # Call the function to download the CSV file
      download_csv(df)
##########################################################
# if user_input is None:
#    st.write("Please Provide Zillow Listings Page link To Proceed Please...")
   

# if user_input is not None:
    

  
    
#     url = "https://app.scrapeak.com/v1/scrapers/zillow/listing"
#     querystring = {
#         "api_key": '97fcae0b-41e4-4588-9361-0675ba8348d7',
#         "url": user_input
#     }

#     listing_response=requests.request("GET", url, params=querystring)


#     # df = pd.read_csv(uploaded_file)
#     df=pd.json_normalize(listing_response.json()['data']['cat1']['searchResults']['mapResults'])
#     st.dataframe(df)

# else:
#   st.write("Please Provide Link to Proceed")

  ########################################################################################################################################







#     #####################################
#     #             FEATURES              #
#     #####################################
#     df_features = df.copy()
#     df_features['ratio_sqft_bd'] = df_features['SQUARE FEET'] / df_features['BEDS']
#     df_features['additional_bd_opp'] = df_features.apply(lambda x: 
#     additional_bedroom_opportunity(x), axis=1)
#     df_features['ratio_lot_sqft'] =  df_features['LOT SIZE'] / df_features['SQUARE FEET']
#     df_features['adu_potential'] = df_features.apply(lambda x: 
#     adu_potential(x), axis=1)


#     #####################################
#     #              TABLES               #
#     #####################################
#     with st.expander('Opportunities', expanded=True):
#         st.markdown("## Opportunities 💡")
#         df_add_bd = df_features.loc[df_features['additional_bd_opp'] == True]
#         df_adu = df_features.loc[df_features['adu_potential'] == True]

#         col1, col2 = st.columns(2)
#         col1.metric('Total Add Bd', len(df_add_bd), help='Number of properties with additonal bedroom opportunity')
#         col2.metric('Total ADU', len(df_adu), help='Number of properties with ADU potential')

#         st.markdown("#### Featurized Dataset")
#         st.write(df_features)

#         # convert featurized dataset to csv
#         csv = convert_df(df_features)

#         st.download_button(
#             "Download 🔽",
#             csv,
#             "property_dataset.csv",
#             "text/csv",
#             key='download-csv'
#         )


