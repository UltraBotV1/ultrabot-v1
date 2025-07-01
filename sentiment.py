import requests
import os

def is_sentiment_safe(token_symbol):
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    if not bearer_token:
        print("❌ Twitter Bearer Token not set in secrets.")
        return False

    headers = {
        "Authorization": f"Bearer {bearer_token}",
    }

    query = f"{token_symbol} -is:retweet lang:en"
    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=10"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"⚠️ Twitter API error for {token_symbol}: {response.status_code}")
            return False

        tweets = response.json().get("data", [])
        if not tweets:
            print(f"📉 No tweets found for {token_symbol}. Skipping...")
            return False

        negative_keywords = ["crash", "rug", "exit", "hack", "sell-off", "lawsuit", "liquidation", "bearish", "scam", "panic"]
        for tweet in tweets:
            text = tweet["text"].lower()
            if any(word in text for word in negative_keywords):
                print(f"🚨 Negative sentiment detected for {token_symbol}")
                return False

        return True

    except Exception as e:
        print(f"🔧 Error checking sentiment for {token_symbol}: {e}")
        return False