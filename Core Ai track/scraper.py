from playwright.sync_api import sync_playwright

def fetch_website_contents(url):
    print(f"Fetching website: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # networkidle ki jagah domcontentloaded use karo + timeout badhao
        page.goto(url, wait_until="domcontentloaded", timeout=60000)

        # Extra wait for JavaScript content
        page.wait_for_timeout(5000)

        text = page.locator("body").inner_text()

        browser.close()
        return text