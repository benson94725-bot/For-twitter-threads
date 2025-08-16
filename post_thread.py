import os
import time
from playwright.sync_api import sync_playwright

# --- Start of Selectors ---
# Selectors for the "Single Composer" thread method.

# The button on the side navigation to open the tweet composer.
NEW_TWEET_BUTTON = 'a[data-testid="SideNav_NewTweet_Button"]'

# The text area for the first tweet in the composer.
TWEET_TEXTAREA_FIRST = 'div[data-testid="tweetTextarea_0"]'

# The button to add another tweet to the thread (the '+' button).
ADD_TWEET_BUTTON = '[aria-label*="Add"]'

# The text area for subsequent tweets (2nd, 3rd, etc.). {i} is the index.
TWEET_TEXTAREA_SUBSEQUENT = 'div[data-testid="tweetTextarea_{i}"]'

# The final button to post the entire thread.
POST_THREAD_BUTTON = 'button[data-testid="tweetButton"]'

# A selector for the "Your post was sent" confirmation message.
POST_SUCCESS_MESSAGE = 'div[data-testid="toast"]'

# --- End of Selectors ---

STATE_FILE = "state.json"

def post_tweet_thread(tweets: list[str]):
    """
    Posts a thread of tweets using the "single composer" method.
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

        # Open the tweet composer
        page.wait_for_selector(NEW_TWEET_BUTTON).click()

        # Write the first tweet
        page.wait_for_selector(TWEET_TEXTAREA_FIRST).fill(tweets[0])

        # Write subsequent tweets
        for i, tweet_text in enumerate(tweets[1:], start=1):
            page.wait_for_selector(ADD_TWEET_BUTTON).click()
            selector = TWEET_TEXTAREA_SUBSEQUENT.format(i=i)
            page.wait_for_selector(selector).fill(tweet_text)

        # Post the entire thread
        page.wait_for_selector(POST_THREAD_BUTTON).click()

        # Wait for the success message to appear
        page.wait_for_selector(POST_SUCCESS_MESSAGE)

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
