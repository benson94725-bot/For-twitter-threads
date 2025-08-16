import os
import time
from playwright.sync_api import sync_playwright

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
        new_tweet_button_selector = 'a[data-testid="SideNav_NewTweet_Button"]'
        page.wait_for_selector(new_tweet_button_selector).click()

        # Wait for the tweet composer to appear and type the first tweet
        first_tweet_composer_selector = 'div[data-testid="tweetTextarea_0"]'
        first_tweet_composer = page.wait_for_selector(first_tweet_composer_selector)
        first_tweet_composer.fill(tweets[0])

        # Add subsequent tweets to the thread
        for i, tweet_text in enumerate(tweets[1:], start=1):
            # Selector for the "Add to thread" button.
            # Twitter UI can change, so if this fails, you might need to find the new selector.
            # Alternative selectors to try:
            # add_tweet_button_selector = 'div[aria-label*="Add"]'
            # add_tweet_button_selector = 'button[data-testid="addButton"]'
            add_tweet_button_selector = '[data-testid="addTweet"]'

            add_button = page.wait_for_selector(add_tweet_button_selector)
            add_button.click()

            # Wait for the next tweet box to appear and type the tweet
            next_tweet_composer_selector = f'div[data-testid="tweetTextarea_{i}"]'
            next_tweet_composer = page.wait_for_selector(next_tweet_composer_selector)
            next_tweet_composer.fill(tweet_text)

        # Wait for the "Tweet all" button to be clickable and click it
        tweet_all_button_selector = 'div[data-testid="tweetButton"]'
        tweet_all_button = page.wait_for_selector(tweet_all_button_selector)
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
