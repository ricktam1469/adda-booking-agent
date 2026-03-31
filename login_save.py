from playwright.sync_api import sync_playwright

BOOKING_URL = "https://in.adda.io/myadda/facilities-index.php#/facilities"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # visible browser
    context = browser.new_context()

    page = context.new_page()
    page.goto(BOOKING_URL)

    print("\n🔐 Please login manually in the browser...")
    print("👉 After login & when booking page is visible, press ENTER here\n")

    input("Press ENTER after login...")

    # Save session
    context.storage_state(path="auth.json")

    print("✅ Login session saved to auth.json")

    browser.close()