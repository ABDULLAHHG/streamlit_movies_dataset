import pandas as pd
import streamlit as st 
import numpy as np 
import plotly.graph_objects as go 
from plotly.subplots import make_subplots 
import colorlover as cl
import plotly.colors as plc
import colorsys



# Define the number of colors needed (up to 20,000)
num_colors = 20000

# Generate the color palette
color_palette = plc.qualitative.Plotly * (num_colors // len(plc.qualitative.Plotly) + 1)

# Trim the color palette to the desired number of colors
color_palette = color_palette[:num_colors]

df = pd.read_csv('imdb_movies.csv')
df = df.dropna()
df['date_x'] = pd.to_datetime(df['date_x']) 
df['year'] = df['date_x'].dt.year
df = df.set_index('date_x')




colors = ['#7c90db', '#92a8d1', '#a5c4e1', '#f7cac9', '#fcbad3', '#e05b6f', '#f8b195', '#f5b971', '#f9c74f',
          '#ee6c4d', '#c94c4c', '#589a8e', '#a381b5', '#f8961e', '#4f5d75', '#6b5b95', '#9b59b6', '#b5e7a0',
          '#a2b9bc', '#b2ad7f', '#679436', '#878f99', '#c7b8ea', '#6f9fd8', '#d64161', '#f3722c', '#f9a828',
          '#ff7b25', '#7f7f7f']

colors.append(color_palette)


# Scatter plot for 
def scatter(df):
    df =df.sort_values(by = 'budget_x',ascending = False )
    df = df.iloc[:100,:]
    trace1 = go.Scatter(
                        x = df.index,
                        y = df.budget_x,
                        mode = 'markers',
                        name = 'budget',
                        marker = dict(color = colors[0]),
                        text = df.names)
    
    trace2 = go.Scatter(
                        x = df.index,
                        y = df.revenue,
                        mode = 'markers',
                        name = 'revenue',
                        marker = dict(color = colors[1]),
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
    
    fig.add_trace(go.Pie(values = y[0:unique_count] ,
                    labels=x[0:unique_count],       
                    textposition='auto',
                    hoverinfo='label',
                    
                    marker = dict(colors = colors)),row = 1 , col = 2)
    

    fig.update_layout(
        title = {'text' : f'Distribution of the {column}',
                 'y' : 0.9,
                 'x' : 0.5,
                 'xanchor' : 'center',
                  'yanchor' : 'top'},
                  template = 'plotly_dark')
    
    st.plotly_chart(fig)
    st.text( df[column].value_counts().index[:unique_count])


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


def choose_dataframe(df):

    # SideBar 
    st.sidebar.header('User Input Feature')
    selected_year = st.sidebar.selectbox('Year' , reversed(sorted(df.year.unique())))
    
    # SideBar - type of movies selection
    unique_values = df[df.year == selected_year]['genre'].str.split(',').explode().str.split().explode().unique()
    selected_unique = st.sidebar.multiselect('Type Of Movies' ,unique_values,unique_values)
    pattern = '|'.join(selected_unique)
    selected_df = df[(df.year == selected_year) & (df.genre.str.contains(pattern))]
    
    # Show DataFrame
    st.text(f'rows : {selected_df.shape[0]} \tcolmns: {selected_df.shape[1]}') 
    st.dataframe(selected_df)




    # Distroplot for selection dataframe 
    distrobox = st.checkbox('Distroplot for columns')
    if distrobox == 1:
        distribution(selected_df)






choose_dataframe(df)

comapre_with_year : bool = st.checkbox('compare budget_x and revenue with years')
if comapre_with_year:
    compare_multi_column(df)






# Scatter plot for selection dataframe
scat : bool = st.checkbox('Scatter Plot')
if scat:
    scatter(df)


