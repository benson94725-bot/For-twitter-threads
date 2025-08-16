# Twitter Thread Poster

This script automates posting threads on Twitter using a reliable reply-based method.

## Features

- Logs in to Twitter once and saves the session for future use.
- Posts a thread of multiple tweets by replying to the previous one.
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

2.  **Run the script:**
    ```bash
    python post_thread.py
    ```

### First Run (Login)

On the first run, a browser window will open. You need to log in to your Twitter account manually. After you log in, go back to your terminal and press `Enter`. Your session details will be saved in `state.json`.

### Subsequent Runs

On subsequent runs, the script will use the saved session in `state.json` to log in automatically and post the tweets in headless mode (no browser window will be visible).

---

## How it Works

The script uses the Playwright library to control a web browser. It creates a thread using the following logic:

1.  It posts the first tweet from your home timeline.
2.  It waits for the page to redirect to the new tweet's URL and saves that URL.
3.  For every subsequent tweet in your list, it navigates to the URL of the *previous* tweet and posts the new tweet as a reply.
4.  This process continues until all tweets are posted, creating a chain of replies that forms a thread.

This method is more reliable than using the UI's "Add to thread" button, which can change frequently.

---

## Troubleshooting

### The script fails with a `TimeoutError`

This is the most common issue and it usually means that Twitter has updated its website structure, causing the script's selectors to become outdated.

To fix this, you need to find the new selector for the element that the script is failing to find.

### How to find and update selectors

1.  **Force the browser to be visible:**
    The script runs in headless mode when `state.json` is present. To debug, **delete the `state.json` file** to force the script to open a visible browser window.

2.  **Run the script and open Developer Tools:**
    Run `python post_thread.py`. When the browser opens, press `F12` or `Ctrl+Shift+I` (`Cmd+Option+I` on Mac) to open the Developer Tools.

3.  **Find the element and its selector:**
    *   In Developer Tools, use the "element picker" tool to click on the button or element that is causing the script to fail.
    *   The HTML for that element will be highlighted. Look for a stable attribute like `data-testid` or `aria-label`.

4.  **Update the selectors in `post_thread.py`:**
    *   Open `post_thread.py`. At the top of the file, you will find the selector constants.
    *   Replace the value of the outdated selector with the new one you found.
    *   Save the file and try running the script again.
