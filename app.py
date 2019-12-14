#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go

# In[2]:


import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table


# In[3]:


def newDataset(file, genre):
    s = file[file['Genre1'] == genre]

    swinner = s[(s['isWinner'] == True) | (s['otherAwards'] == True)]
    sloser = s[(s['isWinner'] == False) & (s['otherAwards'] == False)]
    return s, swinner, sloser


# In[4]:

def drop_contenders_new(file, contenders, drop=True):
    if drop == True:
        newfile = file.drop(contenders.index, axis=0)
    else:
        newindex = [index for index in contenders.index if index in file.index]
        newfile = file.loc[newindex]
    return newfile


# In[6]:


def outliers(file, feature):
    Q1 = file[feature].quantile(0.25)
    Q3 = file[feature].quantile(0.75)
    IQR = Q3 - Q1
    outlier = file[(file[feature] > Q3 + 1.5 * IQR) & (file[feature] < Q1 - 1.5 * IQR)]
    removed = file[(file[feature] <= Q3 + 1.5 * IQR) & (file[feature] >= Q1 - 1.5 * IQR)]
    return outlier, removed


# In[7]:


def cal_mean(dataset, feature, r=0):
    mean = round(np.nanmean(dataset[feature]), r)
    return mean


# In[9]:


with open('combinedata.json') as json_file:
    combine = json.load(json_file)

with open('otherGenre.json') as json_file:
    otherGenre = json.load(json_file)

with open('allOptions.json') as json_file:
    all_options = json.load(json_file)

# In[10]:

feature = 'AdjustedTotalGross'

# In[11]:


sundance = pd.read_csv('Sundance_data.csv', index_col='tconst')
tribeca = pd.read_csv('Tribeca_data.csv', index_col='tconst')
chicago = pd.read_csv('Chicago_data.csv', index_col='tconst')
berlin = pd.read_csv('Berlin_data.csv', index_col='tconst')
rotterdam = pd.read_csv('Rotterdam_data.csv', index_col='tconst')
cannes = pd.read_csv('Cannes_data.csv', index_col='tconst')
venice = pd.read_csv('Venice_data.csv', index_col='tconst')
sxsw = pd.read_csv('SXSW_data.csv', index_col='tconst')
seattle = pd.read_csv('Seattle_data.csv', index_col='tconst')
san = pd.read_csv('SanFrancisco_data.csv', index_col='tconst')
slam = pd.read_csv('Slamdance_data.csv', index_col='tconst')
locarno = pd.read_csv('Locarno_data.csv', index_col='tconst')
sitges = pd.read_csv('Sitges_data.csv', index_col='tconst')
toronto = pd.read_csv('Toronto_data.csv', index_col='tconst')
kv = pd.read_csv('KarlovyVary_data.csv', index_col='tconst')
hongkong = pd.read_csv('HongKong_data.csv', index_col='tconst')
torino = pd.read_csv('Torino_data.csv', index_col='tconst')
austin = pd.read_csv('Austin_data.csv', index_col='tconst')
marrakech = pd.read_csv('Marrakech_data.csv', index_col='tconst')
tokyo = pd.read_csv('Tokyo_data.csv', index_col='tconst')
goldenhorse = pd.read_csv('GoldenHorse_data.csv', index_col='tconst')
buenosaires = pd.read_csv('BuenosAires_data.csv', index_col='tconst')
gramado = pd.read_csv('Gramado_data.csv', index_col='tconst')
cairo = pd.read_csv('Cairo_data.csv', index_col='tconst')
havana = pd.read_csv('Havana_data.csv', index_col='tconst')
rio = pd.read_csv('Rio_data.csv', index_col='tconst')
saopaulo = pd.read_csv('SaoPaulo_data.csv', index_col='tconst')
asiapacific = pd.read_csv('AsiaPacific_data.csv', index_col='tconst')
india = pd.read_csv('India_data.csv', index_col='tconst')
sydney = pd.read_csv('Sydney_data.csv', index_col='tconst')
beijing = pd.read_csv('Beijing_data.csv', index_col='tconst')
tokyof = pd.read_csv('TokyoF_data.csv', index_col='tconst')
aafca = pd.read_csv('AAFCA_data.csv', index_col='tconst')
brisbane = pd.read_csv('Brisbane_data.csv', index_col='tconst')
jerusalem = pd.read_csv('Jerusalem_data.csv', index_col='tconst')
grandbell = pd.read_csv('GrandBell_data.csv', index_col='tconst')
haifa = pd.read_csv('Haifa_data.csv', index_col='tconst')
fajr = pd.read_csv('Fajr_data.csv', index_col='tconst')
singapore = pd.read_csv('Singapore_data.csv', index_col='tconst')
yamagata = pd.read_csv('Yamagata_data.csv', index_col='tconst')
shanghai = pd.read_csv('Shanghai_data.csv', index_col='tconst')
taormina = pd.read_csv('Taormina_data.csv', index_col='tconst')
london = pd.read_csv('London_data.csv', index_col='tconst')
sansebastian = pd.read_csv('SanSebastian_data.csv', index_col='tconst')
moscow = pd.read_csv('Moscow_data.csv', index_col='tconst')
mannheimheidelberg = pd.read_csv('MannheimHeidelberg_data.csv', index_col='tconst')
thessaloniki = pd.read_csv('Thessaloniki_data.csv', index_col='tconst')
taipei = pd.read_csv('Taipei_data.csv', index_col='tconst')
edinburgh = pd.read_csv('Edinburgh_data.csv', index_col='tconst')
kerala = pd.read_csv('Kerala_data.csv', index_col='tconst')
jeonju = pd.read_csv('Jeonju_data.csv', index_col='tconst')

newbo = pd.read_csv('filmDataset_forDashBoard.csv', index_col='tconst')

# In[33]:


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server


# In[34]:

def build_banner():
    return html.Div(
        id='banner',
        className='banner',
        children=[
            html.Div(
                id='banner-text',
                children=[
                    html.H4('FILM FESTIVAL DATA DASHBOARD'),
                    html.H6('Box Office Visualization and Comparision'),
                ]
            ),
            html.Div(
                id='banner-logo',
                children=[
                    html.Img(id='logo', src=app.get_asset_url('logo.png')),
                ]
            )
        ]
    )


app.layout = html.Div(id='big-app-container', children=[
    build_banner(),

    html.Div([
        html.Div([
            html.Div([
                html.H6('Box Office Comparison', style={'font-weight': 'bold'}),
                html.P('Continent', style={'fontSize': 18}),
                html.Div([
                    dcc.Dropdown(
                        id='continent',
                        options=[
                            {'label': 'Asia', 'value': 'Asia'},
                            {'label': 'Africa', 'value': 'Africa'},
                            {'label': 'North America', 'value': 'NorthAmerica'},
                            {'label': 'South America', 'value': 'SouthAmerica'},
                            {'label': 'Europe', 'value': 'Europe'},
                            {'label': 'Australia', 'value': 'Australia'}
                        ],
                        placeholder='Select a continent',
                        value='Asia',
                        className='continent-dropdown'
                    )
                ]),
                html.P('Film Festival', style={'fontSize': 18}),
                html.Div([
                    dcc.Dropdown(
                        id='festival',
                        placeholder='Select a film festival',
                        className='festival-dropdown'
                    )
                ]),
                html.Div([
                    html.P(
                        '*The green cell indicates a significant increase while the red cell indicates a significant '
                        'decrease',
                        style={'color': '#66A5AD', 'fontSize': 14}),
                    html.P(id='note', style={'fontSize': 14, 'color': '#C4DFE6'}),
                ],
                    className='word-wrap')
            ],
                className='pretty_container four columns'),

            html.Div([
                dash_table.DataTable(
                    id='table',
                    columns=[
                        {'name': ['', 'Genre'], 'id': 'genre'},
                        {'name': ['Non-Contenders', 'Box Office'], 'id': 'others'},
                        {'name': ['Contenders', 'Average Box Office'], 'id': 'contendersbo'},
                        {'name': ['Contenders', 'Difference'], 'id': 'contendersdiff'},
                        {'name': ['Nominees', 'Average Box Office'], 'id': 'losersbo'},
                        {'name': ['Nominees', 'Difference'], 'id': 'losersdiff'},
                        {'name': ['Winners', 'Average Box Office'], 'id': 'winnersbo'},
                        {'name': ['Winners', 'Difference'], 'id': 'winnersdiff'},
                    ],
                    merge_duplicate_headers=True,
                    sort_action='native',
                    style_header={
                        'backgroundColor': '#1e2130',
                        'fontWeight': 'bold',
                        'fontSize': 12,
                        'font-family': 'Arial',
                        'textAlign': 'left',
                        'color': '#f3f5f4',
                        'border': '0px',
                        'borderBottom': '1px solid white'
                    },
                    style_cell={
                        'backgroundColor': '#1e2130',
                        'font-family': 'Arial',
                        'fontSize': 12,
                        'textAlign': 'left',
                        'color': '#f3f5f4',
                    },
                    style_data={'border': '0px'},
                    style_as_list_view=True,
                )
            ],
                className='pretty_container eight columns')
        ]),
    ]),

    html.Div([
        html.Div([
            html.H6('By Genre'),
            html.Div([
                dcc.Tabs(
                    id='genre',
                    value='Others',
                    className='custom-tabs',
                )
            ])
        ],
            className='pretty_container twelve columns'),

        html.Div([
            html.Div([
                dcc.Graph(id='boxplot'),
            ],
                className='pretty_container six columns'),

            html.Div([
                dcc.Graph(id='barchart'),
            ],
                className='pretty_container six columns')
        ]),
    ]),

])


@app.callback(
    [Output('festival', 'options'),
     Output('festival', 'value')],
    [Input('continent', 'value')]
)
def choose_festival(continent):
    options = []
    value = 'Beijing'
    if continent == 'Asia':
        options = [
            {'label': 'Beijing International Film Festival', 'value': 'Beijing'},
            {'label': 'Shanghai International Film Festival', 'value': 'Shanghai'},
            {'label': 'Golden Horse Film Festival', 'value': 'GoldenHorse'},
            {'label': 'Hong Kong International Film Festival', 'value': 'HongKong'},
            {'label': 'Grand Bell Awards, South Korea', 'value': 'GrandBell'},
            {'label': 'Tokyo International Film Festival', 'value': 'Tokyo'},
            {'label': 'Tokyo FILMeX', 'value': 'TokyoF'},
            {'label': 'Yamagata International Documentary Film Festival', 'value': 'Yamagata'},
            {'label': 'Singapore International Film Festival', 'value': 'Singapore'},
            {'label': 'Asia-Pacific Film Festival', 'value': 'AsiaPacific'},
            {'label': 'International Film Festival of India', 'value': 'India'},
            {'label': 'Fajr International Film Festival', 'value': 'Fajr'},
            {'label': 'Haifa International Film Festival', 'value': 'Haifa'},
            {'label': 'Jerusalem Film Festival', 'value': 'Jerusalem'},
            {'label': 'Kerala International Film Festival', 'value': 'Kerala'},
            {'label': 'Taipei Film Festival', 'value': 'Taipei'},
            {'label': 'Jeonju International Film Festival', 'value': 'Jeonju'}
        ]
        value = 'Beijing'
    if continent == 'Africa':
        options = [
            {'label': 'Marrakech International Film Festival', 'value': 'Marrakech'},
            {'label': 'Cairo International Film Festival', 'value': 'Cairo'}
        ]
        value = 'Marrakech'
    if continent == 'NorthAmerica':
        options = [
            {'label': 'Sundance Film Festival', 'value': 'Sundance'},
            {'label': 'Tribeca Film Festival', 'value': 'Tribeca'},
            {'label': 'Chicago International Film Festival', 'value': 'Chicago'},
            {'label': 'SXSW Film Festival', 'value': 'SXSW'},
            {'label': 'Seattle International Film Festival', 'value': 'Seattle'},
            {'label': 'San Francisco International Film Festival', 'value': 'SanFrancisco'},
            {'label': 'Slamdance Film Festival', 'value': 'Slamdance'},
            {'label': 'Toronto International Film Festival', 'value': 'Toronto'},
            {'label': 'Austin Film Festival', 'value': 'Austin'},
            {'label': 'Havana Film Festival', 'value': 'Havana'},
            {'label': 'African-American Film Critics Association (AAFCA)', 'value': 'AAFCA'}
        ]
        value = 'Sundance'
    if continent == 'SouthAmerica':
        options = [
            {'label': 'Buenos Aires International Festival of Independent Cinema', 'value': 'BuenosAires'},
            {'label': 'Gramado Film Festival', 'value': 'Gramado'},
            {'label': 'Rio de Janeiro International Film Festival', 'value': 'Rio'},
            {'label': 'São Paulo International Film Festival', 'value': 'SaoPaulo'}
        ]
        value = 'BuenosAires'
    if continent == 'Europe':
        options = [
            {'label': 'Berlin International Film Festival', 'value': 'Berlin'},
            {'label': 'Cannes Film Festival', 'value': 'Cannes'},
            {'label': 'Venice Film Festival', 'value': 'Venice'},
            {'label': 'Rotterdam International Film Festival', 'value': 'Rotterdam'},
            {'label': 'Locarno International Film Festival', 'value': 'Locarno'},
            {'label': 'Sitges - Catalonian International Film Festival', 'value': 'Sitges'},
            {'label': 'Karlovy Vary International Film Festival', 'value': 'KarlovyVary'},
            {'label': 'Torino Film Festival', 'value': 'Torino'},
            {'label': 'Moscow International Film Festival', 'value': 'Moscow'},
            {'label': 'Edinburgh International Film Festival', 'value': 'Edinburgh'},
            {'label': 'International Film Festival Mannheim-Heidelberg', 'value': 'MannheimHeidelberg'},
            {'label': 'San Sebastián International Film Festival', 'value': 'Sansebastián'},
            {'label': 'Taormina Film Festival', 'value': 'Taormina'},
            {'label': 'London Film Festival', 'value': 'London'},
            {'label': 'Thessaloniki International Film Festival', 'value': 'Thessaloniki'}
        ]
        value = 'Berlin'
    if continent == 'Australia':
        options = [
            {'label': 'Sydney Film Festival', 'value': 'Sydney'},
            {'label': 'Brisbane International Film Festival', 'value': 'Brisbane'}
        ]
        value = 'Sydney'
    return options, value


@app.callback(
    Output('genre', 'children'),
    [Input('festival', 'value')])
def set_genre(festival_name):
    tabs = all_options[festival_name].copy()
    original = all_options[festival_name]
    if festival_name == 'Berlin':
        for i in range(len(tabs)):
            if tabs[i] == 'Drama / Thriller':
                tabs[i] = 'DramaThriller'
            elif tabs[i] == 'Comedy / Drama':
                tabs[i] = 'ComedyDrama'
    return [dcc.Tab(label=original[i], value=original[i], id=tabs[i], className='custom-tab') for i in range(len(tabs))]


@app.callback(
    Output('note', 'children'),
    [Input('festival', 'value')])
def set_htmlp(festival_name):
    if festival_name in ['Rotterdam', 'Slamdance', 'SanFrancisco', 'HongKong', 'Austin', 'Torino', 'Marrakech',
                         'BuenosAires', 'Gramado', 'Cario', 'Havana', 'Rio', 'AsiaPacific', 'India', 'Sydney', 'Beijing',
                         'TokyoF', 'Brisbane','Jerusalem','Haifa','Fajr','Saingapore','Yamagata']:
        content = '*Due to the limited amount of data, the reliability of the statistical results should be carefully ' \
                  'considered '
    else:
        content = ''
    return content


@app.callback(
    [Output('boxplot', 'figure'),
     Output('barchart', 'figure')],
    [Input('festival', 'value'),
     Input('genre', 'value')])
def update_graph(festival_name, genre_name):
    if festival_name == 'Sundance':
        s, s_winner, s_loser = newDataset(sundance, genre_name)

    elif festival_name == 'Tribeca':
        s, s_winner, s_loser = newDataset(tribeca, genre_name)

    elif festival_name == 'Chicago':
        s, s_winner, s_loser = newDataset(chicago, genre_name)

    elif festival_name == 'Berlin':
        s, s_winner, s_loser = newDataset(berlin, genre_name)

    elif festival_name == 'Rotterdam':
        s, s_winner, s_loser = newDataset(rotterdam, genre_name)

    elif festival_name == 'Cannes':
        s, s_winner, s_loser = newDataset(cannes, genre_name)

    elif festival_name == 'Venice':
        s, s_winner, s_loser = newDataset(venice, genre_name)

    elif festival_name == 'SXSW':
        s, s_winner, s_loser = newDataset(sxsw, genre_name)

    elif festival_name == 'Seattle':
        s, s_winner, s_loser = newDataset(seattle, genre_name)

    elif festival_name == 'SanFrancisco':
        s, s_winner, s_loser = newDataset(san, genre_name)

    elif festival_name == 'Slamdance':
        s, s_winner, s_loser = newDataset(slam, genre_name)

    elif festival_name == 'Locarno':
        s, s_winner, s_loser = newDataset(locarno, genre_name)

    elif festival_name == 'Sitges':
        s, s_winner, s_loser = newDataset(sitges, genre_name)

    elif festival_name == 'Toronto':
        s, s_winner, s_loser = newDataset(toronto, genre_name)

    elif festival_name == 'KarlovyVary':
        s, s_winner, s_loser = newDataset(kv, genre_name)

    elif festival_name == 'HongKong':
        s, s_winner, s_loser = newDataset(hongkong, genre_name)

    elif festival_name == 'Austin':
        s, s_winner, s_loser = newDataset(austin, genre_name)

    elif festival_name == 'Torino':
        s, s_winner, s_loser = newDataset(torino, genre_name)

    elif festival_name == 'Marrakech':
        s, s_winner, s_loser = newDataset(marrakech, genre_name)

    elif festival_name == 'Tokyo':
        s, s_winner, s_loser = newDataset(tokyo, genre_name)

    elif festival_name == 'GoldenHorse':
        s, s_winner, s_loser = newDataset(goldenhorse, genre_name)

    elif festival_name == 'BuenosAires':
        s, s_winner, s_loser = newDataset(buenosaires, genre_name)

    elif festival_name == 'Gramado':
        s, s_winner, s_loser = newDataset(gramado, genre_name)

    elif festival_name == 'Cairo':
        s, s_winner, s_loser = newDataset(cairo, genre_name)

    elif festival_name == 'Havana':
        s, s_winner, s_loser = newDataset(havana, genre_name)

    elif festival_name == 'Rio':
        s, s_winner, s_loser = newDataset(rio, genre_name)

    elif festival_name == 'SaoPaulo':
        s, s_winner, s_loser = newDataset(saopaulo, genre_name)

    elif festival_name == 'AsiaPacific':
        s, s_winner, s_loser = newDataset(asiapacific, genre_name)

    elif festival_name == 'India':
        s, s_winner, s_loser = newDataset(india, genre_name)

    elif festival_name == 'Sydney':
        s, s_winner, s_loser = newDataset(sydney, genre_name)

    elif festival_name == 'Beijing':
        s, s_winner, s_loser = newDataset(beijing, genre_name)

    elif festival_name == 'TokyoF':
        s, s_winner, s_loser = newDataset(tokyof, genre_name)

    elif festival_name == 'AAFCA':
        s, s_winner, s_loser = newDataset(aafca, genre_name)

        s, s_winner, s_loser = newDataset(brisbane, genre_name)

    elif festival_name == 'Jerusalem':
        s, s_winner, s_loser = newDataset(jerusalem, genre_name)

    elif festival_name == 'Haifa':
        s, s_winner, s_loser = newDataset(haifa, genre_name)

    elif festival_name == 'GrandBell':
        s, s_winner, s_loser = newDataset(grandbell, genre_name)

    elif festival_name == 'Fajr':
        s, s_winner, s_loser = newDataset(fajr, genre_name)

    elif festival_name == 'Singapore':
        s, s_winner, s_loser = newDataset(singapore, genre_name)

    elif festival_name == 'Yamagata':
        s, s_winner, s_loser = newDataset(yamagata, genre_name)

    elif festival_name == 'Shanghai':
        s, s_winner, s_loser = newDataset(shanghai, genre_name)

    elif festival_name == 'Kerala':
        s, s_winner, s_loser = newDataset(kerala, genre_name)

    elif festival_name == 'Taipei':
        s, s_winner, s_loser = newDataset(taipei, genre_name)

    elif festival_name == 'Jeonju':
        s, s_winner, s_loser = newDataset(jeonju, genre_name)

    elif festival_name == 'Moscow':
        s, s_winner, s_loser = newDataset(moscow, genre_name)

    elif festival_name == 'Edinburgh':
        s, s_winner, s_loser = newDataset(edinburgh, genre_name)

    elif festival_name == 'Mannheim-Heidelberg':
        s, s_winner, s_loser = newDataset(mannheimheidelberg, genre_name)

    elif festival_name == 'San Sebastián':
        s, s_winner, s_loser = newDataset(sansebastián , genre_name)

    elif festival_name == 'Taormina':
        s, s_winner, s_loser = newDataset(taormina, genre_name)

    elif festival_name == 'London':
        s, s_winner, s_loser = newDataset(london, genre_name)

    elif festival_name == 'Thessaloniki':
        s, s_winner, s_loser = newDataset(thessaloniki, genre_name)

    allfilm = newbo[newbo['Genre_' + festival_name] == genre_name]

    allfilm_outlier, allfilm_new = outliers(allfilm, feature)
    s_outlier, s_new = outliers(s, feature)
    s_winner_new = drop_contenders_new(s_winner, s_new, False)
    s_loser_new = drop_contenders_new(s_loser, s_new, False)

    allmean = cal_mean(allfilm_new, feature)
    smean = cal_mean(s_new, feature)
    slmean = cal_mean(s_loser_new, feature)
    swmean = cal_mean(s_winner_new, feature)

    title1 = festival_name + ' ' + genre_name + ' Box Office Boxplot'
    title2 = genre_name + ' Films Average Box Office'

    figure = go.Figure(data=[go.Box(y=s_winner_new[feature], name='Winners', marker_color='#C4DFE6'),
                             go.Box(y=s_loser_new[feature], name='Nominees', marker_color='#66A5AD'),
                             go.Box(y=s_new[feature], name='Contenders', marker_color='#07575B'),
                             go.Box(y=allfilm_new[feature], name='Non-Contenders', marker_color='#003B46')],
                       layout=go.Layout(title={'text': title1, 'x': 0.5}))
    figure2 = go.Figure(data=[go.Bar(x=[allmean, smean, slmean, swmean],
                                     y=['others', 'contenders', 'nominee', 'winner'],
                                     text=combine[festival_name]['boxoffice'][genre_name],
                                     textposition='auto',
                                     marker_color=['#003B46', '#07575B', '#66A5AD', '#C4DFE6'],
                                     orientation='h')],
                        layout=go.Layout(title={'text': title2, 'x': 0.5}))

    figure.update_layout(
        paper_bgcolor='#1e2130',
        plot_bgcolor='#1e2130',
        legend={'font': {'color': 'darkgray'}},
        font={'color': 'darkgray'},
        showlegend=True
    )
    figure2.update_layout(
        paper_bgcolor='#1e2130',
        plot_bgcolor='#1e2130',
        legend={'font': {'color': 'darkgray'}},
        font={'color': 'darkgray'},
        showlegend=False
    )

    return figure, figure2


@app.callback(
    [Output('table', 'data'),
     Output('table', 'style_data_conditional'),
     Output('table', 'style_cell_conditional')],
    [Input('festival', 'value')])
def update_table(festival_name):
    data = combine[festival_name]
    boxoffice, percent, pvalue, pos_sigs, neg_sigs = data['boxoffice'], data['percent'], data['pvalue'], \
                                                     data['pos_sigs'], data['neg_sigs']

    data = [
        {
            'genre': i,
            'others': boxoffice[i][0],
            'contendersbo': boxoffice[i][1],
            'contendersdiff': percent[i][0],
            'losersbo': boxoffice[i][2],
            'losersdiff': percent[i][1],
            'winnersbo': boxoffice[i][3],
            'winnersdiff': percent[i][2],
        }
        for i in all_options[festival_name]
    ]

    style_cell_conditional = [
        {
            "if": {"row_index": sig[0],
                   "column_id": sig[1]},
            "backgroundColor": "#66A5AD",
            'color': 'white'
        }
        for sig in pos_sigs if len(pos_sigs) > 0
    ]

    style_data_conditional = [
        {
            "if": {"row_index": sig[0],
                   "column_id": sig[1]},
            "backgroundColor": "#880000",
            'color': 'white'
        }
        for sig in neg_sigs if len(neg_sigs) > 0
    ]

    return data, style_data_conditional, style_cell_conditional


# In[35]:


if __name__ == '__main__':
    app.run_server()

# In[ ]:
