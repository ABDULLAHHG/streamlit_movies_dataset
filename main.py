import pandas as pd
import streamlit as st 
import numpy as np 
import plotly.graph_objects as go 
from plotly.subplots import make_subplots 

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


#scatter(df)

def distribution (df):
    column = st.selectbox('select column' , [i for i in df.columns if i != 'names'])
    unique_count = st.select_slider('select number of unique count',[i for i in range(len(df[column].value_counts())+1)] , len(df[column].value_counts().index)//5)
    fig = make_subplots(rows = 1 , cols = 2 , subplot_titles=('countplot','percentage'))
    x = df[column].value_counts().values
    y = df[column].value_counts().index

    fig.add_trace(go.Pie(values = x[0:unique_count] ,
                    labels=y[0:unique_count],
                    textposition='auto',
                    hoverinfo='label',
                    
                    ))
    

    fig.add_trace(go.Bar(x = x[0:unique_count],
                         y = y[0:unique_count],
                         ))
    st.plotly_chart(fig)
    st.text( df[column].value_counts().index[:unique_count])

distribution(df)