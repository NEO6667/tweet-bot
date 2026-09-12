import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# DeepSeek uses the OpenAI-compatible endpoint
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# Model name: use "deepseek-flash" for the latest Flash model
# (the old name "deepseek-v4-flash" still works but is deprecated)
MODEL_NAME = os.getenv("DEEPSEEK_MODEL", "deepseek-flash")

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
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    tweet_text = response.choices[0].message.content.strip()

    # Hard enforce length limit
    if len(tweet_text) > 260:
        tweet_text = tweet_text[:257] + "..."

    return tweet_text