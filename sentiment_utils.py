from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd
from typing import List, Dict, Tuple

class SentimentAnalyzer:
    def __init__(self):
        self.model_name = "cardiffnlp/twitter-roberta-base-sentiment"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Analyze sentiment of a given text
        Returns: (sentiment_label, confidence_score)
        """
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            scores = torch.softmax(outputs.logits, dim=1)
            
        sentiment_map = {0: "NEGATIVE", 1: "NEUTRAL", 2: "POSITIVE"}
        sentiment_idx = scores.argmax().item()
        confidence = scores[0][sentiment_idx].item()
        
        return sentiment_map[sentiment_idx], confidence

    def analyze_articles(self, articles_df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze sentiment for all articles in the DataFrame
        """
        sentiments = []
        confidences = []
        
        for _, row in articles_df.iterrows():
            # Combine title and content for better context
            text = f"{row['title']} {row['content'][:500]}"  # Limit content length
            sentiment, confidence = self.analyze_sentiment(text)
            sentiments.append(sentiment)
            confidences.append(confidence)
        
        articles_df['sentiment'] = sentiments
        articles_df['confidence'] = confidences
        return articles_df

    def get_market_recommendation(self, articles_df: pd.DataFrame) -> str:
        """
        Generate market recommendation based on sentiment analysis
        """
        sentiment_scores = {
            'POSITIVE': 1,
            'NEUTRAL': 0,
            'NEGATIVE': -1
        }
        
        # Calculate weighted sentiment score
        total_score = 0
        for _, row in articles_df.iterrows():
            score = sentiment_scores[row['sentiment']] * row['confidence']
            total_score += score
        
        # Generate recommendation
        if total_score > 2:
            return "📈 Market mood is optimistic"
        elif total_score < -2:
            return "📉 Sentiment is negative"
        else:
            return "😐 Mixed signals, stay cautious" 