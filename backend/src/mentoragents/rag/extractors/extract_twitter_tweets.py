from langchain_core.documents import Document
from mentoragents.models.mentor_extract import MentorExtract
from mentoragents.core.config import settings
from arcadepy import Arcade
from loguru import logger

def extract_twitter_tweets(mentor_extract : MentorExtract, max_tweets : int = 100) -> list[Document]:
    """Extract tweets from Twitter for a given mentor.

    Args:
        mentor_extract : MentorExtract object containing mentor details.

    Returns:
        list[Document] : List of documents extracted from Twitter.
    """
    logger.info(f"Extracting tweets from Twitter for {mentor_extract.id}")
    ARCADE_API_KEY = settings.ARCADE_API_KEY
    USER_ID = settings.ARCADE_USER_ID
    TOOL_NAME = "X.SearchRecentTweetsByUsername"

    try:  
        client = Arcade(api_key=ARCADE_API_KEY)
        all_tweets = get_all_tweets(client, mentor_extract.twitter_handle, USER_ID, TOOL_NAME, max_tweets)
        documents : list[Document] = list[Document]()
        for tweet in all_tweets:
            document = Document(
                page_content = tweet["text"],
                metadata = {
                    "mentor_id" : mentor_extract.id,
                    "mentor_name" : mentor_extract.name,
                    "source" : "twitter",
                    "source_url" : tweet["tweet_url"],
                }
            )
            documents.append(document)
        logger.info(f"Extracted {len(documents)} tweets from Twitter for {mentor_extract.id}")
        return documents    
    except Exception as e:
        logger.error(f"Error extracting tweets from Twitter for {mentor_extract.id} : {e}")
        return []

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