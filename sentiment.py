import requests
from textblob import TextBlob
from config import NEWS_API_KEY

def get_news_sentiment():
    url = "https://newsapi.org/v2/everything"
    params = {"q": "Ibovespa", "language": "pt", "apiKey": NEWS_API_KEY}

    response = requests.get(url, params=params)
    articles = response.json().get("articles", [])

    sentiment_scores = []
    for article in articles[:5]:  # Check top 5 news
        text = f"{article['title']} {article['description']}"
        sentiment = TextBlob(text).sentiment.polarity  # -1 to 1
        sentiment_scores.append(sentiment)

    return sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

if __name__ == "__main__":
    print(f"News Sentiment Score: {get_news_sentiment():.2f}")
