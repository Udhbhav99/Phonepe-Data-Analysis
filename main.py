import sqlite3 as sql
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
conn=sql.connect('phonepe_data (3).db')
cur=conn.cursor()

p_logo=Image.open('phonepe.png')

st.set_page_config(page_title='Phonepe Data', page_icon="chart_with_upwards_trend", layout="wide",
                   initial_sidebar_state="auto")
c1,c2=st.columns([1.5,20])
with c1:
    st.image(p_logo)
with c2:
    st.title('Phonepe Data Exploration and visualisation')
st.header(':pray: Welcome to Phonepe-Pulse Dashboard :pray:',divider="grey")
selected = option_menu(None, ["Home","Top Charts","Explore Data"],
                       icons=["house","graph-up-arrow","bar-chart-line",],
                       menu_icon="menu-button-wide", orientation="horizontal",
                       default_index=0, styles={
                           "container": {"padding": "0!important", "background-color": "#6739B7"},
                           "icon": {"color": "white", "font-size": "20px"},
                           "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px",
                                        "--hover-color": None },
                           "nav-link-selected": {"background-color": "red"}})
if selected=="Top Charts":
    options_charts=[
                    "Transactions","Users","Brands","Transaction Type"]
    chart=st.sidebar.selectbox("Select the charts you want to browse",options_charts)
    Year = st.sidebar.slider('select an year',2018,2022)
    Quarter =st.sidebar.slider('select an quarter',1,4)
    if chart=="Transactions":
        col1,col2=st.columns([1,1])
        with col1:
            cur.execute(
                f"select State, sum(Transaction_count) as Total_Count, sum(Transaction_amount) as Total_amount from agg_transactions where Year = {Year} and Quarter = {Quarter} group by state order by Total_amount desc limit 10")
            df = pd.DataFrame(cur.fetchall(), columns=['State', 'Total_Count', 'Total_amount'])
            fig = px.pie(df, values='Total_amount',
                         names='State',
                         title='Top 10 States',
                         color_discrete_sequence=px.colors.sequential.Sunset,
                         hover_data=['Total_Count'],
                         labels={'Total_Count': 'Total_Count'})
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

            cur.execute(
                f"select region as district, sum(Count) as count, sum(Amount)  as amount from map_trans where Year={Year} and Quarter={Quarter} group by district order by amount desc limit 10")
            df_1 = pd.DataFrame(cur.fetchall(), columns=['district', 'count', 'amount'])
            fig1 = px.pie(df_1, values='amount',
                         names='district',
                         title='Top 10 Districts',
                         color_discrete_sequence=px.colors.sequential.Sunset,
                         hover_data=['count'],
                         labels={'count': 'count'})
            fig1.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig1, use_container_width=True)
            cur.execute(
                f"select Pincode as pincode, sum(Transaction_count) as count, sum(Transaction_amount)  as amount from top_trans where Year={Year} and Quarter={Quarter} group by pincode order by amount desc limit 10")
            df_2 = pd.DataFrame(cur.fetchall(), columns=['pincode', 'count', 'amount'])
            fig2 = px.pie(df_2, values='amount',
                          names='pincode',
                          title='Top 10 Pincodes',
                          color_discrete_sequence=px.colors.sequential.Sunset,
                          hover_data=['count'],
                          labels={'count': 'count'})
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig2, use_container_width=True)
        with col2:
            st.write("Top 10 Transactions State Wise")
            st.dataframe(df)
            st.write("Top 10 Transactions District Wise")
            st.dataframe(df_1)
            st.write("Top 10 Transactions Pincode Wise")
            st.dataframe(df_2)

    if chart=="Users":
        if Year==2022 and Quarter in [2,3,4]:
            st.subheader("NO DATA TO BE DISPLAYED IN 2ND 3RD AND 4TH QUARTER OF 2022")
            st.image('sorry-images-hd.webp',width=400)

        else:
            c1,c2=st.columns([1,1])
            with c1:
                cur.execute(
                    f"select State as state, sum(Count) as users from agg_users where Year={Year} and Quarter={Quarter} group by state order by users desc limit 10")
                df_4 = pd.DataFrame(cur.fetchall(), columns=['State', 'users'])
                fig1 = px.pie(df_4, values='users',
                              names='State',
                              title='Top 10 States',
                              color_discrete_sequence=px.colors.sequential.Sunset,
                              hover_data=['users'],
                              labels={'users': 'users'})
                fig1.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig1, use_container_width=True)
                cur.execute(
                    f"select Region as district, sum(RegisteredUsers) as users, sum(AppOpens) as app_opens from map_users where Year={Year} and Quarter={Quarter} group by district order by users desc limit 10")
                df_5 = pd.DataFrame(cur.fetchall(), columns=['district', 'users', 'app_opens'])
                fig2 = px.pie(df_5, values='users',
                              names='district',
                              title='Top 10 Districts',
                              color_discrete_sequence=px.colors.sequential.Sunset,
                              hover_data=['users'],
                              labels={'users': 'users'})
                fig2.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig2, use_container_width=True)
                cur.execute(
                    f"select Pincode as pincodes, sum(RegisteredUsers) as users from top_users where Year={Year} and Quarter={Quarter} group by pincodes order by users desc limit 10")
                df_6 = pd.DataFrame(cur.fetchall(), columns=['pincodes', 'users'])
                fig3 = px.pie(df_6, values='users',
                              names='pincodes',
                              title='Top 10 Pincodes',
                              color_discrete_sequence=px.colors.sequential.Sunset,
                              hover_data=['users'],
                              labels={'users': 'users'})
                fig3.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig3, use_container_width=True)
            with c2:
                st.write("Top 10 User Count State Wise")
                st.dataframe(df_4)
                st.write("Top 10 User Count District Wise")
                st.dataframe(df_5)
                st.write("Top 10 User Count Pincode Wise")
                st.dataframe(df_6)
    if chart=='Brands':
        c1,c2=st.columns([1,1])
        with c1:

            cur.execute(
                f"select Brand_name as brand, Count as users from agg_users where Year={Year} and Quarter={Quarter} group by brand order by users desc limit 10")
            df_7 = pd.DataFrame(cur.fetchall(), columns=['brand', 'users'])
            fig1 = px.pie(df_7, values='users',
                          names='brand',
                          title='Top 10 Brands',
                          color_discrete_sequence=px.colors.sequential.Sunset,
                          hover_data=['users'],
                          labels={'users': 'users'})
            fig1.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig1, use_container_width=True)
        with c2:
            st.write("Top 10 Brands")
            st.dataframe(df_7)
    if chart=="Transaction Type":
        cur.execute(
            f"select Transaction_type as type, Transaction_amount as amount from agg_transactions where Year = {Year} and Quarter = {Quarter} group by type order by amount desc limit 10")
        df_8 = pd.DataFrame(cur.fetchall(), columns=['type', 'amount'])
        fig = px.pie(df_8, values='amount',
                      names='type',
                      title='Top Transaction Types',
                      color_discrete_sequence=px.colors.sequential.Sunset,
                      hover_data=['amount'],
                      labels={'amount': 'amount'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df_8)
if selected=="Explore Data":
    states_list=['andaman-&-nicobar-islands',
                 'andhra-pradesh', 'arunachal-pradesh',
                 'assam', 'bihar', 'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu',
                 'delhi', 'goa', 'gujarat','haryana','himachal-pradesh',
                 'jammu-&-kashmir','jharkhand','karnataka','kerala',
                 'ladakh', 'lakshadweep','madhya-pradesh','maharashtra','manipur','meghalaya','mizoram','nagaland',
                 'odisha','puducherry','punjab','rajasthan','sikkim','tamil-nadu',
                 'telangana','tripura','uttar-pradesh','uttarakhand','west-bengal']
    c1,c2,c3=st.columns([1,1,1])
    with c1:

        map_data=st.selectbox("Select the data to be browsed",["Transaction Count","Transaction Amount","user count"])
    with c2:
        Year = st.selectbox('select an year', [2018, 2019, 2020, 2021, 2022])

    with c3:
        Quarter = st.selectbox('select an quarter', [1, 2, 3, 4])
    df_state=pd.read_csv('States.csv')
    if map_data=="Transaction Count":
        cur.execute(
            f"select State, sum(Transaction_count) as Total_Count, sum(Transaction_amount) as Total_amount from agg_transactions where Year = {Year} and Quarter = {Quarter} group by State order by State")
        df = pd.DataFrame(cur.fetchall(), columns=['State', 'Total_Count', 'Total_amount'])
        df.State = df_state
        fig = px.choropleth(df,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Total_amount',
                            color_continuous_scale='sunset', hover_name='State', hover_data='Total_amount',
                            fitbounds='locations', basemap_visible=False)
        st.plotly_chart(fig, use_container_width=True)
    if map_data == "Transaction Amount":

        cur.execute(
            f"select State, sum(Transaction_count) as Total_Count, sum(Transaction_amount) as Total_amount from agg_transactions where Year = {Year} and Quarter = {Quarter} group by State order by State")
        df = pd.DataFrame(cur.fetchall(), columns=['State', 'Total_Count', 'Total_amount'])
        df.State = df_state
        fig = px.choropleth(df,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Total_Count',
                            color_continuous_scale='sunset', hover_name='State', hover_data='Total_Count',
                            fitbounds='locations', basemap_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    if map_data == "user count":

        cur.execute(
            f"select State, sum(Count) as Count from agg_users where Year = {Year} and Quarter = {Quarter} group by State order by State")
        df = pd.DataFrame(cur.fetchall(), columns=['State', 'Count'])
        df.State = df_state

        fig = px.choropleth(df,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Count',
                            color_continuous_scale='sunset', hover_name='State', hover_data='Count',
                            fitbounds='locations', basemap_visible=False, scope='asia')

        st.plotly_chart(fig, use_container_width=True)
    d_data=st.selectbox("select Data to be viewed",["Total Amount","Total Transactions","total Users"])
    select_state=st.selectbox("select a state",states_list)

    if d_data=="Total Amount":
        cur.execute(
            f"select region as district, sum(Count) as count, sum(Amount), Year from map_trans where State='{select_state}' group by district,Year order by Year")
        df_1 = pd.DataFrame(cur.fetchall(), columns=['district', 'count', 'amount',"Year"])
        fig=px.bar(df_1,x='district',y='amount',color='amount',
                   color_continuous_scale=px.colors.sequential.ice,
                   animation_frame="Year",animation_group="district")
        st.plotly_chart(fig,use_container_width=True)
    elif d_data == "Total Transactions":
        cur.execute(
            f"select region as district, sum(Count) as count, sum(Amount)  as amount,Year from map_trans where State='{select_state}' group by district,Year order by Year")
        df_1 = pd.DataFrame(cur.fetchall(), columns=['district', 'count', 'amount','Year'])
        fig = px.bar(df_1, x='district', y='count', color='count',
                     color_continuous_scale=px.colors.sequential.ice,
                     animation_frame="Year",animation_group="district")
        st.plotly_chart(fig, use_container_width=True)
    else:
        cur.execute(
            f"select Region as district, sum(RegisteredUsers) as users, sum(AppOpens) as app_opens,Year from map_users where State='{select_state}' group by district,Year order by Year")
        df_5 = pd.DataFrame(cur.fetchall(), columns=['district', 'users', 'app_opens',"Year"])
        fig = px.bar(df_5, x='district', y='users', color='users',
                     color_continuous_scale=px.colors.sequential.ice,
                     animation_frame="Year",animation_group="district")
        st.plotly_chart(fig, use_container_width=False)

if selected=="Home":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('')
        st.markdown('')
        st.subheader('Introduction', anchor=False,divider='grey')
        st.markdown("PhonePe is an Indian digital payments and financial services company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface, went live in August 2016.")
        st.markdown("")
        st.markdown("")
        st.markdown("*AS ON PULSE WEBSITE*")
        st.markdown("The Indian digital payments story has truly captured the world's imagination. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government. Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. PhonePe Pulse is our way of giving back to the digital payments ecosystem.", unsafe_allow_html=False)
        st.markdown("")
        st.markdown("")
        st.markdown("You can explore data divided into Transaction Data and User Count Data and further segregated by states, Districts and Pincodes. **HAPPY** **EXPLORING**")
    with col2:
        st.video("https://youtu.be/OVjM4ICYzng?feature=shared", start_time=0)
        st.video("https://youtu.be/yKvAS0p-qbQ?feature=shared",start_time=0)
        