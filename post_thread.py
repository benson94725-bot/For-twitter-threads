import os
import time
from playwright.sync_api import sync_playwright

# --- Start of Selectors ---
# Selectors for the reply-based threading method.

# The main tweet composer text area on the home page.
HOME_TWEET_TEXTAREA = 'div[data-testid="tweetTextarea_0"]'

# The button to post the first tweet.
POST_FIRST_TWEET_BUTTON = '[aria-label="Post"]'

# The text area for writing a reply on a tweet's page.
REPLY_TEXTAREA = 'div[data-testid="tweetTextarea_0"]' # Often the same as the main composer

# The button to post a reply.
POST_REPLY_BUTTON = '[aria-label="Reply"]' # The reply button is usually labeled "Reply"

# A unique element on a tweet's page to confirm navigation.
TWEET_ARTICLE_SELECTOR = 'article[data-testid="tweet"]'

# --- End of Selectors ---

STATE_FILE = "state.json"

def post_tweet_thread(tweets: list[str]):
    """
    Posts a thread of tweets to Twitter by replying to the previous tweet.
    """
    if not tweets:
        print("No tweets to post.")
        return

    with sync_playwright() as p:
        browser = None
        context = None

        if os.path.exists(STATE_FILE):
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(storage_state=STATE_FILE)
            print("Using saved login state.")
        else:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page_for_login = context.new_page()
            page_for_login.goto("https://x.com/login")
            print("Please log in to Twitter in the browser window.")
            input("After logging in, press Enter here to continue...")
            context.storage_state(path=STATE_FILE)
            print(f"Login state saved to {STATE_FILE}")
            page_for_login.close()

        page = context.new_page()
        page.goto("https://x.com/")
        print("Successfully navigated to Twitter home page.")

        # Post the first tweet
        print(f"Posting first tweet: {tweets[0]}")
        page.wait_for_selector(HOME_TWEET_TEXTAREA).fill(tweets[0])
        page.wait_for_selector(POST_FIRST_TWEET_BUTTON).click()

        # Wait for navigation to the tweet page by looking for a unique element
        page.wait_for_selector(TWEET_ARTICLE_SELECTOR)
        last_tweet_url = page.url
        print(f"First tweet posted at: {last_tweet_url}")

        # Post subsequent tweets as replies
        for tweet_text in tweets[1:]:
            # The page is already on the last tweet's URL, so we can reply directly.
            print(f"Replying with: {tweet_text}")

            # Wait for reply textarea and fill it
            page.wait_for_selector(REPLY_TEXTAREA).fill(tweet_text)

            # Click the reply button
            page.wait_for_selector(POST_REPLY_BUTTON).click()

            # Wait for the new tweet to appear on the page
            page.wait_for_selector(f'article:has-text("{tweet_text}")')
            last_tweet_url = page.url # The URL might not change, but we update it just in case
            print(f"Replied successfully.")

        print("Tweet thread posted successfully!")
        browser.close()

if __name__ == "__main__":
    tweet_thread = [
        "This is the first tweet in the thread!",
        "This is the second tweet, continuing the discussion.",
        "And this is the third and final tweet."
    ]
    post_tweet_thread(tweet_thread)
    print("Tweet thread posted successfully!")
