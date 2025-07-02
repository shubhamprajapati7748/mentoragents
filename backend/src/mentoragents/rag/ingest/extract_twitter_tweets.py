from langchain_core.documents import Document
from loguru import logger
from mentoragents.models.mentor_extract import MentorExtract
from arcadepy import Arcade
import os
from mentoragents.core.config import settings

def extract_twitter_tweets(mentor_extract : MentorExtract, max_tweets : int = 100) -> list[Document]:
    """Extract tweets from Twitter for a given mentor.

    Args:
        mentor_extract : MentorExtract object containing mentor details.

    Returns:
        list[Document] : List of documents extracted from Twitter.
    """
    logger.info(f"Extracting tweets from Twitter for {mentor_extract.name}")

    ARCADE_API_KEY = settings.ARCADE_API_KEY
    USER_ID = settings.ARCADE_USER_ID
    client = Arcade(api_key=ARCADE_API_KEY)
    TOOL_NAME = "X.SearchRecentTweetsByUsername"

    all_tweets = get_all_tweets(client, mentor_extract.twitter_handle, USER_ID, TOOL_NAME, max_tweets)

    tweets = []
    for tweet in all_tweets:
        tweets.append(Document(
            page_content = tweet["text"],
            metadata = {
                "mentor_id" : mentor_extract.id,
                "mentor_name" : mentor_extract.name,
                "source" : "twitter",
                "source_url" : tweet["tweet_url"],
            }
        ))

    logger.info(f"Extracted {len(tweets)} tweets from Twitter for {mentor_extract.name}")
    return tweets

def get_all_tweets(client, username: str, user_id: str, tool_name: str = "X.SearchRecentTweetsByUsername", max_tweets: int = 100) -> list:
    """
    Fetch all available tweets for a given username using pagination.
    
    Args:
        client: Arcade client instance
        username: Twitter username to fetch tweets for
        user_id: Arcade user ID
        tool_name: Name of the Arcade tool to use
        
    Returns:
        list: All collected tweets
    """
    all_tweets = []
    next_token = None
    
    while True:
        # Prepare inputs (include next_token if we have one)
        inputs = {"username": username, "max_results": 100}
        if next_token:
            inputs["next_token"] = next_token
            
        # Execute the request
        response = client.tools.execute(
            tool_name=tool_name,
            input= {
                "owner": "ArcadeAI",
                "name": "arcade-ai",
                "starred": "true",
                "username": username,
                "max_results": max_tweets
            },
            user_id=user_id,
        )
        
        # Get tweets from the response
        new_tweets = response.output.value['data']
        all_tweets.extend(new_tweets)
        
        # Get next token if available
        next_token = response.output.value["meta"].get("next_token", None)
        
        # If no next token, we've reached the end
        if not next_token:
            break
            
    return all_tweets