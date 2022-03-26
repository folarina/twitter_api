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
        html.H4('Interactive Sentiment Analysis with Fabrizio Romanao Tweets'),
        dcc.Graph(id="scatter-plot"),
        html.P("Filter by Tweet Length:"),
        dcc.RangeSlider(
            id='range-slider',
            min=tweets_df['Text Length'].min(), max=tweets_df['Text Length'].max(), step=None,
            marks = {30: '30', 50: '50'},
            value=[30, 50]
        ),
    ])


    @app.callback(
        Output("scatter-plot", "figure"), 
        Input("range-slider", "value"))
    def update_bar_chart(slider_range):
        low, high = slider_range
        mask = (tweets_df['Text Length'] > low) & (tweets_df['Text Length'] < high)
        fig = px.scatter(tweets_df[mask], x='TimeStamp', y='Polarity', color='Analysis', size='Text Length')
        
        fig.update_layout(xaxis={'categoryorder':'total ascending'},
                            title={'xanchor':'center', 'yanchor': 'top', 'y':0.9,'x':0.5,})
        
        
        return fig
    return app


if __name__ == '__main__': #learn

    tweets_df = get_tweets()
    app = create_plotly(tweets_df)

    app.run_server(debug=False)

