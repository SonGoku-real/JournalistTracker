import os
import json
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

# The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# Do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

def analyze_article_sentiment(text):
    """
    Analyze the sentiment of an article using OpenAI's API.
    Returns sentiment score (-1.0 to 1.0) and label (positive, negative, neutral).
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a sentiment analysis expert specializing in cryptocurrency journalism. "
                    + "Analyze the sentiment of this crypto news article and return a JSON object with: "
                    + "1. sentiment_score: a float between -1.0 (very negative) and 1.0 (very positive) where 0 is neutral "
                    + "2. sentiment_label: one of 'positive', 'negative', or 'neutral' "
                    + "3. tone: the overall tone (analytical, confident, concerned, etc.) "
                    + "4. key_topics: a list of 2-4 crypto-specific topics mentioned"
                },
                {"role": "user", "content": text[:4000]}  # Limit to first 4000 chars for API limits
            ],
            response_format={"type": "json_object"},
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        logger.error(f"Error analyzing article with OpenAI: {e}")
        # Return default values if API fails
        return {
            "sentiment_score": 0.0,
            "sentiment_label": "neutral",
            "tone": "unknown",
            "key_topics": []
        }

def extract_article_topics(text):
    """
    Extract the main topics from an article using OpenAI's API.
    Returns a list of topic names relevant to crypto journalism.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a cryptocurrency news analyst specializing in topic extraction. "
                    + "Extract the main crypto-related topics from this article and return only a JSON array "
                    + "with 2-5 topic names. Focus on specific cryptocurrency topics like 'Bitcoin', 'DeFi', "
                    + "'Regulation', 'NFTs', 'Mining', etc. Be specific and accurate to crypto terminology."
                },
                {"role": "user", "content": text[:4000]}  # Limit to first 4000 chars for API limits
            ],
            response_format={"type": "json_object"},
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get("topics", [])
    except Exception as e:
        logger.error(f"Error extracting topics with OpenAI: {e}")
        return []

def summarize_article(text):
    """
    Generate a concise summary of an article using OpenAI's API.
    Returns a string with the summary.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a cryptocurrency news summarizer. "
                    + "Create a concise 2-3 sentence summary of this crypto news article. "
                    + "Focus on the key facts and implications for the crypto industry."
                },
                {"role": "user", "content": text[:4000]}  # Limit to first 4000 chars for API limits
            ]
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error summarizing article with OpenAI: {e}")
        return "Summary not available."