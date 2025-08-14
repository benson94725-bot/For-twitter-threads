# Twitter Thread Poster

This script automates posting threads on Twitter using Playwright.

## Features

- Logs in to Twitter once and saves the session for future use.
- Posts a thread of multiple tweets.
- Runs locally without needing a server.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Install dependencies:**
    Make sure you have Python 3.7+ installed.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Playwright browsers:**
    ```bash
    playwright install
    ```

## Usage

1.  **Configure the tweet thread:**
    Open `post_thread.py` and modify the `tweet_thread` list in the `if __name__ == "__main__":` block.

    ```python
    if __name__ == "__main__":
        tweet_thread = [
            "This is the first tweet of your thread.",
            "This is the second tweet.",
            "And so on..."
        ]
        post_tweet_thread(tweet_thread)
    ```

2.  **Run the script:**
    ```bash
    python post_thread.py
    ```

### First Run (Login)

On the first run, a browser window will open. You need to log in to your Twitter account manually. After you log in, go back to your terminal and press `Enter`. Your session details will be saved in `state.json`, so you won't have to log in again.

### Subsequent Runs

On subsequent runs, the script will use the saved session in `state.json` to log in automatically and post the tweets in headless mode (no browser window will be visible).

## How it Works

The script uses the Playwright library to control a web browser. It automates the steps of logging in, composing a tweet, adding more tweets to create a thread, and posting the thread.

## `.gitignore`

The `state.json` file, which contains your session cookies, is included in the `.gitignore` file to prevent it from being accidentally committed to version control.
