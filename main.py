import pandas as pd
import streamlit as st 
import numpy as np 
import plotly.graph_objects as go 

df = pd.read_csv('imdb_movies.csv')
df = df.dropna()
df['date_x'] = pd.to_datetime(df['date_x']) 
df['year'] = df['date_x'].dt.year
df = df.set_index('date_x')
st.dataframe(df.sort_values(by = 'budget_x'))
 
def scatter(df):
    df =df.sort_values(by = 'budget_x')
    df = df.iloc[:100,:]
    trace1 = go.Scatter(
                        x = df.index,
                        y = df.budget_x,
                        mode = 'lines',
                        name = 'budget',
                        marker = dict(color = '#4B0082'),
                        text = df.names)
    
    trace2 = go.Scatter(
                        x = df.index,
                        y = df.revenue,
                        mode = 'lines+markers',
                        name = 'revenue',
                        marker = dict(color = '#FFFCA5'),
                        text = df.names)
    

    data = [trace1 ,trace2]
    layout = dict(title = 'budget and revenue vs time' ,
                  xaxis = dict (title = 'time year - month - day',ticklen = 5 , zeroline = False)
                  )
    fig = dict(data = data , layout = layout)
    st.plotly_chart(fig)

# distribution function 
def dist(df):
    # Select column
    x = st.selectbox('select column' , [i for i in df.columns]) 
    trace = go.pie(
        x = x,
        y = x.value_counts().index,

                    )

#scatter(df)
