import pandas as pd
import streamlit as st 
import numpy as np 
import plotly.graph_objects as go 
from plotly.subplots import make_subplots 
import seaborn as sns 


# Read Dataset
df = pd.read_csv('imdb_movies.csv')
df = df.dropna()


df['date_x'] = pd.to_datetime(df['date_x']) 
df['year'] = df['date_x'].dt.year
df = df.set_index('date_x')


 









# Scatter plot for 
def scatter(df):
    # Define color palette
    colors = sns.color_palette('deep',n_colors=2).as_hex()

    # resize data choose only first 100 
    df =df.sort_values(by = 'budget_x',ascending = False )


    # Create first Scatter for Budget
    trace1 = go.Scatter(
                        x = df.index,
                        y = df.budget_x,
                        mode = 'markers',
                        name = 'budget',
                        marker = dict(color = colors[0]),
                        text = df.names)
    
    # Create second Scatter for Revenue
    trace2 = go.Scatter(
                        x = df.index,
                        y = df.revenue,
                        mode = 'markers',
                        name = 'revenue',
                        marker = dict(color = colors[1]),
                        text = df.names)
    

    data = [trace1 ,trace2]

    # Set the layout of the plot
    layout = dict(title='Budget and Revenue vs Time',
                  xaxis=dict(title='Time Year-Month', ticklen=5, zeroline=False))
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


def distribution (df):
    # Select column to plot 
    column = st.selectbox('select column' , [i for i in df.columns if i != 'names'])

    # min and max for unique silder 
    min_value = st.slider("Minimum value:", 0, (len(df[column].value_counts())+1)//2 , 0)
    max_value = st.slider("Maximum value:", min_value, len(df[column].value_counts())+1 , (len(df[column].value_counts())+1)//2)

    # Define color palette
    colors = sns.color_palette('husl',n_colors=max_value-min_value).as_hex()
    
    # Create subplot of 1X2 row = 1 and col = 2 
    fig = make_subplots(rows = 1 , cols = 2 , subplot_titles=('countplot','percentage'), specs=[[{"type": "xy"}, {'type': 'domain'}]])
    y = df[column].value_counts().values
    x = df[column].value_counts().index


    
    # Bar Plot
    fig.add_trace(go.Bar(x = x[min_value:max_value],
                         y = y[min_value:max_value],
                         textposition='auto',
                         marker = dict(
                                        color = colors, 
                                        line = dict(color = 'black',width = 0.1))
                         ),row = 1 ,col = 1)
    
    # Piechart Plot
    fig.add_trace(go.Pie(values = y[min_value:max_value] ,
                    labels=x[min_value:max_value],       
                    textposition='auto',
                    hoverinfo='label',
                    
                    marker = dict(colors = colors)),row = 1 , col = 2)
    
    # Update Bar remove its legend 
    fig.update_traces(col = 1,row =1 ,showlegend=False)

    fig.update_layout(
        title = {'text' : f'Distribution of the {column}',
                 'y' : 0.9,
                 'x' : 0.5,
                 'xanchor' : 'center',
                  'yanchor' : 'top'},
                  template = 'plotly_dark',
                  height = 600,
                  width = 800
                  
                  )
    
    st.plotly_chart(fig)
    st.text( df[column].value_counts().index[min_value:max_value])


def compare_multi_column(df):
    # Define color palette
    colors = sns.color_palette('deep',n_colors=10).as_hex()

    # Define layout of the plot
    layout = dict(title='Revenue vs Income',
              height=600,
              width=800,
              xaxis=dict(title='Income', ticklen=5),
              yaxis=dict(title='Revenue', ticklen=5))
    
    # Create dictionary to store plots
    plots = {}

    fig = dict(layout = layout)
    
    # Iterate over the top 10 most frequent values in the `year` column
    for i, year in zip(range(10), sorted(df.year.value_counts().index[:10], reverse=True)):
        checkbox = st.checkbox(str(year))
        if checkbox:
        # Create plot and add to dictionary
            plots[year] = go.Scatter(x=df[df.year == year]['budget_x'],
                                 y=df[df.year == year]['revenue'],
                                 mode='markers',
                                 name=str(year),
                                 marker=dict(color=colors[i]))
            
    # Create list of plots to display
    list_to_plot = list(plots.values())

    # Create figure with layout and list of plots
    fig = dict(layout=layout, data=list_to_plot)

    # Display plot if at least one checkbox is selected
    if len(plots) > 0:
        st.plotly_chart(fig)
    else:
        st.text('Choose a year to display')


def choose_dataframe(df):

    # SideBar 
    st.sidebar.header('User Input Feature')
    selected_year = st.sidebar.selectbox('Year' , reversed(sorted(df.year.unique())))
    
    # SideBar - type of movies selection
    unique_values : list = df[df.year == selected_year]['genre'].str.split(',').explode().str.split().explode().unique()
    multi_selected_movies : list = st.sidebar.multiselect('Movies' ,unique_values,unique_values)
    pattern_movies : str = '|'.join(multi_selected_movies)
    selected_df = df[(df.year == selected_year) & (df.genre.str.contains(pattern_movies))]
    
    # SideBar - country selection
    country = sorted(df.country.unique())
    multi_selected_country : list = st.sidebar.multiselect('Countries ' ,country,country)
    pattern_country : str = '|'.join(multi_selected_country)
    selected_df = selected_df[(selected_df.country.str.contains(pattern_country))]
    
    # Header
    st.header('Streamlit movies EDA')
    
    # text 
    st.subheader('User Input Dataset  (User Input Feature) ')

    # Show DataFrame
    st.text(f'rows : {selected_df.shape[0]} \tcolmns: {selected_df.shape[1]}') 
    st.dataframe(selected_df.sort_index())


    # subheader 2 
    st.subheader('Plots')

    # Distroplot for selection dataframe 
    distrobox : bool = st.checkbox('Distroplot for columns (User Input Feature)')
    if distrobox == 1:
        distribution(selected_df)

    # Scatter plot for selection dataframe
    scat : bool = st.checkbox('Scatter Plot (User Input Feature)')
    if scat:
        scatter(selected_df)






choose_dataframe(df)

comapre_with_year : bool = st.checkbox('compare budget_x and revenue with years')
if comapre_with_year:
    compare_multi_column(df)









