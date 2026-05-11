from textblob import TextBlob


def analyze_sentiment(news_articles):

    positive = 0
    negative = 0
    neutral = 0

    for article in news_articles:

        title = article.get("title", "")

        polarity = TextBlob(title).sentiment.polarity

        if polarity > 0:
            positive += 1
        elif polarity < 0:
            negative += 1
        else:
            neutral += 1

    total = positive + negative + neutral


    if total == 0:
        total = 1

    return {
        "positive": f"{round((positive/total)*100)}%",
        "negative": f"{round((negative/total)*100)}%",
        "neutral": f"{round((neutral/total)*100)}%"
    }