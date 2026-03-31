from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import time
import ctypes
import random

# 🔥 Prevent laptop sleep
ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)

BOOKING_URL = "https://in.adda.io/myadda/facilities-index.php#/facilities"
PREFERRED_TIME = "21:00"
FLAT_NAME = "B-606"
AMENITY_NAME = "Badminton Court"


# ⏰ TIME SCHEDULER
def get_target_time(hour, minute):
    now = datetime.now()
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

    if now >= target:
        target += timedelta(days=1)

    return target


def wait_until(target_time):
    print(f"⏳ Waiting until {target_time.strftime('%H:%M:%S')}")

    while True:
        if datetime.now() >= target_time:
            print("\n🚀 TIME REACHED !!!")
            break
        time.sleep(0.2)


# 📅 SELECT NEXT DAY
def select_next_day(page):
    target_date = datetime.now() + timedelta(days=2)
    day = str(target_date.day)

    print(f"📅 Selecting date: {day}")

    page.locator("#datepicker").click()
    time.sleep(1)

    cells = page.locator("//td[not(contains(@class,'disabled'))]")

    for i in range(cells.count()):
        cell = cells.nth(i)
        if cell.inner_text().strip() == day and cell.is_visible():
            cell.click()
            print("✅ Date selected")
            return

    raise Exception("❌ Date not found")


# 🏸 ENSURE AMENITY
def ensure_amenity_selected(page):
    print("🏸 Checking Amenity...")

    dropdown = page.locator("#fac_name")

    try:
        selected = dropdown.locator("option:checked").inner_text()
    except:
        selected = ""

    if AMENITY_NAME not in selected:
        print("⚠️ Selecting Amenity again")

        options = dropdown.locator("option")

        for i in range(options.count()):
            opt = options.nth(i)
            if AMENITY_NAME in opt.inner_text():
                dropdown.select_option(value=opt.get_attribute("value"))
                time.sleep(random.uniform(0.2, 0.5))
                print("✅ Amenity selected")
                return
    else:
        print("✅ Amenity already selected")


# ⏰ SELECT TIME (FIXED STRICT MATCH)
def select_time_slot(page):
    print("⏰ Selecting time...")

    dropdown = page.locator("select[name='fac_slot_id']")
    dropdown.wait_for(timeout=10000)
    time.sleep(random.uniform(0.5, 1.0))

    options = dropdown.locator("option")

    for i in range(options.count()):
        opt = options.nth(i)
        text = opt.inner_text().strip()

        # ✅ STRICT START MATCH ONLY
        if text.startswith(PREFERRED_TIME):
            dropdown.select_option(value=opt.get_attribute("value"))
            time.sleep(random.uniform(0.5, 1.0))
            print(f"✅ Selected slot: {text}")
            return

    print("⚠️ Preferred not found → fallback")
    dropdown.select_option(index=1)


# 🏠 SELECT FLAT
def select_book_for(page):
    print("🏠 Selecting flat...")

    dropdown = page.locator("select[ng-model='booking.flatId']")
    dropdown.wait_for(timeout=5000)

    options = dropdown.locator("option")

    for i in range(options.count()):
        opt = options.nth(i)
        if FLAT_NAME in opt.inner_text():
            dropdown.select_option(value=opt.get_attribute("value"))
            time.sleep(random.uniform(0.2, 0.5))
            print("✅ Flat selected")
            return

    raise Exception("❌ Flat not found")


# 🔍 VERIFY SUCCESS
def verify_booking_success(page):
    try:
        page.wait_for_selector("text=Reservation is successful!", timeout=5000)
        print("🎉 BOOKING CONFIRMED !!!")
        return True
    except:
        return False


# ⚡ SMART BUTTON FLOW (FIXED)
def smart_booking_step(page):
    print("⚡ Smart booking step...")

    try:
        # Check Availability (if present)
        if page.get_by_role("button", name="Check Availability").count() > 0:
            page.get_by_role("button", name="Check Availability").click()
            print("➡️ Clicked Check Availability")
            time.sleep(random.uniform(1, 2))

        # Direct Reserve (if already available)
        if page.get_by_role("button", name="Reserve Amenity").count() > 0:
            page.get_by_role("button", name="Reserve Amenity").click()
            print("➡️ Clicked Reserve")
            time.sleep(random.uniform(1, 2))

        return True

    except Exception as e:
        print(f"❌ Button flow failed: {e}")
        return False


# 🔁 FULL FLOW (FAIL SAFE)
def run_booking_flow(page):
    for attempt in range(3):
        print(f"\n🔁 ATTEMPT {attempt + 1}")

        try:
            ensure_amenity_selected(page)
            select_time_slot(page)
            select_book_for(page)

            smart_booking_step(page)

            if verify_booking_success(page):
                print("🏆 SUCCESSFULLY BOOKED")
                return True

        except Exception as e:
            print(f"⚠️ Error: {e}")

        print("🔄 Retrying...")

    print("❌ FAILED AFTER ALL ATTEMPTS")
    return False


# 🚀 MAIN
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]
    page = context.pages[0]

    print("✅ Connected to real Chrome")

    page.goto(BOOKING_URL)
    time.sleep(2)

    # Pre-setup
    ensure_amenity_selected(page)
    select_next_day(page)

    # ⏰ SET TIME
    target_time = get_target_time(6, 00)  # change to (6,0) for real
    wait_until(target_time)

    print("\n🚀 STARTING BOOKING FLOW")

    run_booking_flow(page)

    time.sleep(5)