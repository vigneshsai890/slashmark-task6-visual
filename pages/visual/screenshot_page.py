from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ScreenshotPage(BasePage):
    GOOGLE_URL = "https://www.google.com"
    W3SCHOOLS_URL = "https://www.w3schools.com"
    GITHUB_URL = "https://github.com"

    HERO_SECTION = (By.CSS_SELECTOR, "body")
    NAVBAR = (By.TAG_NAME, "nav")
    FOOTER = (By.TAG_NAME, "footer")
    MAIN_CONTENT = (By.TAG_NAME, "main")

    def open_google(self):
        self.driver.get(self.GOOGLE_URL)
        return self

    def open_w3schools(self):
        self.driver.get(self.W3SCHOOLS_URL)
        return self

    def open_github(self):
        self.driver.get(self.GITHUB_URL)
        return self

    def take_full_page_screenshot(self, name):
        return self.take_screenshot(name)

    def take_element_screenshot(self, by, value, name):
        return super().take_element_screenshot(by, value, name)

    def get_page_dimensions(self):
        return self.driver.execute_script(
            "return {width: document.documentElement.scrollWidth, "
            "height: document.documentElement.scrollHeight}"
        )

    def set_viewport(self, width, height):
        self.driver.set_window_size(width, height)
