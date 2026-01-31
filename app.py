import pandas as pd 
import numpy as np 
import streamlit as st 
import matplotlib.pyplot as plt 
st.set_page_config(layout = 'wide',page_title = 'Startup analysis')

df = pd.read_csv("startup_cleaned.csv")

df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
def load_overall_analysis():
    st.title("Overall analysis")
    #  total invested amount :
    total = round(df['amount'].sum())
    
    maxi = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    total_startup = df['startup'].nunique()
    average = df.groupby('startup')['amount'].sum().mean()
    col1 , col2,col3 ,col4  = st.columns(4)
    with col1:
        st.metric('Total', total,'Cr')
    with col2:
        st.metric('Maximum funding : ', maxi,'Cr')
    with col3 :
        st.metric('Average funding : ', average,'Cr')
    with col4: 
        st.metric('Total funded startup ',str(total_startup))
    st.header("MoM graph ")
    df['year'] = df['date'].dt.year
    
    selected_option = st.selectbox('select type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else :
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x- axis'] = temp_df['month'].astype('str')+'-'+temp_df['year'].astype('str')
    fig5, ax5 = plt.subplots()
    ax5.plot(temp_df['x- axis'], temp_df['amount'])
    st.pyplot(fig5)
        
def load_investors_details(investors):
    st.title(investors)
    # load the recent 5 investments of the investors
    last5_df = df[df['Investors'].str.contains(investors , na=False)].head()[['date', 'startup', 'Industry Vertical', 'subverticals', 'city',	'Investors', 'round', 'amount']]
    st.subheader('Most recent Investment ')
    st.dataframe(last5_df)
    col1 , col2,col3 , col4  = st.columns(4)
    with col1:
       #  biggest investments ::: 
       big_series = df[df['Investors'].str.contains(investors, na=False)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
       st.subheader('Biggest Investment  ')
       # st.dataframe(big_series)
       fig,ax = plt.subplots()
       ax.bar(big_series.index , big_series.values )
       st.pyplot(fig)
    with col2 :
        
        vertical_series = df[df['Investors'].str.contains(
            'investors', na=False)].groupby('Industry Vertical')['amount'].sum()

        st.subheader('Select invensted in :')
        fig1,ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index , autopct = "%0.01f%%")
        st.pyplot(fig1)
        
        
    with col3:
        v1 = df[df['Investors'].str.contains('investors', na=False)].groupby('round')['amount'].sum()
        st.subheader('Select round  in :')
        fig3, ax3 = plt.subplots()
        ax3.pie(v1, labels=v1.index, autopct="%0.01f%%")
        st.pyplot(fig1)
        
    with col4:

        # 1. Convert the column to datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

# 2. Now you can extract the year
        df['year'] = df['date'].dt.year

        v2 = df[df['Investors'].str.contains('investors', na=False)].groupby('year')[
            'amount'].sum()

        st.subheader('Year on Year Investment :')
        fig4, ax4 = plt.subplots()
        ax4.plot(v2.index , v2.values)
        st.pyplot(fig4)

        
st.sidebar.title('Startup Funding Analysis ')
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup','Investor'])

if option == 'Overall Analysis':
    # btn= st.sidebar.button('Show Overall Analysis')
    # if btn:
elif option == 'Overall Analysis':
    option = st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details ')
    st.title('Startup Analysis ')

else :
    selected_investor =  st.sidebar.selectbox('Select Startup', sorted( df['Investors'].str.split(',').explode().str.strip().dropna().unique()))
    btn2 = st.sidebar.button("Find Investors Details ")
    if btn2 :
        load_investors_details(selected_investor)
    st.title("Investor Analysis ")



























