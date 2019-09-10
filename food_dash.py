import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import dateparser

number_rows = 10

df = pd.read_excel("inspection-aliments-contrevenants.xlsx")
list_addr = df["/contrevenant/adresse"]

df2 = df.drop('/contrevenant/description', axis=1) #no description


def newColumns(dataTable, colList):
    newCols = {}
    for col in colList:
        newCols.update({col: col.replace('/contrevenant/', '')})
    dataTable.rename(columns=newCols, inplace=True)


newColumns(df, list(df.columns))
newColumns(df2, list(df2.columns))


def correctLoc(df_cost):
    i = 0
    for value in df_cost['ville']:
        df_cost['ville'][i] = value[:-8]
        i += 1
    return df_cost



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Inspection des aliments – contrevenants',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'paddingTop': '25px'
        }
    ),

    html.Div(
        children=u'''Liste des établissements alimentaires situés sur le territoire de 
        l’agglomération montréalaise et sous la responsabilité de la Division de l’inspection des aliments de 
        la Ville de Montréal ayant fait l’objet d’une condamnation pour une infraction à la Loi 
        sur les produits alimentaires (L.R.Q., c. P-29) et ses règlements.''',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'fontSize': '15px',
        }),

    dcc.Graph(id='money-location-scatter',
              figure={
                  'data': [
                      go.Scatter(
                          y=df['date_infraction'],
                          x=df['montant'],
                          text=df['etablissement'],
                          mode='markers',
                          opacity=0.7,
                          marker={

                              'size': 12,
                              'line': {'width': 0.5, 'color': 'white'}
                            },

                      )
                  ],
                  'layout': go.Layout(
                      title='Coût de Contravention Selon les Années',
                      yaxis={'title': 'Année'},
                      xaxis={'title': 'Montant de la Contravention ($)'},
                      hovermode='closest',
                      #legend={'x': 0, 'y': 1}

                  )

              },
              style={
                  'paddingLeft': '25px'
              }
              ),

    html.Div(children='Liste Des Restaurants',
             style={
                 'color': colors['text'],
                 'fontSize': '35px',
                 'marginLeft': '100px'
             }),

    html.Table(children=
               [html.Tr([html.Th(col) for col in df.columns])] +

               [html.Tr([
                   html.Td(df.iloc[i][col]) for col in df.columns
               ]) for i in range(min(len(df), number_rows))],

               style={
                   'color': colors['text'],
                   'fontSize': '12px',
                   'marginLeft': 'auto',
                   'marginRight': 'auto'
               })
])


if __name__ == '__main__':
    app.run_server(debug=True)
