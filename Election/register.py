import time
import datetime
import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# ============================================================
# SETTINGS
# ============================================================

URL = "https://ypgvote.vercel.app/reelection/register"

EXCEL_FILE = "list.xlsx"
RESULT_FILE = "registration_results.xlsx"

CONSTITUENCY = "Sunyani East"

# Set to False if you eventually want the browser hidden
HEADLESS = False

# Seconds to wait between registrations
DELAY_BETWEEN_REGISTRATIONS = 2


# ============================================================
# PHONE NUMBER FORMATTING (SOLUTION 1)
# ============================================================

def format_phone_number(value):
    """
    Ensures phone numbers retain their leading zero and 
    are formatted as a standard 10-digit Ghana mobile number.
    
    Examples:
        509029043   -> "0509029043"
        "509029043" -> "0509029043"
        "024 1234567" -> "0241234567"
    """
    # Convert to string and remove decimal points from pandas numeric types
    phone_str = str(value).split('.')[0].strip()
    
    # Keep only digits
    phone_str = ''.join(filter(str.isdigit, phone_str))
    
    # If Excel stripped the leading zero (making it 9 digits), restore it
    if len(phone_str) == 9:
        phone_str = '0' + phone_str
        
    return phone_str


# ============================================================
# DATE HANDLING
# ============================================================

def parse_date(value):
    """
    Convert the Excel date into day, month, year components.
    """
    date = pd.to_datetime(value)

    return {
        "day": str(date.day),
        "month": date.strftime("%B"),
        "year": str(date.year),
    }


# ============================================================
# SELECT CONSTITUENCY
# ============================================================

def select_constituency(page):
    """
    Interacts with the custom constituency combobox.
    """
    print("Selecting constituency...")

    # 1. Open the dropdown menu
    constituency_trigger = page.get_by_role("combobox", name="Constituency")
    constituency_trigger.click()
    page.wait_for_timeout(500)

    # 2. Attempt to type to filter options
    try:
        page.keyboard.type(CONSTITUENCY, delay=100)
        page.wait_for_timeout(500)
    except Exception:
        pass

    # 3. Target option via flexible matching strategies
    try:
        # Strategy A: Target explicit ARIA option role
        option = page.get_by_role("option", name=CONSTITUENCY)
        option.click(timeout=3000)
    except Exception:
        try:
            # Strategy B: Non-exact text search
            option = page.get_by_text(CONSTITUENCY, exact=False).first
            option.click(timeout=3000)
        except Exception:
            # Strategy C: Fallback to Enter key selection
            page.keyboard.press("Enter")

    page.wait_for_timeout(500)
    print(f"Constituency selected: {CONSTITUENCY}")


# ============================================================
# REGISTER ONE PERSON
# ============================================================

def register_person(page, person, index, total):

    person_id = str(person["ID"])
    name = str(person["Full Name"]).strip()
    
    # Apply Solution 1 to format phone number correctly
    phone = format_phone_number(person["Phone Number"])

    dob = parse_date(person["Date of Birth"])

    print()
    print("=" * 65)
    print(f"PERSON {index} OF {total}")
    print("=" * 65)

    print(f"ID: {person_id}")
    print(f"Name: {name}")
    print(
        f"DOB: {dob['day']} "
        f"{dob['month']} "
        f"{dob['year']}"
    )
    print(f"Phone: {phone}")
    print(f"Constituency: {CONSTITUENCY}")

    try:

        # ----------------------------------------------------
        # OPEN REGISTRATION PAGE
        # ----------------------------------------------------

        print("\nOpening registration page...")

        page.goto(
            URL,
            wait_until="networkidle"
        )

        page.wait_for_timeout(1000)

        # ----------------------------------------------------
        # FULL NAME
        # ----------------------------------------------------

        print("Filling full name...")

        page.get_by_label(
            "Full name"
        ).fill(name)

        # ----------------------------------------------------
        # DATE OF BIRTH
        # ----------------------------------------------------

        print("Filling date of birth...")

        page.get_by_label(
            "Day"
        ).fill(dob["day"])

        page.get_by_label(
            "Month"
        ).select_option(
            label=dob["month"]
        )

        page.get_by_label(
            "Year"
        ).fill(dob["year"])

        # ----------------------------------------------------
        # PHONE NUMBER
        # ----------------------------------------------------

        print("Filling phone number...")

        page.get_by_label(
            "Phone number"
        ).fill(phone)

        # ----------------------------------------------------
        # CONSTITUENCY
        # ----------------------------------------------------

        select_constituency(page)

        # ----------------------------------------------------
        # WAIT BEFORE SUBMITTING
        # ----------------------------------------------------

        page.wait_for_timeout(500)

        # ----------------------------------------------------
        # SUBMIT
        # ----------------------------------------------------

        print("Submitting registration...")

        submit_button = page.get_by_role(
            "button",
            name="Register to vote"
        )

        submit_button.click()

        # Give the website time to process response
        page.wait_for_timeout(1000)

        # ----------------------------------------------------
        # CHECK RESULT
        # ----------------------------------------------------

        body_text = page.locator("body").inner_text()
        body_lower = body_text.lower()

        print("\nWebsite response:")
        print(body_text[:1500])

        # ----------------------------------------------------
        # DETERMINE STATUS
        # ----------------------------------------------------

        if "already registered" in body_lower:

            status = "ALREADY REGISTERED"
            message = "Person was already registered"

        elif (
            "success" in body_lower
            or "successfully" in body_lower
            or "registration successful" in body_lower
            or "registered successfully" in body_lower
        ):

            status = "SUCCESS"
            message = "Registration completed successfully"

        elif (
            "error" in body_lower
            or "failed" in body_lower
            or "invalid" in body_lower
        ):

            status = "FAILED"
            message = "Website reported an error"

        else:

            status = "UNKNOWN"
            message = "Could not automatically determine result"

        print()
        print(f"RESULT: {status}")

        return {
            "ID": person_id,
            "Full Name": name,
            "Date of Birth": person["Date of Birth"],
            "Phone Number": phone,
            "Constituency": CONSTITUENCY,
            "Status": status,
            "Message": message,
        }

    except Exception as e:

        print()
        print("!" * 56)
        print("REGISTRATION ERROR")
        print("!" * 56)

        print(f"Person: {name}")
        print(f"Error: {e}")

        # ----------------------------------------------------
        # SAVE SCREENSHOT
        # ----------------------------------------------------

        screenshot_name = f"error_{person_id}.png"

        try:
            page.screenshot(
                path=screenshot_name,
                full_page=True
            )
            print(f"Screenshot saved: {screenshot_name}")
        except Exception:
            pass

        return {
            "ID": person_id,
            "Full Name": name,
            "Date of Birth": person["Date of Birth"],
            "Phone Number": phone,
            "Constituency": CONSTITUENCY,
            "Status": "ERROR",
            "Message": str(e),
        }


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print()
    print("=" * 65)
    print("YPG RE-ELECTION REGISTRATION AUTOMATION")
    print("=" * 65)

    # --------------------------------------------------------
    # READ EXCEL
    # --------------------------------------------------------

    print("\nReading Excel file...")

    try:
        df = pd.read_excel(EXCEL_FILE)
    except Exception as e:
        print("\nCould not open Excel file.")
        print(e)
        return

    # --------------------------------------------------------
    # CHECK COLUMNS
    # --------------------------------------------------------

    required_columns = [
        "ID",
        "Full Name",
        "Date of Birth",
        "Phone Number",
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        print("\nERROR: Missing Excel columns:")
        for col in missing_columns:
            print(f"  - {col}")
        print("\nYour Excel file should contain:")
        for col in required_columns:
            print(f"  - {col}")
        return

    total = len(df)
    print(f"\nFound {total} people to register.")
    print(f"Constituency for all people: {CONSTITUENCY}")

    # --------------------------------------------------------
    # START PLAYWRIGHT
    # --------------------------------------------------------

    results = []

    with sync_playwright() as p:

        print("\nStarting browser...")

        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page(
            viewport={"width": 1280, "height": 900}
        )

        for index, (_, person) in enumerate(df.iterrows(), start=1):

            result = register_person(
                page,
                person,
                index,
                total
            )

            results.append(result)

            if index < total:
                print(
                    f"\nWaiting {DELAY_BETWEEN_REGISTRATIONS} "
                    f"seconds before next person..."
                )
                time.sleep(DELAY_BETWEEN_REGISTRATIONS)

        browser.close()

    # --------------------------------------------------------
    # SAVE RESULTS (WITH PERMISSION ERROR FALLBACK)
    # --------------------------------------------------------

    print()
    print("=" * 65)
    print("SAVING RESULTS")
    print("=" * 65)

    results_df = pd.DataFrame(results)

    try:
        results_df.to_excel(RESULT_FILE, index=False)
        print(f"\nResults successfully saved to: {RESULT_FILE}")
    except PermissionError:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fallback_file = f"registration_results_{timestamp}.xlsx"
        results_df.to_excel(fallback_file, index=False)
        print(
            f"\nWARNING: Could not overwrite {RESULT_FILE} because it is open."
        )
        print(f"Saved results to fallback file: {fallback_file}")

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    success_count = sum(r["Status"] == "SUCCESS" for r in results)
    already_count = sum(r["Status"] == "ALREADY REGISTERED" for r in results)
    failed_count  = sum(r["Status"] == "FAILED" for r in results)
    error_count   = sum(r["Status"] == "ERROR" for r in results)
    unknown_count = sum(r["Status"] == "UNKNOWN" for r in results)

    print()
    print("=" * 65)
    print("REGISTRATION COMPLETE")
    print("=" * 65)

    print(f"Total people:       {total}")
    print(f"Successful:         {success_count}")
    print(f"Already registered: {already_count}")
    print(f"Failed:             {failed_count}")
    print(f"Errors:             {error_count}")
    print(f"Unknown:            {unknown_count}")
    print("=" * 65)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()