from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from django.core.cache import cache
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

FIDE_LOGIN_URL = "https://frs.fide.com/frslogin.phtml"
FIDE_REGISTERED_URL = "https://frs.fide.com/view_registered.phtml"
FIDE_USERNAME = os.getenv("FIDE_USERNAME")
FIDE_PASSWORD = os.getenv("FIDE_PASSWORD")

class FIDEClient:
    CACHE_KEY = "fide_session_cookie"

    @staticmethod
    def get_driver():
        logger.info("""Initialize and return a Selenium WebDriver.""")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        selenium_url = os.getenv("SELENIUM_REMOTE_URL")
        return webdriver.Remote(command_executor=selenium_url, options=chrome_options)

    @staticmethod
    def login():
        logger.info("""Log in to FIDE and store session cookies.""")
        driver = FIDEClient.get_driver()
        driver.get(FIDE_LOGIN_URL)

        # Fill in login credentials
        driver.find_element(By.NAME, "user").send_keys(FIDE_USERNAME)
        driver.find_element(By.NAME, "pass").send_keys(FIDE_PASSWORD)

        # Accept Terms & Conditions (if required)
        try:
            terms_checkbox = driver.find_element(By.NAME, "terms")
            if not terms_checkbox.is_selected():
                terms_checkbox.click()
        except:
            logger.warning("Terms & Conditions checkbox not found or already accepted.")

        # Click the Login button
        driver.save_screenshot("before_submit.png")
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        time.sleep(2)  # Wait for login to complete

        driver.save_screenshot("after_submit.png")
        # Store session cookies
        cookies = driver.get_cookies()
        cache.set(FIDEClient.CACHE_KEY, cookies, timeout=3600)

        logger.info("""Logged into FIDE FRS, returning.""")

        return driver  # Return WebDriver instance with session

    @staticmethod
    def fetch_registered_tournaments():
        logger.info("""Fetch registered tournaments using stored session cookies.""")
        cookies = cache.get(FIDEClient.CACHE_KEY)

        if cookies:
            logger.info("Using existing session cookies.")
            driver = FIDEClient.get_driver()
            driver.get(FIDE_LOGIN_URL)
            # Restore cookies
            for cookie in cookies:
                driver.add_cookie(cookie)
        else:
            logger.info("No valid session found. Logging in...")
            driver = FIDEClient.login()  # Log in and get a driver with a valid session

        # Now, always fetch tournaments
        driver.get(FIDE_REGISTERED_URL)
        time.sleep(2)  # Allow JavaScript to load

        # Get raw HTML of the page
        page_source = driver.page_source

        driver.quit()
        return page_source
