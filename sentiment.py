import requests
from textblob import TextBlob
from typing import List, Optional
from config import NEWS_API_KEY

def get_news_sentiment() -> float:
    """
    Fetch and analyze sentiment from news articles about Ibovespa.
    
    Returns:
        float: Average sentiment score between -1 and 1
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "Ibovespa",
        "language": "pt",
        "apiKey": NEWS_API_KEY,
        "pageSize": 5  # Limit to 5 articles directly in API call
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        
        articles = response.json().get("articles", [])
        if not articles:
            print("Warning: No articles found")
            return 0.0

        sentiment_scores: List[float] = []
        for article in articles:
            text = f"{article.get('title', '')} {article.get('description', '')}"
            if text.strip():  # Only analyze non-empty text
                sentiment = TextBlob(text).sentiment.polarity
                sentiment_scores.append(sentiment)

        return sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0

    except requests.RequestException as e:
        print(f"Error fetching news: {str(e)}")
        return 0.0
    except Exception as e:
        print(f"Error processing sentiment: {str(e)}")
        return 0.0

if __name__ == "__main__":
    print(f"News Sentiment Score: {get_news_sentiment():.2f}")
