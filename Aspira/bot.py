from playwright.sync_api import sync_playwright
from Aspira.config import BOT_PASSWORSD, BOT_EMAIL_ID
import re
from Aspira.interview import Interview

class BOT:
    def __init__(self, meet_url, name,interview_id) -> None:
        self.interview_id=interview_id
        
        try:
            self.start_interview(meet_url=meet_url, name=name)
        except Exception as e:
            print("Error signing into Google or Joining the meet")
            self.start_interview(meet_url=meet_url,name=name)
        self.browser=None
        
        """After Joining in the meet"""
        #
        # Check Camera
        # Check Microphone
        # Check any other buttons
        
        
    def sign_in_to_google_account(self, page):
        # Navigate to the Google login page
        page.goto(
            "https://accounts.google.com/",
        )
        # Fill in the email field and press Enter
        page.fill("#identifierId", BOT_EMAIL_ID)
        page.keyboard.press("Enter")

        # Wait for the password field to appear and fill it
        page.wait_for_selector("[name=Passwd]")
        page.fill("[name=Passwd]", BOT_PASSWORSD)
        page.keyboard.press("Enter")

        # Wait for the login to complete
        page.wait_for_url("https://myaccount.google.com/?pli=1")

    def join_google_meet(self, page, meet_url):
        # Navigate to the Google Meet URL
        page.goto(meet_url)

        # Click the "Join now" button
        join_button = page.locator("text=Join now")
        join_button.click()

    def extract_meeting_info(self, zoom_link):
        # Regular expression pattern to extract meeting ID and password
        pattern = (
            r"https://app.zoom.us/wc/(?P<meeting_id>\d+)/join/\?pwd=(?P<password>\w+)"
        )
        # pattern = (
        #     r"https://zoom.us/j/(?P<meeting_id>\d+)\?pwd=(?P<password>\w+)"
        # )
        # Attempt to match the pattern
        match = re.match(pattern, zoom_link)
        print(match)
        if match:
            meeting_id = match.group("meeting_id")
            password = match.group("password")

            return meeting_id, password
        else:
            return None, None

    def join_zoom_meet(self, page, meet_url):
        meeting_id, password = self.extract_meeting_info(meet_url)
        page.goto(f"https://app.zoom.us/wc/{meeting_id}/join/?pwd={password}")
        # join_button = page.locator("text=Join now")
        pwd = page.locator("#input-for-pwd")
        pwd.fill("jGnNk3")
        name = page.locator("#input-for-name")
        name.fill("Aspira")
        btn = page.get_by_role("button", name="Join", exact=True)
        btn.click()
        audio_btn = page.locator("button:has-text('Join Audio by Computer')")
        audio_btn.click()
        unmute_btn = page.locator('button[aria-label="unmute my microphone"]')
        unmute_btn.click()

    def start_interview(self, meet_url, name):
        with sync_playwright() as p:
            browser_type = p.chromium  # You can use 'firefox' or 'webkit' as well
            self.browser = browser_type.launch(
                headless=False, args=["--use-fake-ui-for-media-stream"]
            )

            context = self.browser.new_context()
            page = context.new_page()
            try:
                self.sign_in_to_google_account(page)

                meet_url = meet_url.strip('"')
                print("meet_url------------------->:", meet_url)
                if "zoom" in meet_url:
                    self.join_zoom_meet(page, meet_url)
                elif "google" in meet_url:
                    self.join_google_meet(page, meet_url)
                    import time
                    time.sleep(1)
                interview=Interview(f"loan_applications/{self.interview_id}.xlsx",interview_id=self.interview_id)
                interview.start_interview(name=name)
            except Exception as e:
                print("error is :'             -----------        ",e)
                raise Exception("Error occured", e)
            finally:
                self.browser.close()
                self.browser=None
            print(
                "---------------------          completed the Interview   --------------"
            )

    def end_interview(self):
        if self.browser:
            pass
        else:
            print("no browser")


# bot = BOT("https://meet.google.com/kfi-pdwq-yse", "sathwik")
