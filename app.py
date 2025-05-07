import streamlit as st
import pandas as pd
from news_utils import NewsFetcher
from sentiment_utils import SentimentAnalyzer
from visualizations import (
    create_sentiment_pie_chart,
    create_sentiment_bar_chart,
    create_sentiment_summary
)

# Set page config
st.set_page_config(
    page_title="Market Pulse AI",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = SentimentAnalyzer()
if 'news_fetcher' not in st.session_state:
    st.session_state.news_fetcher = NewsFetcher()

# Sidebar
st.sidebar.title("Market Pulse AI Settings")
company_name = st.sidebar.text_input("Enter Company Name or Ticker", "Tesla")
num_articles = st.sidebar.slider("Number of Articles", 5, 20, 10)

# Main content
st.title("📊 Market Pulse AI")
st.subheader("Real-time Market Sentiment Analysis")

if st.sidebar.button("Analyze Market Sentiment"):
    with st.spinner("Fetching and analyzing news articles..."):
        # Fetch news articles
        articles = st.session_state.news_fetcher.fetch_news(company_name, num_articles)
        
        if not articles:
            st.error("No articles found. Please try a different company name or ticker.")
        else:
            # Convert to DataFrame
            articles_df = st.session_state.news_fetcher.get_articles_dataframe(articles)
            
            # Analyze sentiment
            articles_df = st.session_state.analyzer.analyze_articles(articles_df)
            
            # Get market recommendation
            recommendation = st.session_state.analyzer.get_market_recommendation(articles_df)
            
            # Display recommendation
            st.markdown(f"### Market Recommendation: {recommendation}")
            
            # Create two columns for charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Display pie chart
                pie_chart = create_sentiment_pie_chart(articles_df)
                st.plotly_chart(pie_chart, use_container_width=True)
            
            with col2:
                # Display bar chart
                bar_chart = create_sentiment_bar_chart(articles_df)
                st.plotly_chart(bar_chart, use_container_width=True)
            
            # Display sentiment summary
            summary = create_sentiment_summary(articles_df)
            st.markdown("### Sentiment Analysis Summary")
            st.markdown(f"""
            - Total Articles Analyzed: {summary['total_articles']}
            - Positive Articles: {summary['positive_count']}
            - Neutral Articles: {summary['neutral_count']}
            - Negative Articles: {summary['negative_count']}
            - Average Confidence: {summary['average_confidence']:.2f}
            """)
            
            # Display articles with sentiment
            st.markdown("### Article Analysis")
            for _, row in articles_df.iterrows():
                sentiment_color = {
                    'POSITIVE': 'green',
                    'NEUTRAL': 'blue',
                    'NEGATIVE': 'red'
                }[row['sentiment']]
                
                st.markdown(f"""
                #### [{row['title']}]({row['url']})
                - Source: {row['source']}
                - Published: {row['publishedAt']}
                - Sentiment: <span style='color:{sentiment_color}'>{row['sentiment']}</span>
                - Confidence: {row['confidence']:.2f}
                """, unsafe_allow_html=True)
                st.markdown("---")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, NewsAPI, and Hugging Face") 