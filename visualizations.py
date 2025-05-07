import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict

def create_sentiment_pie_chart(articles_df: pd.DataFrame) -> go.Figure:
    """
    Create a pie chart showing the distribution of sentiments
    """
    sentiment_counts = articles_df['sentiment'].value_counts()
    
    fig = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        title='Sentiment Distribution',
        color=sentiment_counts.index,
        color_discrete_map={
            'POSITIVE': '#00CC96',
            'NEUTRAL': '#636EFA',
            'NEGATIVE': '#EF553B'
        }
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_sentiment_bar_chart(articles_df: pd.DataFrame) -> go.Figure:
    """
    Create a bar chart showing sentiment confidence scores
    """
    fig = px.bar(
        articles_df,
        x='title',
        y='confidence',
        color='sentiment',
        title='Article Sentiment Confidence',
        color_discrete_map={
            'POSITIVE': '#00CC96',
            'NEUTRAL': '#636EFA',
            'NEGATIVE': '#EF553B'
        }
    )
    
    fig.update_layout(
        xaxis_title='Articles',
        yaxis_title='Confidence Score',
        xaxis_tickangle=-45,
        showlegend=True
    )
    
    return fig

def create_sentiment_summary(articles_df: pd.DataFrame) -> Dict:
    """
    Create a summary of sentiment analysis results
    """
    total_articles = len(articles_df)
    sentiment_counts = articles_df['sentiment'].value_counts()
    
    return {
        'total_articles': total_articles,
        'positive_count': sentiment_counts.get('POSITIVE', 0),
        'neutral_count': sentiment_counts.get('NEUTRAL', 0),
        'negative_count': sentiment_counts.get('NEGATIVE', 0),
        'average_confidence': articles_df['confidence'].mean()
    } 