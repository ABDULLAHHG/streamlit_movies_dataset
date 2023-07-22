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



# Scatter plot time VS Budget and Revenue 
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
def distribution (df):
    # Select column to plot 
    column = st.selectbox('select column' , [i for i in df.columns if i != 'names'])

    # Min and Max 
    min_index = st.slider("Minimum value:", 0, (len(df[column].value_counts())+1)//2 , 0)
    max_index = st.slider("Maximum value:", min_index, len(df[column].value_counts())+1 , (len(df[column].value_counts())+1)//2)

    # Define color palette
    colors = sns.color_palette('deep',n_colors=max_index-min_index).as_hex()
    
    # create a checkbox widget labeled 'Pie Chart' with a default value of 1
    Pie = st.checkbox('Pie Chart',1)


    # Create subplot of 1X2 row = 1 and col = 2 
    if Pie:
        fig = make_subplots(rows = 1 , cols = 2 , subplot_titles=('countplot','percentage'), specs=[[{"type": "xy"}, {'type': 'domain'}]])
    else:
        fig = make_subplots(rows = 1 , cols = 1 , subplot_titles=['Countplot'])
    
    y = df[column].value_counts().values
    x = df[column].value_counts().index


    
    # Bar Plot
    fig.add_trace(go.Bar(x = x[min_index:max_index],
                         y = y[min_index:max_index],
                         textposition='auto',
                         marker = dict(
                                        color = colors, 
                                        line = dict(color = 'black',width = 0.1))
                         ),row = 1 ,col = 1)
    if Pie:
    # Piechart Plot
        fig.add_trace(go.Pie(values = y[min_index:max_index] ,
                        labels=x[min_index:max_index],       
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
    st.text( df[column].value_counts().index[min_index:max_index])

# Not being used Right now 
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

# plot profit for each movies type 
def profit_movies_type(df):
    # split the genre into deblicate rows 
    df.genre = df.genre.str.split(',') 
    df = df.explode('genre')
    df.genre = df.genre.str.strip() 

    # Group by genre and use sum for total Revenue and Budget for each movies type 
    total_sales = df.groupby('genre').sum()

    # make 1X1 plot to make Revenue and Budget in same plot 
    fig = make_subplots(rows = 1 , cols = 1)

    # Bar for Budget
    fig.add_trace(go.Bar(
               x = total_sales.index,
               y = total_sales.budget_x,
               name = 'Budget'         
    ),row = 1 ,col = 1)

    # Bar for Revenue
    fig.add_trace(go.Bar(
               x = total_sales.index,
               y = total_sales.revenue,
               name = 'Revenue'         
    ),row = 1 ,col = 1)

    # Set layout of the plot 
    fig.update_layout(
                height = 600,
                width = 800,
                title = 'Movie Genre Analysis: Comparing Total Revenue and Budget',
                title_x = 0.185,
                xaxis_title = 'Movie Genres',
                yaxis_title = 'Revenue and Budget'
    )

    # Show plot 
    st.plotly_chart(fig)

def genre_count(df , selected_df):
    # split the genre into deblicate (df)
    df.genre = df.genre.str.split(',') 
    df = df.explode('genre')
    df.genre = df.genre.str.strip() 

    # split the genre into deblicate rows (selected_df)
    selected_df.genre = selected_df.genre.str.split(',') 
    selected_df = selected_df.explode('genre')
    selected_df.genre = selected_df.genre.str.strip() 



    fig = make_subplots(rows = 1 ,cols = 1)
    
    # Bar for Budget
    fig.add_trace(go.Bar(
               x = df.genre.value_counts().index,
               y = selected_df.genre.value_counts().values,
               name = str(selected_df.year[0])         
    ),row = 1 ,col = 1)

    # Bar for Revenue
    fig.add_trace(go.Bar(
               x = df.genre.value_counts().index,
               y = df.genre.value_counts().values,
               name = 'All Years'         
    ),row = 1 ,col = 1)

    # Set layout of the plot 
    fig.update_layout(
                height = 600,
                width = 800,
                title = f'Movie Genre Analysis: Genre counts VS {str(selected_df.year[0]) } VS All Years',
                title_x = 0.185,
                xaxis_title = 'Movie Genres',
                yaxis_title = 'counts'
    )
    # Show plot 
    st.plotly_chart(fig) 


def choose_dataframe(df):

    # SideBar 
    st.sidebar.header('User Input Feature')
    selected_year = st.sidebar.selectbox('Year' , reversed(sorted(df.year.unique())))
    
    # SideBar - Type of Movies Selection
    unique_values : list = df[df.year == selected_year]['genre'].str.split(',').explode().str.split().explode().unique()
    multi_selected_movies : list = st.sidebar.multiselect('Movies' ,unique_values,unique_values)
    pattern_movies : str = '|'.join(multi_selected_movies)
    selected_df = df[(df.year == selected_year) & (df.genre.str.contains(pattern_movies))]
    
    # SideBar - Country Selection
    country = sorted(df.country.unique())
    multi_selected_country : list = st.sidebar.multiselect('Countries ' ,country,country)
    pattern_country : str = '|'.join(multi_selected_country)
    selected_df = selected_df[(selected_df.country.str.contains(pattern_country))]
    
    # Header
    st.header('Streamlit movies EDA')
    
    # SubHeader 1 
    st.subheader('User Input Dataset  (User Input Feature) ')

    # Show DataFrame
    st.text(f'rows : {selected_df.shape[0]} \tcolmns: {selected_df.shape[1]}') 
    st.dataframe(selected_df.sort_index())


    # SubHeader 2 
    st.subheader('Plots')

    # Distroplot for Selection DataFrame 
    distrobox : bool = st.checkbox('Distroplot for columns (User Input Feature)')
    if distrobox == 1:
        distribution(selected_df)

    # Scatter plot for Selection DataFrame
    scat : bool = st.checkbox('Scatter Plot (User Input Feature)')
    if scat:
        scatter(selected_df)

    # Revenue VS budget VS Movies-Type plot for Selection DataFrame
    Bar : bool = st.checkbox('Revenue VS budget VS Movies-Type (User Input Feature)')
    if Bar:
        profit_movies_type(selected_df)

        
    # Genre counts VS selected year vs all year plot 
    count_genre_bool : bool = st.checkbox(f'Movie Genre Analysis: Genre counts VS {str(selected_df.year[0]) } VS All Years')
    if count_genre_bool:    
        genre_count(df,selected_df)
    




choose_dataframe(df)


# comapre_with_year : bool = st.checkbox('compare budget_x and revenue with years')
# if comapre_with_year:
#     compare_multi_column(df)

# Revenue VS budget VS Movies-Type plot
RVSB_full_data : bool = st.checkbox('Revenue VS budget VS Movies-Type')
if RVSB_full_data:
    profit_movies_type(df)    







