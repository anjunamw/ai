# backend/app/services/social_media.py
from typing import Dict, List

import tweepy
from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.llm import generate_text
from backend.app.db.database import get_db
from backend.app.db.models import SocialMediaPost


async def fetch_posts(user: str, db: Session = Depends(get_db)) -> List[Dict[str, str]]:
    posts = db.query(SocialMediaPost).filter(SocialMediaPost.user_id == 1).all()
    return [
        {"id": str(post.id), "text": post.text, "created_at": str(post.created_at)}
        for post in posts
    ]


async def draft_post(user: str) -> str | None:
    prompt = f"Draft a social media post"
    return generate_text(prompt)


async def publish_post(post: str, user: str) -> str:
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    if (
        not bearer_token
        or not consumer_key
        or not consumer_secret
        or not access_token
        or not access_token_secret
    ):
        return "Twitter credentials not configured"
    try:
        client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )
        response = client.create_tweet(text=post)
        return f"Tweet created successfully: {response.data.get('id')}"
    except Exception as e:
        print(f"An error occurred while creating tweet: {e}")
        return "An error occurred while creating tweet"
