import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SOFT_TWEET_PROMPT = """You are a thoughtful tech writer. Write a short, soft, conversational tweet about this article.

Rules:
- Under 250 characters total
- No hype words (revolutionary, game-changing, groundbreaking)
- No exclamation marks
- No ALL CAPS
- Sound human and curious, not robotic
- End with a short observation or open question
- Include 1-2 relevant hashtags
- Do NOT include the article link (it will be added separately)

Article title: {title}
Article description: {description}

Write only the tweet text, nothing else."""

def generate_soft_tweet(article):
    prompt = SOFT_TWEET_PROMPT.format(
        title=article["title"],
        description=article["description"] or article["title"],
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    tweet_text = response.text.strip()

    # Hard enforce length limit
    if len(tweet_text) > 260:
        tweet_text = tweet_text[:257] + "..."

    return tweet_text