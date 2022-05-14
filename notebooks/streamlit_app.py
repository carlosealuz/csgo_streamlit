import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
import os

cwd = os.getcwd()
print(cwd)
st.set_page_config(layout="wide")


color_dict = {'V': '#00cc66', 'D':'#8c0303'}

def plot_diff_per_game(df_plot, map): #total #against, #conceived
    rc = {'figure.figsize':(10,5),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'white',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 12,
          'font.weight': 'bold',
          'axes.labelsize': 18,
          'xtick.labelsize': 14}
    
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    
    df_plot = df_plot.query(f'map=="{map}"')
    df_plot['GAME_DATE'] = df_plot['GAME_DATE'].dt.strftime('%m-%d %H:%M')
    df_plot = df_plot.sort_values('GAME_DATE')
    #df_plot['date_plt'] = df_plot['GAME_DATE'].dt.strftime('%y-%m-%d %H:%M')
    colors = ['g' if c >= 0 else 'r' for c in df_plot.score_diff]
    ax = sns.barplot(x="GAME_DATE", y='score_diff', data=df_plot, palette = colors)
    ax.set(xlabel = "Data")
    #x_dates = df_plot['GAME_DATE'].dt.strftime('%m-%d %H:%M').sort_values().unique()
    ax.set_xticklabels(labels=df_plot['GAME_DATE'], rotation=45, ha='right') 
    
    for p in ax.patches:
        ax.annotate(str(format(p.get_height(), '.0f')), 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center',
                va = 'center', 
                xytext = (0, 18),
                rotation = 0,
                textcoords = 'offset points')

    ax.set(ylabel=None)  # remove the y-axis label
    ax.tick_params(left=False)  # remove the ticks
    ax.axes.yaxis.set_ticklabels([]) # remove values
    st.pyplot(fig)

def plot_mean_per_player(df_plot, metric):
    rc = {'figure.figsize':(8,3.0),
            'axes.facecolor':'#0e1117',
            'axes.edgecolor': '#0e1117',
            'axes.labelcolor': 'white',
            'figure.facecolor': '#0e1117',
            'patch.edgecolor': '#0e1117',
            'text.color': 'white',
            'xtick.color': 'white',
            'ytick.color': 'white',
            'grid.color': 'grey',
            'font.size' : 12,
            'font.weight': 'bold',
            'axes.labelsize': 18,
            'xtick.labelsize': 14}

    plt.rcParams.update(rc)
    fig, ax = plt.subplots()

    df_plot = df_plot.sort_values('GAME_DATE')
    df_plot = df_plot.groupby('MONTH_YR', as_index=False)[metric].mean()
    ax = sns.lineplot(x="MONTH_YR", y=metric, data=df_plot, markers=True, ci=None)
    ax.set(xlabel = "Data")
    plt.xticks(rotation=45,horizontalalignment="right")


    for v in df_plot.iterrows():
        plt.text(v[1][0], v[1][1], f'{round(v[1][1], 2)}')

    ax.set(ylabel=None)  # remove the y-axis label
    ax.tick_params(left=False)  # remove the ticks
    ax.axes.yaxis.set_ticklabels([]) # remove values
    st.pyplot(fig)

def plot_x_per_team(df_plot, map): #total #against, #conceived
    rc = {'figure.figsize':(10,5),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'white',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 12,
          'font.weight': 'bold',
          'axes.labelsize': 18,
          'xtick.labelsize': 14}
    
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    
    df_plot = df_plot.query(f'map=="{map}"')
    ax = sns.barplot(x="MONTH_YR", y='games_played', data=df_plot, palette = color_dict, hue = "result")
    ax.set(xlabel = "Data")
    plt.xticks(rotation=0,horizontalalignment="center")
    #plt.title(f'Resultado por mês - {map}')
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.0f'), 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center',
                va = 'center', 
                xytext = (0, 18),
                rotation = 0,
                textcoords = 'offset points')

    ax.set(ylabel=None)  # remove the y-axis label
    ax.tick_params(left=False)  # remove the ticks
    ax.axes.yaxis.set_ticklabels([]) # remove values
    st.pyplot(fig)

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

def pct_wins(df, map):
    return round(df.query(f'map=="{map}"')['result'].value_counts(normalize=True)['V'] * 100, 2) 

def write_markdown_title(text, h='h1'):
    st.markdown(f"<{h} style='text-align: center; color: white;'>{text}</{h}>", unsafe_allow_html=True)

def return_markdown_mean(df, col):
    return str(round(df[col].mean(),2))

def return_markdown_comp_hist(df, df_full, col):
    mean = return_markdown_mean(df, col)
    hist = return_markdown_mean(df_full, col)
    diff = float(mean) - float(hist)
    if diff > 0:
        return "⬆️" + str(round(diff,2))
    elif diff < 0:
        return "⬇️" + str(round(diff,2))
    else:
        return "0.0"


st.title('Análise jogos CS:GO')

# Load players dataframe.
players_data = pd.read_csv(cwd+'/data_scrapped.csv')
players_data.drop('Unnamed: 0', axis=1, inplace=True)
players_data['GAME_DATE'] = pd.to_datetime(players_data['GAME_DATE'], format='%d/%m/%Y %H:%M')
players_data['MONTH_YR'] = players_data['GAME_DATE'].dt.strftime('%m/%Y')
#filter sa players
sa_players = ['rebores', 'urielton', 'Anabele de Malhadas', 'bemol', 'Puff']
players_data = players_data[players_data['NAME'].isin(sa_players)]

players = players_data.NAME.unique().tolist()
dates = players_data.GAME_DATE.dt.date.unique().tolist()
dates = [min(dates), max(dates)]


# Load games dataframe
team_data = pd.read_csv(cwd+'/games_clean.csv')
team_data.drop('Unnamed: 0', axis=1, inplace=True)
team_data['GAME_DATE'] = pd.to_datetime(team_data['GAME_DATE'], format='%d/%m/%Y %H:%M')
team_data['MONTH_YR'] = team_data['GAME_DATE'].dt.strftime('%m/%Y')
team_data['OT'] = team_data.apply(lambda x: 'OT' if x['team_score'] >= 15 and x['foe_score'] >= 15 else '', axis=1)
maps = team_data.map.unique().tolist()

# Sidebar
# Using object notation
with st.sidebar:
    stats_selected = st.radio(
        "Selecione as estatísticas desejadas:",
        ("Time", "Jogadores")
    )
    if stats_selected == 'Jogadores':
        selected_player = st.selectbox('Selecione o jogador:', players)
        selected_date = st.date_input('Selecione o período:', dates)
        if len(selected_date) == 1:
            selected_date = [selected_date[0], max(dates)]
    else:
        selected_date = st.date_input('Selecione o período:', dates)
        if len(selected_date) == 1:
            selected_date = [selected_date[0], max(dates)]


if stats_selected == 'Jogadores':
    
    query = f"NAME=='{selected_player}'"
    df_filtered = players_data[(players_data['NAME']==selected_player) & 
                    (players_data['GAME_DATE'].dt.date.between(selected_date[0], selected_date[1]))]

    filtered_player_full_data = players_data[players_data['NAME']==selected_player]

    st.subheader(f'Performance de: {selected_player}')
    
    row16_spacer1, row16_1, row16_2, row16_4 = st.columns((4.6, 1.5, 1.5, 6.1))
    with row16_1:
        st.markdown("**Métrica**")
        st.markdown("🏋🏽‍♀️ KDR")
        st.markdown("🔥 ADR")
        st.markdown("🏹 Kills")
        st.markdown("🏃‍♂️ Assists")
        st.markdown("👻 Deaths")
        st.markdown("🆘 KAST")
        st.markdown("🔁 Trades")
        st.markdown("🖐 Multikill")
        st.markdown("☝ First kill")

    with row16_2:
        st.markdown("**Média período selecionado**")
        st.markdown(" " + return_markdown_mean(df_filtered, 'KDR'))
        st.markdown(" " + return_markdown_mean(df_filtered, 'ADR'))
        st.markdown(" " + return_markdown_mean(df_filtered, 'K'))
        st.markdown(" " + return_markdown_mean(df_filtered, 'A'))
        st.markdown(" " + return_markdown_mean(df_filtered, 'D'))
        st.markdown(" " + return_markdown_mean(df_filtered, 'KAST'))
        st.markdown(" " + return_markdown_mean(df_filtered, 'T'))
        st.markdown(" " + return_markdown_mean(df_filtered, 'MK'))
        st.markdown(" " + return_markdown_mean(df_filtered, 'FK'))
        
    with row16_4:
        st.markdown("**Comparativo com histórico**")
        st.markdown(" "+return_markdown_comp_hist(df_filtered, filtered_player_full_data, 'KDR'))
        st.markdown(" "+return_markdown_comp_hist(df_filtered, filtered_player_full_data, 'ADR'))
        st.markdown(" "+return_markdown_comp_hist(df_filtered, filtered_player_full_data, 'K'))
        st.markdown(" "+return_markdown_comp_hist(df_filtered, filtered_player_full_data, 'A'))
        st.markdown(" "+return_markdown_comp_hist(df_filtered, filtered_player_full_data, 'D'))
        st.markdown(" "+return_markdown_comp_hist(df_filtered, filtered_player_full_data, 'KAST'))
        st.markdown(" "+return_markdown_comp_hist(df_filtered, filtered_player_full_data, 'T'))
        st.markdown(" "+return_markdown_comp_hist(df_filtered, filtered_player_full_data, 'MK'))
        st.markdown(" "+return_markdown_comp_hist(df_filtered, filtered_player_full_data, 'FK'))

    row4_spacer1, row4_1, row4_spacer2, row4_2, row4_spacer3  = st.columns((.2, 3.3, .4, 3.4, .2))
    with row4_1:
        write_markdown_title(f'Evolução do KDR ao longo do tempo')
        plot_mean_per_player(df_filtered, 'KDR')
    with row4_2:
        write_markdown_title('Evolução do ADR ao longo do tempo')
        plot_mean_per_player(df_filtered, 'ADR')

else:
    
    df_filtered = team_data[(team_data['GAME_DATE'].dt.date.between(selected_date[0], selected_date[1])) &
                            (team_data['map'].isin(maps))]

    df_wins_per_map = return_pct_win_per_map_per_month(df_filtered)

    row1_spacer0, row0_1, row0_spacer2, row0_2, row0_spacer3  = st.columns((.2, 3.3, .4, 3.4, .2))
    with row0_1:
        write_markdown_title('Número de vitórias e derrotas por mapa', 'h4')
    with row0_2:
        write_markdown_title('Diferença de score ao final do jogo', 'h4')
        write_markdown_title('Calculado através da subtração do número de rounds que vencemos pelo número de rounds que perdemos', 'p')
    row1_spacer1, row1_1, row1_spacer2, row1_2, row1_spacer3  = st.columns((.2, 3.3, .4, 3.4, .2))
    with row1_1:
        write_markdown_title(f'Mirage - {pct_wins(df_filtered, "mirage")}% vitória')
        plot_x_per_team(df_wins_per_map, 'mirage')
    with row1_2:
        write_markdown_title('Mirage')
        plot_diff_per_game(df_filtered, 'mirage')
    
    row2_spacer1, row2_1, row2_spacer2, row2_2, row2_spacer3  = st.columns((.2, 3.3, .4, 3.4, .2))
    with row2_1:
        write_markdown_title(f'Inferno - {pct_wins(df_filtered, "inferno")}% vitória')
        plot_x_per_team(df_wins_per_map, 'inferno')
    with row2_2:
        write_markdown_title('Inferno')
        plot_diff_per_game(df_filtered, 'inferno')

    row3_spacer1, row3_1, row3_spacer2, row3_2, row3_spacer3  = st.columns((.2, 3.3, .4, 3.4, .2))
    with row3_1:
        write_markdown_title(f'Nuke - {pct_wins(df_filtered, "nuke")}% vitória')
        plot_x_per_team(df_wins_per_map, 'nuke')
    with row3_2:
        write_markdown_title('Nuke')
        plot_diff_per_game(df_filtered, 'nuke')
    
    row4_spacer1, row4_1, row4_spacer2, row4_2, row4_spacer3  = st.columns((.2, 3.3, .4, 3.4, .2))
    with row4_1:
        write_markdown_title(f'Overpass - {pct_wins(df_filtered, "overpass")}% vitória')
        plot_x_per_team(df_wins_per_map, 'overpass')
    with row4_2:
        write_markdown_title('Overpass')
        plot_diff_per_game(df_filtered, 'overpass')

    
