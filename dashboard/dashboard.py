#Deployed at : https://messlytixdashboard.herokuapp.com/

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 
import numpy as np 


app = dash.Dash()

df=pd.read_csv('FOODYLYTICSDATASET1.csv')
dff=pd.read_csv('foodylytics2.csv')

external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]


app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)

colors = {
    'background': '#000000',
    'text': '#b02346'
}

#<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital@1&display=swap" rel="stylesheet">

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
                html.H1(children='DASHBOARD',
                        style={'textAlign': 'center',
                                 'color': colors['text'],
                                 'font-family':'Montserrat,sans-serif',
                                 'font-style':'italic',
                                 'font-weight':'bold',
                                 'fontSize':30
                              },
                        ),

                html.Img(src='/assets/picss.png', style={'height':'10%', 'width':'10%'}),

                html.Br(),

                html.Br(),


                dash_table.DataTable(
                    id='datatable_id',
                    data=df.to_dict('records'),
                    columns=[
                        {"name": i, "id": i, "deletable": False, "selectable": False} for i in df.columns
                    ],
                    editable=False,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    #row_selectable="multi",
                    row_deletable=False,
                    selected_rows=[],
                    #page_action="native",
                    #page_current= 0,
                    #page_size= 6,
                    page_action='none',
                    style_cell={
                      'fontSize':20,
                      'font-family':'Montserrat,sans-serif',
                      'backgroundColor': '#111111',
                      'color': '#b02346'
                      
                    },
                    fixed_rows={ 'headers': True, 'data': 0 },
                    virtualization=False,
                    style_cell_conditional=[
                        {'if': {'column_id': 'Day'},
                         'width': '20%', 'textAlign': 'center'},
                        {'if': {'column_id': 'Menu Rating'},
                         'width': '10%', 'textAlign': 'left'},
                        {'if': {'column_id': 'Amount Of Food Cooked'},
                         'width': '20%', 'textAlign': 'left'},
                        {'if': {'column_id': 'Wastage'},
                         'width': '20%', 'textAlign': 'left'},
                        {'if': {'column_id': 'Week'},
                         'width': '10%', 'textAlign': 'left'},
                        {'if': {'column_id': 'Date'},
                         'width': '20%', 'textAlign': 'left'},
                  
                  
                    ],

                    style_table={
                        'width':'100%'
                    }
                    
                ),


                dcc.Graph(
                    id='example-graph',
                    figure={
                        'data': [
                                  {'x':df['Day'], 'y':df['Wastage'], 'type': 'bar'},
                                ],
                        'layout': {
                            'title': 'DAY Vs Wastage',
                            'xaxis' : dict(
                                title='Days',
                                titlefont=dict(
                                family='Montserrat,sans-serif',
                                size=20,
                                
                            )),
                            'yaxis' : dict(
                                title='Wastage',
                                titlefont=dict(
                                family= 'Montserrat,sans-serif',
                                size=20,
                                
                            )),

                            'plot_bgcolor': colors['background'],
                            'paper_bgcolor':colors['background'],
                            'font': {
                                  'color': colors['text']
                                    }       
                        }
                    }
                ),
                
                dcc.Graph(
                    id='example-graph-2',
                    figure={
                        'data': [
                                  {'x':dff['WEEK'], 'y':dff['Wastage'], 'type': 'line','name':'Wastage'},
                                  {'x':dff['WEEK'], 'y':dff['Wastage if followed Model'], 'type': 'line','name':'wastage if Messlytix is used'},
                                
                                ],
                        
                        'layout': {
                            'title': 'How Foodylytics will affect food loss',

                            'xaxis' : dict(
                                title='WEEK NO',
                                titlefont=dict(
                                family='Montserrat,sans-serif',
                                size=20,
                                
                            )),

                            'yaxis' : dict(
                                title='Food Wastage',
                                titlefont=dict(
                                family= 'Montserrat,sans-serif',
                                size=20,
                                
                            )),

                            'plot_bgcolor': colors['background'],
                            'paper_bgcolor':colors['background'],
                            'font': {
                                  'color': colors['text']
                                    }  
                        }
                    }
                )

            ]
        
        )       

                
            
            

if __name__ == '__main__':
    app.run_server(debug=True)
