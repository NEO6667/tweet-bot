from src.fetcher import fetch_latest_news
from src.generator import generate_soft_tweet
from src.image_handler import download_article_image
from src.twitter_client import get_twitter_clients, post_tweet
from src.deduplicator import is_duplicate, save_posted_hash

def main():
    print("Fetching latest news...")
    articles = fetch_latest_news()

    # Pick the first non-duplicate article
    selected = None
    for article in articles:
        if not is_duplicate(article["link"]):
            selected = article
            break

    if not selected:
        print("No new articles found. Skipping.")
        return

    print(f"Selected: {selected['title']}")

    # Generate soft tweet
    tweet_text = generate_soft_tweet(selected)
    # Append the link
    full_tweet = f"{tweet_text}\n\n{selected['link']}"

    # Download image
    image_path = download_article_image(selected.get("image_url"))

    # Post
    api_v1, client_v2 = get_twitter_clients()
    result = post_tweet(api_v1, client_v2, full_tweet, image_path)

    print(f"Posted: {result}")

    # Record as posted
    save_posted_hash(selected["link"])

    # Cleanup
    if image_path and os.path.exists(image_path):
        os.remove(image_path)

if __name__ == "__main__":
    main()