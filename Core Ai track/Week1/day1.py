import requests
from bs4 import BeautifulSoup

from dotenv import load_dotenv
from IPython.display import Markdown, display

from call_llm import callingLLM

# ============================================================
# 1. SCRAPER
# ============================================================
from playwright.sync_api import sync_playwright


def fetch_website_contents(url):
    print(f"Fetching website: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(url, wait_until="networkidle")

        # Wait for JavaScript-rendered content
        page.wait_for_timeout(3000)

        text = page.locator("body").inner_text()

        browser.close()

        return text
    print(f"Fetching website: {url}")

    response = requests.get(url, timeout=10)

    # Raise an error if the website request failed
    response.raise_for_status()

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unnecessary elements
    for element in soup(["script", "style", "noscript"]):
        element.decompose()

    # Extract visible text
    text = soup.get_text(" ", strip=True)

    return text


deployment_name = "gpt-5.6-sol"

client=callingLLM()
response = client.chat.completions.create(model= deployment_name,messages=[{"role":"user","content":"Tell me a fun fact"}])
print(response.choices[0].message.content)

# ============================================================
# 3. SCRAPE YOUR WEBSITE
# ============================================================

url = "https://myportfolio1-wine.vercel.app/"

content = fetch_website_contents(url)

print("\n--- WEBSITE CONTENT ---")
print(content)


# ============================================================
# 4. SEND WEBSITE CONTENT TO GPT-5
# ============================================================

prompt = f"""
You are analyzing my portfolio website.

Here is the content scraped from the website:

{content}

Based only on this content:

1. Summarize the portfolio.
2. Tell me what technologies I know.
3. Tell me what projects I have worked on.
4. Tell me what my professional profile looks like.
"""

response = client.responses.create(
    model=deployment_name,
    input=prompt
)


# ============================================================
# 5. PRINT AI RESPONSE
# ============================================================

print("\n--- AI RESPONSE ---")
print(response.output_text)