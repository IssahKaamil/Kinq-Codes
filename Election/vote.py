import time
import datetime
import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# ============================================================
# SETTINGS
# ============================================================

LOGIN_URL = "https://ypgvote.vercel.app/reelection/login"
EXCEL_FILE = "vote_list.xlsx"
RESULT_FILE = "vote_list_results.xlsx"

HEADLESS = False
DELAY_BETWEEN_ACTIONS = 0.5  # Seconds between UI steps
INTER_ACCOUNT_DELAY = 0.1     # Seconds delay before logging in the next voter


# ============================================================
# CUSTOM EXCEPTIONS
# ============================================================

class VotingAutomationError(Exception):
    """Base exception for voting automation."""
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"[{status_code}] {message}")


class LoginError(VotingAutomationError):
    """Raised when authentication fails."""
    pass


class CandidateSelectionError(VotingAutomationError):
    """Raised when candidate selection fails."""
    pass


class VotingError(VotingAutomationError):
    """Raised when casting the vote fails."""
    pass


# ============================================================
# DATA FORMATTING HELPERS
# ============================================================

def format_phone_number(value):
    """
    Ensures phone numbers retain their leading zero and 
    are formatted as a standard 10-digit Ghana mobile number.
    """
    if pd.isna(value):
        raise ValueError("Phone number is empty or missing")

    phone_str = str(value).split('.')[0].strip()
    phone_str = ''.join(filter(str.isdigit, phone_str))
    
    if len(phone_str) == 9:
        phone_str = '0' + phone_str
    elif len(phone_str) == 12 and phone_str.startswith('233'):
        phone_str = '0' + phone_str[3:]

    if len(phone_str) != 10 or not phone_str.startswith('0'):
        raise ValueError(f"Invalid Ghana mobile format: '{value}' -> parsed as '{phone_str}'")
        
    return phone_str


def parse_date(value):
    """
    Convert the Excel date into Day, Month (full name), Year components.
    """
    if pd.isna(value):
        raise ValueError("Date of Birth is empty or missing")

    try:
        date = pd.to_datetime(value)
        return {
            "day": str(date.day),
            "month": date.strftime("%B"),  # e.g. "January", "February"
            "year": str(date.year),
        }
    except Exception as e:
        raise ValueError(f"Could not parse Date of Birth '{value}': {e}")


# ============================================================
# WORKFLOW ACTIONS
# ============================================================

def reset_to_login(page, context):
    """Clears session storage, cookies, and navigates back to the login page."""
    try:
        context.clear_cookies()
        page.goto(LOGIN_URL, wait_until="networkidle", timeout=30000)
        page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")
        page.reload(wait_until="networkidle")
    except Exception as e:
        print(f" -> [RESET WARNING] Could not reset state cleanly: {e}")
        page.goto(LOGIN_URL, wait_until="domcontentloaded")


def login(page, phone, dob_parsed):
    """Navigates to login page, submits credentials, and verifies authentication."""
    print(f"Logging in: {phone} | DOB: {dob_parsed['day']} {dob_parsed['month']} {dob_parsed['year']}")

    if LOGIN_URL not in page.url:
        page.goto(LOGIN_URL, wait_until="networkidle", timeout=30000)

    page.wait_for_timeout(1000)

    # 1. Fill Phone Number via character-by-character typing to fire JS state events
    phone_input = page.get_by_label("Phone number")
    phone_input.click()
    phone_input.focus()
    phone_input.press("Control+A")
    phone_input.press("Backspace")
    phone_input.press_sequentially(phone, delay=80)

    # 2. Fill Date of Birth
    page.get_by_label("Day").fill(dob_parsed["day"])
    page.get_by_label("Month").select_option(label=dob_parsed["month"])
    page.get_by_label("Year").fill(dob_parsed["year"])

    # 3. Submit Login Form
    page.get_by_role("button", name="Sign in").click()
    page.wait_for_timeout(2500)

    # 4. Check for URL progression / successful login indicators
    current_url = page.url.lower()
    body_text = page.locator("body").inner_text()
    body_lower = body_text.lower()

    if "/vote" in current_url or "cast your vote" in body_lower or "re-election ballot" in body_lower:
        print(" -> Login successful")
        return

    # 5. Handle Specific UI Error Messages
    if "no registration record" in body_lower or "record not found" in body_lower or "not registered" in body_lower:
        raise LoginError("ACCOUNT_NOT_REGISTERED", "No voter record exists for this phone number and DOB combination.")

    if "phone number does not match" in body_lower or "incorrect date of birth" in body_lower or "invalid credentials" in body_lower:
        raise LoginError("CREDENTIAL_MISMATCH", "The provided Date of Birth does not match the registered phone number.")

    if "enter a valid ghana mobile number" in body_lower or "invalid phone" in body_lower:
        raise LoginError("INVALID_PHONE_PORTAL_REJECT", "The portal rejected the phone number structure.")

    if "18 to 35" in body_lower or "age constraint" in body_lower or "too young" in body_lower or "too old" in body_lower:
        raise LoginError("AGE_ELIGIBILITY_ERROR", "The Date of Birth falls outside the required age range.")

    if "too many attempts" in body_lower or "rate limit" in body_lower or "try again later" in body_lower:
        raise LoginError("RATE_LIMITED_BY_SERVER", "Server rate-limited requests. Increase delay between accounts.")

    if "500" in body_lower or "internal server error" in body_lower or "application error" in body_lower:
        raise LoginError("SERVER_500_ERROR", "The voting portal encountered an internal server error.")

    # Generic Fallback Error
    clean_snippet = body_text[:150].replace("\n", " ").strip()
    raise LoginError("UNHANDLED_LOGIN_FAILURE", f"Login failed. Portal message: '{clean_snippet}'")


def select_candidate(page, candidate_name="Hon. Anaba Stanislaus Suguru"):
    """Locates and selects the specified candidate on the ballot."""
    print(f"Selecting candidate: {candidate_name}")

    try:
        candidate_card = page.get_by_text(candidate_name, exact=False)
        candidate_card.wait_for(state="visible", timeout=10000)
        candidate_card.click()
        page.wait_for_timeout(int(DELAY_BETWEEN_ACTIONS * 1000))
        print(" -> Candidate selected")
    except PlaywrightTimeoutError:
        raise CandidateSelectionError(
            "CANDIDATE_NOT_FOUND", 
            f"Candidate '{candidate_name}' was not found or visible on the page within 10 seconds."
        )


def open_and_confirm_vote(page):
    """Scrolls to the submit button, opens confirmation modal, and confirms the vote."""
    print("Submitting ballot...")

    try:
        submit_button = page.get_by_role("button", name="Submit my vote")
        submit_button.scroll_into_view_if_needed()
        page.wait_for_timeout(int(DELAY_BETWEEN_ACTIONS * 1000))
        submit_button.click()
    except Exception as e:
        raise VotingError("SUBMIT_BUTTON_CLICK_FAILED", f"Could not click initial submit button: {e}")

    try:
        confirm_button = page.get_by_role("button", name="Yes, cast my vote")
        confirm_button.wait_for(state="visible", timeout=5000)
        confirm_button.click()
        page.wait_for_timeout(1000)
        print(" -> Vote successfully cast")
    except PlaywrightTimeoutError:
        raise VotingError("CONFIRMATION_MODAL_TIMEOUT", "Confirmation modal did not appear or 'Yes, cast my vote' button was missing.")


# ============================================================
# MAIN AUTOMATION ENGINE
# ============================================================

def process_voter(page, row, index):
    """Processes a single row from the Excel dataset."""
    raw_phone = row.get("Phone Number", "")
    raw_dob = row.get("Date of Birth", "")

    # Pre-validation phase
    try:
        phone = format_phone_number(raw_phone)
    except ValueError as e:
        print(f" -> [PRE-VALIDATION ERROR] Phone: {e}")
        return {
            "Index": index,
            "Phone Number": str(raw_phone),
            "Date of Birth": str(raw_dob),
            "Status": "INVALID_EXCEL_PHONE",
            "Message": str(e),
            "URL": "N/A"
        }

    try:
        dob_parsed = parse_date(raw_dob)
    except ValueError as e:
        print(f" -> [PRE-VALIDATION ERROR] DOB: {e}")
        return {
            "Index": index,
            "Phone Number": phone,
            "Date of Birth": str(raw_dob),
            "Status": "INVALID_EXCEL_DOB",
            "Message": str(e),
            "URL": "N/A"
        }

    # Browser interaction phase
    try:
        login(page, phone, dob_parsed)
        select_candidate(page)
        open_and_confirm_vote(page)

        return {
            "Index": index,
            "Phone Number": phone,
            "Date of Birth": str(raw_dob),
            "Status": "SUCCESS",
            "Message": "Vote successfully cast and confirmed",
            "URL": page.url
        }

    except VotingAutomationError as e:
        print(f" -> [PROCESS ERROR] {e.status_code}: {e.message}")
        page.screenshot(path=f"error_{index}_{e.status_code.lower()}.png", full_page=True)
        return {
            "Index": index,
            "Phone Number": phone,
            "Date of Birth": str(raw_dob),
            "Status": e.status_code,
            "Message": e.message,
            "URL": page.url
        }

    except PlaywrightTimeoutError:
        err_msg = "Playwright network or selector timeout exceeded (30s)"
        print(f" -> [TIMEOUT ERROR] {err_msg}")
        page.screenshot(path=f"error_{index}_timeout.png", full_page=True)
        return {
            "Index": index,
            "Phone Number": phone,
            "Date of Birth": str(raw_dob),
            "Status": "NETWORK_TIMEOUT",
            "Message": err_msg,
            "URL": page.url
        }

    except Exception as e:
        clean_msg = str(e).replace("\n", " ")
        print(f" -> [UNHANDLED ERROR] {clean_msg}")
        try:
            page.screenshot(path=f"error_{index}_unhandled.png", full_page=True)
        except Exception:
            pass
        return {
            "Index": index,
            "Phone Number": phone,
            "Date of Birth": str(raw_dob),
            "Status": "UNHANDLED_EXCEPTION",
            "Message": clean_msg,
            "URL": page.url
        }


def main():
    print("\n" + "=" * 65)
    print("YPG VOTE AUTOMATION & AUDIT SUITE")
    print("=" * 65)

    try:
        df = pd.read_excel(EXCEL_FILE, dtype=str)
        print(f"Loaded '{EXCEL_FILE}' successfully. Found {len(df)} records.")
    except FileNotFoundError:
        print(f"FATAL ERROR: File '{EXCEL_FILE}' not found.")
        return
    except Exception as e:
        print(f"FATAL ERROR: Failed to load Excel file: {e}")
        return

    results = []

    with sync_playwright() as p:
        print("Launching persistent browser instance...")
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        total = len(df)
        for i, (_, row) in enumerate(df.iterrows(), start=1):
            print("\n" + "-" * 60)
            print(f"PROCESSING RECORD {i} OF {total}")
            print("-" * 60)

            # Process the voter on the open page
            res = process_voter(page, row, i)
            results.append(res)

            # Reset back to login page for the next record
            if i < total:
                print("Resetting state and returning to login page...")
                reset_to_login(page, context)
                if INTER_ACCOUNT_DELAY > 0:
                    time.sleep(INTER_ACCOUNT_DELAY)

        browser.close()

    # Output Management
    print("\n" + "=" * 65)
    print("SAVING RESULTS")
    print("=" * 65)
    
    results_df = pd.DataFrame(results)

    try:
        results_df.to_excel(RESULT_FILE, index=False)
        print(f"Results successfully saved to: {RESULT_FILE}")
    except PermissionError:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fallback_file = f"vote_results_{timestamp}.xlsx"
        results_df.to_excel(fallback_file, index=False)
        print(f"[WARNING] Could not write to '{RESULT_FILE}' (file open). Saved to '{fallback_file}' instead.")

    # Execution Summary Tally
    print("\n" + "=" * 65)
    print("EXECUTION SUMMARY")
    print("=" * 65)
    print(f"Total Records Processed: {total}")
    print(f"  - SUCCESS:               {sum(r['Status'] == 'SUCCESS' for r in results)}")
    print(f"  - ACCOUNT_NOT_REGISTERED:{sum(r['Status'] == 'ACCOUNT_NOT_REGISTERED' for r in results)}")
    print(f"  - CREDENTIAL_MISMATCH:   {sum(r['Status'] == 'CREDENTIAL_MISMATCH' for r in results)}")
    print(f"  - FORMAT ERRORS:         {sum('INVALID_EXCEL' in r['Status'] for r in results)}")
    print(f"  - SYSTEM / OTHER ERRORS: {sum(r['Status'] not in ['SUCCESS', 'ACCOUNT_NOT_REGISTERED', 'CREDENTIAL_MISMATCH'] and 'INVALID_EXCEL' not in r['Status'] for r in results)}")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()