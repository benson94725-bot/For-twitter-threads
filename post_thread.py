import os
import time
from playwright.sync_api import sync_playwright

# --- Start of Selectors ---
# Selectors for Twitter UI elements. These may change over time.
# If the script fails, you may need to update these selectors.
# See the README.md for instructions on how to find new selectors.

# The button on the side navigation to open the tweet composer
NEW_TWEET_BUTTON = 'a[data-testid="SideNav_NewTweet_Button"]'

# The main text area for the first tweet in the composer
TWEET_TEXTAREA_FIRST = 'div[data-testid="tweetTextarea_0"]'

# The text area for subsequent tweets in a thread. The '{i}' will be replaced with the tweet index.
TWEET_TEXTAREA_SUBSEQUENT = 'div[data-testid="tweetTextarea_{i}"]'

# The button to add another tweet to the thread.
ADD_TWEET_BUTTON = 'div[aria-label*="Add"]' # Using a partial match for the aria-label

# The button to post the entire thread.
POST_THREAD_BUTTON = 'div[data-testid="tweetButton"]'

# --- End of Selectors ---

STATE_FILE = "state.json"

def post_tweet_thread(tweets: list[str]):
    """
    Posts a thread of tweets to Twitter.
    This function will log in and save the session state if it's the first run.
    On subsequent runs, it will use the saved session to post tweets.
    """
    with sync_playwright() as p:
        browser = None
        context = None

        if os.path.exists(STATE_FILE):
            # If state file exists, launch browser in headless mode and use saved state
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(storage_state=STATE_FILE)
            print("Using saved login state.")
        else:
            # If state file does not exist, launch browser in headed mode for login
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto("https://x.com/login")
            print("Please log in to Twitter in the browser window that has opened.")
            input("After logging in, press Enter here to continue...")

            # Save the storage state to a file
            context.storage_state(path=STATE_FILE)
            print(f"Login state saved to {STATE_FILE}")

        # At this point, we should be logged in.
        page = context.new_page()
        page.goto("https://x.com/")

        print("Successfully navigated to Twitter home page.")

        if not tweets:
            print("No tweets to post.")
            browser.close()
            return

        # Wait for the main tweet button to be visible and click it
        page.wait_for_selector(NEW_TWEET_BUTTON).click()

        # Wait for the tweet composer to appear and type the first tweet
        first_tweet_composer = page.wait_for_selector(TWEET_TEXTAREA_FIRST)
        first_tweet_composer.fill(tweets[0])

        # Add subsequent tweets to the thread
        for i, tweet_text in enumerate(tweets[1:], start=1):
            add_button = page.wait_for_selector(ADD_TWEET_BUTTON)
            add_button.click()

            # Wait for the next tweet box to appear and type the tweet
            next_tweet_composer_selector = TWEET_TEXTAREA_SUBSEQUENT.format(i=i)
            next_tweet_composer = page.wait_for_selector(next_tweet_composer_selector)
            next_tweet_composer.fill(tweet_text)

        # Wait for the "Tweet all" button to be clickable and click it
        tweet_all_button = page.wait_for_selector(POST_THREAD_BUTTON)
        tweet_all_button.click()

        print("Tweet thread posted successfully.")

        # Wait for a few seconds to ensure the tweet is posted
        time.sleep(5)

        browser.close()

if __name__ == "__main__":
    tweet_thread = [
        "This is the first tweet in the thread!",
        "This is the second tweet, continuing the discussion.",
        "And this is the third and final tweet."
    ]
    post_tweet_thread(tweet_thread)
    print("Tweet thread posted successfully!")
