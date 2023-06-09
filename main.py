import pandas as pd
import streamlit as st 
import numpy as np 
import plotly.graph_objects as go 
from plotly.subplots import make_subplots 
import colorlover as cl
import plotly.colors as pc

# color_palette = cl.scales['12']['qual']['Set3']

# # Generate a color palette with more than 20,000 colors
# color_palette = cl.interp(cl.scales['11']['div']['RdYlBu'], 20000)

# # Convert color values to RGB format
# color_palette_rgb = [pc.to_rgb(c) for c in color_palette]

df = pd.read_csv('imdb_movies.csv')
df = df.dropna()
df['date_x'] = pd.to_datetime(df['date_x']) 
df['year'] = df['date_x'].dt.year
df = df.set_index('date_x')
st.dataframe(df)

 

colors = ['#7c90db', '#92a8d1', '#a5c4e1', '#f7cac9', '#fcbad3', '#e05b6f', '#f8b195', '#f5b971', '#f9c74f', '#ee6c4d', '#c94c4c', '#589a8e', '#a381b5', '#f8961e', '#4f5d75', '#6b5b95', '#9b59b6', '#b5e7a0', '#a2b9bc', '#b2ad7f', '#679436', '#878f99', '#c7b8ea', '#6f9fd8', '#d64161', '#f3722c', '#f9a828', '#ff7b25', '#7f7f7f']


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
    fig = make_subplots(rows = 1 , cols = 2 , subplot_titles=('countplot','percentage'), specs=[[{"type": "xy"}, {'type': 'domain'}]])
    y = df[column].value_counts().values
    x = df[column].value_counts().index


    

    fig.add_trace(go.Bar(x = x[0:unique_count],
                         y = y[0:unique_count],
                         textposition='auto',
                         marker = dict(
                                        color = colors, 
                                        line = dict(color = 'black',width = 0.1))
                         ),row = 1 ,col = 1)
    
    fig.add_trace(go.Pie(values = x[0:unique_count] ,
                    labels=x[0:unique_count],       
                    textposition='auto',
                    hoverinfo='label',
                    
                    ),row = 1 , col = 2)
    

    fig.update_layout(
        title = {'text' : f'Distribution of the {column}',
                 'y' : 0.9,
                 'x' : 0.5,
                 'xanchor' : 'center',
                  'yanchor' : 'top'},
                  template = 'plotly_dark')
    
    st.plotly_chart(fig)
    st.text( df[column].value_counts().index[:unique_count])


def type_of_movie(df):
    selected_type = st.selectbox('select type of movie' , [i for i in df['genre'].unique()])
    type_movie = df[df['genre'] == selected_type]
    st.dataframe(type_movie)

distrobox = st.checkbox('Distroplot for columns')
if distrobox == 1:
    distribution(df)

type_of_movie(df)
st.dataframe(df.year.value_counts())

def compare_multi_column(df):
    layout = dict(title = 'age and Number of Children vs Income', xaxis = dict(title = 'Income' , ticklen = 5))
    list_to_plot = []
    fig = dict(layout = layout)

    for c ,i in enumerate(sorted(df.year.value_counts().index[0:11] , reverse=True)):
        checkbox = st.checkbox(str(i))
        if checkbox:
            variable_name = f"{i}"
            locals()[variable_name] = go.Scatter(
                x = df[df.year == i]['budget_x'] ,
                y = df[df.year == i]['revenue'] ,
                mode = 'markers',
                name = f'{i}',
                marker = dict(color = colors[c]))
            
            list_to_plot.append(locals()[variable_name])
    try:
        fig.update({'data' : list_to_plot  })
        st.plotly_chart(fig)
    except:
        st.text('choose 5 ')
comapre_with_year = st.checkbox('compare budget_x and revenue with years')
if comapre_with_year:
    compare_multi_column(df)