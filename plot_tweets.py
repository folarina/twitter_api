import plotly.express as px
import datetime as dt
from dash import Dash, dcc, html, Input, Output
import pandas as pd


def get_tweets():
    df = pd.read_csv('processed_df.csv')
    return df #return df as thats the item that i need 

def create_plotly(tweets_df):
    app = Dash(__name__)


    app.layout = html.Div([
        html.Div([
        html.H3(['Interactive Sentiment Analysis of Football Tweets']),
        dcc.Dropdown(
            id='my_dropdown',
            options= [{'label':str(b),'value':b} for b in sorted(tweets_df['Team'].unique())],
           ## ['Generic','Arsenal','Chelsea','Manchester United'],
            value='Teams',
            multi=True,
            clearable=False,
            style={"width": "80%"}
        ),
    ]),

    ])
    
    @app.callback(
    Output("the_graph", "figure"), 
    [Input("my_dropdown", "value")])

    def update_graph(my_dropdown):
        mask = tweets_df['Team'].isin(my_dropdown)
        scatter = px.scatter(tweets_df[mask], x='Day-Time', y='Polarity', color='User', size='Text Length', hover_data=["User"])
        
        
        return (scatter)    
    return app


if __name__ == '__main__': #learn

    tweets_df = get_tweets()
    app = create_plotly(tweets_df)

    app.run_server(debug=False)
