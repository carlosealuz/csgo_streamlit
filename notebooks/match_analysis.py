import streamlit as st
import numpy as np
import pandas as pd
import pickle
import time
from matplotlib import pyplot as plt
from  matplotlib.ticker import FuncFormatter
import seaborn as sns
import plotly.express as px

st.set_page_config(layout="wide")

types = ["Mean","Absolute","Median","Maximum","Minimum"]

# Load players dataframe.
players_data = pd.read_csv('../data/data_scrapped.csv')
players_data.drop('Unnamed: 0', axis=1, inplace=True)
players_data['GAME_DATE'] = pd.to_datetime(players_data['GAME_DATE'], format='%d/%m/%Y %H:%M')
players_data['MONTH_YR'] = players_data['GAME_DATE'].dt.strftime('%m/%Y')
#filter sa players
sa_players = ['rebores', 'urielton', "t'challa", 'bemol', 'Puff']
players_data = players_data[players_data['NAME'].isin(sa_players)]

players = players_data.NAME.unique().tolist()



# Load games dataframe
team_data = pd.read_csv('../data/games_clean.csv')
team_data.drop('Unnamed: 0', axis=1, inplace=True)
team_data['GAME_DATE'] = pd.to_datetime(team_data['GAME_DATE'], format='%d/%m/%Y %H:%M')
team_data['MONTH_YR'] = team_data['GAME_DATE'].dt.strftime('%m/%Y')

maps = team_data.map.unique().tolist()

def filter_teams(df_data):
    df_filtered_team = pd.DataFrame()
    if all_teams_selected == 'Select teams manually (choose below)':
        df_filtered_team = df_data[df_data['team'].isin(selected_teams)]
        return df_filtered_team
    return df_data

def get_unique_teams(df_data):
    unique_teams = np.unique(df_data.team).tolist()
    return unique_teams

def return_mean_data(df, col):
    if df[col].mean() not in ['nan', np.nan]:
        return round(df[col].mean(), 2)
    else:
        return None

def return_delta_rounded(data1, data2):
    return round(data1 - data2, 2)

def return_pct_win_per_map_per_month(df):
    victories_per_map_per_month = df.groupby(['MONTH_YR', 'result', 'map'])['result'].count().reset_index(name='games_played')
    return victories_per_map_per_month[['MONTH_YR', 'result', 'map', 'games_played']]

def plot_map_data(df, map):
    fig = px.bar(df.query(f'map == "{map}"'), x='MONTH_YR', y='games_played', color='result', barmode='stack', text='games_played',
                title=f"Resultados por mês - {map}", color_discrete_map={'V':'green', 'D':'red'})
    fig.update_layout(yaxis_visible=False, yaxis_showticklabels=False, xaxis_title='Data')
    fig.update_xaxes(categoryorder='array', categoryarray= ['01/2022', '02/2022', '03/2022', '04/2022', '05/2022', '06/2022',
                                                            '07/2022', '08/2022', '09/2022', '10/2022', '11/2022', '12/2022'])
    return fig

def filter_season(df_data):
    dates = df_data.GAME_DATE.dt.date.unique().tolist()
    dates = [min(dates), max(dates)]

    if len(selected_date) == 1:
            selected_date = [selected_date[0], max(dates)]
    
    df_filtered_season = df_data[(df_data['GAME_DATE'].dt.date.between(selected_date[0], selected_date[1])) &
                                (df_data['map'].isin(['inferno']))]
    
    return df_filtered_season

####################
### INTRODUCTION ###
####################

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('BuLiAn - Bundesliga Analyzer')
with row0_2:
    st.text("")
    st.subheader('Streamlit App by [Tim Denzler](https://www.linkedin.com/in/tim-denzler/)')
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("Hello there! Have you ever spent your weekend watching the German Bundesliga and had your friends complain about how 'players definitely used to run more' ? However, you did not want to start an argument because you did not have any stats at hand? Well, this interactive application containing Bundesliga data from season 2013/2014 to season 2019/2020 allows you to discover just that! If you're on a mobile device, I would recommend switching over to landscape for viewing ease.")
    st.markdown("You can find the source code in the [BuLiAn GitHub Repository](https://github.com/tdenzl/BuLiAn)")
    st.markdown("If you are interested in how this app was developed check out my [Medium article](https://tim-denzler.medium.com/is-bayern-m%C3%BCnchen-the-laziest-team-in-the-german-bundesliga-770cfbd989c7)")
    
def get_unique_matchdays(df_data):
    #returns minimum and maximum
    dates = df_data.GAME_DATE.dt.date.unique().tolist()
    return [min(dates), max(dates)]


### SEASON RANGE ###
st.sidebar.markdown("**Selecione qual analise deseja fazer:** 👇")
stats_selected = st.sidebar.radio(label='', options=("Time", "Jogadores"))
start_season, end_season = get_unique_matchdays(players_data)

selected_date = st.sidebar.date_input('Select the season range you want to include', [start_season, end_season])
if stats_selected == 'Jogadores':
    df_data_filtered_season = filter_season(players_data)
if stats_selected == 'Time':
    df_data_filtered_season = filter_season(team_data)             





# Sidebar
# Using object notation

# with st.sidebar:
#     stats_selected = st.radio(
#         "Selecione as estatísticas desejadas:",
#         ("Time", "Jogadores")
#     )
#     if stats_selected == 'Jogadores':
#         selected_player = st.selectbox('Selecione o jogador:', players)
#         selected_date = st.date_input('Selecione o período:', dates)
#         if len(selected_date) == 1:
#             selected_date = [selected_date[0], max(dates)]
#     else:
#         selected_date = st.date_input('Selecione o período:', dates)
        
#         selected_map = st.multiselect('Selecione o mapa:', maps, default=maps)
#         if len(selected_map) == 0:
#             selected_map = maps

# if stats_selected == 'Jogadores':
#     '''
#     to do:
#     adicionar comparativo nas medias dos jogadores com periodos anteriores
#     adicionar estatisticas dos jogadores por mapa
    
#     '''
#     st.subheader(f'Performance de: {selected_player}')
    
#     query = f"NAME=='{selected_player}'"
#     df_filtered = players_data[(players_data['NAME']==selected_player) & 
#                     (players_data['GAME_DATE'].dt.date.between(selected_date[0], selected_date[1]))]

#     filtered_player_full_data = players_data[players_data['NAME']==selected_player]
    
#     mean_filtered_adr = return_mean_data(df_filtered, 'ADR')
#     mean_full_adr = return_mean_data(filtered_player_full_data, 'ADR')
#     mean_filtered_kdr = return_mean_data(df_filtered, 'KDR')
#     mean_full_kdr = return_mean_data(filtered_player_full_data, 'KDR')
    
#     col1, col2 = st.columns(2)
#     with col1:
#         st.metric('Média ADR', mean_filtered_adr, 
#                   delta=return_delta_rounded(mean_filtered_adr, mean_full_adr))
#     with col2:
#         st.metric('Média KDR', mean_filtered_kdr,
#                   delta=return_delta_rounded(mean_filtered_kdr, mean_full_kdr))


#     st.dataframe(df_filtered)

# else:
#     '''
#     to do:
#     adicionar diff per map nas vitorias e derrotas

#     '''
    
    

#     df_wins_per_map = return_pct_win_per_map_per_month(df_filtered)
    
#     col1, col2 = st.columns(2)
#     with col1:
#         st.plotly_chart(plot_map_data(df_wins_per_map, 'mirage'))
#     with col2:
#         st.plotly_chart(plot_map_data(df_wins_per_map, 'inferno'))
    
#     col1, col2 = st.columns(2)
#     with col1:
#         st.plotly_chart(plot_map_data(df_wins_per_map, 'nuke'))
#     with col2:
#         st.plotly_chart(plot_map_data(df_wins_per_map, 'overpass'))
    
        

    
    

    
#     st.dataframe(df_filtered)