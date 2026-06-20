import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def find_all(self, by, value):
        return self.wait.until(EC.presence_of_all_elements_located((by, value)))

    def click(self, by, value):
        from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
        import time
        for _ in range(3):
            try:
                self.wait.until(EC.element_to_be_clickable((by, value))).click()
                return
            except StaleElementReferenceException:
                time.sleep(0.5)
            except TimeoutException as e:
                print(f"\nTimeoutException waiting for {(by, value)} to be clickable.")
                print(f"Current URL: {self.driver.current_url}")
                self.driver.save_screenshot("error_screenshot.png")
                raise e
        self.wait.until(EC.element_to_be_clickable((by, value))).click()

    def type_text(self, by, value, text):
        from selenium.common.exceptions import StaleElementReferenceException
        import time
        for _ in range(3):
            try:
                element = self.wait.until(EC.visibility_of_element_located((by, value)))
                element.clear()
                element.send_keys(text)
                return
            except StaleElementReferenceException:
                time.sleep(0.5)
        element = self.wait.until(EC.visibility_of_element_located((by, value)))
        element.clear()
        element.send_keys(text)

    def get_text(self, by, value):
        return self.find(by, value).text

    def is_visible(self, by, value, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except:
            return False

    @property
    def current_url(self):
        return self.driver.current_url

    @property
    def title(self):
        return self.driver.title

    def take_screenshot(self, name, directory="screenshots"):
        os.makedirs(directory, exist_ok=True)
        path = f"{directory}/{name}.png"
        self.driver.save_screenshot(path)
        return path

    def take_element_screenshot(self, by, value, name, directory="screenshots"):
        os.makedirs(directory, exist_ok=True)
        element = self.find(by, value)
        path = f"{directory}/{name}.png"
        element.screenshot(path)
        return path
