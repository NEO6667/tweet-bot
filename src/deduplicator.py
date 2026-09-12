import hashlib
import json
import os

HISTORY_FILE = "data/posted_articles.json"

def load_posted_hashes():
    if not os.path.exists(HISTORY_FILE):
        return set()
    with open(HISTORY_FILE, "r") as f:
        return set(json.load(f))

def save_posted_hash(article_link):
    hashes = load_posted_hashes()
    article_hash = hashlib.sha256(article_link.encode()).hexdigest()
    hashes.add(article_hash)

    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(list(hashes), f)

def is_duplicate(article_link):
    article_hash = hashlib.sha256(article_link.encode()).hexdigest()
    return article_hash in load_posted_hashes()