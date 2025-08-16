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

2.  **Run the script:**
    ```bash
    python post_thread.py
    ```

### First Run (Login)

On the first run, a browser window will open. You need to log in to your Twitter account manually. After you log in, go back to your terminal and press `Enter`. Your session details will be saved in `state.json`.

### Subsequent Runs

On subsequent runs, the script will use the saved session in `state.json` to log in automatically and post the tweets in headless mode (no browser window will be visible).

---

## Troubleshooting

### The script fails with a `TimeoutError`

This is the most common issue and it usually means that Twitter has updated its website structure, causing the script's selectors to become outdated. The error message will typically say something like `Timeout 30000ms exceeded. waiting for locator(...)`.

To fix this, you need to find the new selector for the element that the script is failing to find.

### How to find and update selectors

1.  **Force the browser to be visible:**
    The script runs in headless mode (no visible browser) when a `state.json` file is present. To debug, you need to see what the script is doing. **Delete the `state.json` file** to force the script to open a visible browser window for a new login.

2.  **Run the script and open Developer Tools:**
    Run `python post_thread.py`. When the browser window opens to the Twitter login page, press `F12` or `Ctrl+Shift+I` (or `Cmd+Option+I` on Mac) to open the Developer Tools.

3.  **Find the element and its selector:**
    *   In the Developer Tools, click on the "Inspector" or "Elements" tab.
    *   Click the "element picker" tool (it usually looks like a mouse cursor in a box).
    *   On the Twitter page, click on the button or element that the script is failing to find (e.g., the "Add to thread" button).
    *   The HTML for that element will be highlighted in the Developer Tools.
    *   Look for a stable and unique attribute for the element, such as `data-testid`, `aria-label`, or a unique `id`. `data-testid` is usually the most reliable.

4.  **Update the selectors in `post_thread.py`:**
    *   Open `post_thread.py` in a text editor.
    *   At the top of the file, you will find a section with selector constants (e.g., `NEW_TWEET_BUTTON`, `ADD_TWEET_BUTTON`).
    *   Replace the value of the outdated selector with the new one you found. For example, if you found a new `data-testid` for the "Add Tweet" button, you would change the `ADD_TWEET_BUTTON` constant.
    *   Save the file and try running the script again.

---

## How it Works

The script uses the Playwright library to control a web browser. It automates the steps of logging in, composing a tweet, adding more tweets to create a thread, and posting the thread.

## `.gitignore`

The `state.json` file, which contains your session cookies, is included in the `.gitignore` file to prevent it from being accidentally committed to version control.
