import os
from newsapi import NewsApiClient
from newspaper import Article
from typing import List, Dict
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class NewsFetcher:
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        if not self.api_key:
            raise ValueError("NEWS_API_KEY not found in environment variables")
        self.newsapi = NewsApiClient(api_key=self.api_key)

    def fetch_news(self, company_name: str, num_articles: int = 10) -> List[Dict]:
        """
        Fetch news articles for a given company name or ticker
        """
        try:
            # Search for news articles
            news = self.newsapi.get_everything(
                q=company_name,
                language='en',
                sort_by='publishedAt',
                page_size=num_articles
            )

            articles = []
            for article in news['articles']:
                try:
                    # Download and parse article content
                    news_article = Article(article['url'])
                    news_article.download()
                    news_article.parse()
                    
                    articles.append({
                        'title': article['title'],
                        'url': article['url'],
                        'publishedAt': article['publishedAt'],
                        'content': news_article.text,
                        'source': article['source']['name']
                    })
                except Exception as e:
                    print(f"Error processing article: {str(e)}")
                    continue

            return articles
        except Exception as e:
            print(f"Error fetching news: {str(e)}")
            return []

    def get_articles_dataframe(self, articles: List[Dict]) -> pd.DataFrame:
        """
        Convert articles list to pandas DataFrame
        """
        return pd.DataFrame(articles) 