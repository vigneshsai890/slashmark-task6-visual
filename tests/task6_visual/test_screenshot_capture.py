import pytest
import os
from pages.visual.screenshot_page import ScreenshotPage


@pytest.mark.screenshot
class TestScreenshotCapture:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.page = ScreenshotPage(driver)
        os.makedirs("screenshots", exist_ok=True)

    def test_full_page_screenshot_google(self, driver):
        self.page.open_google()
        path = self.page.take_full_page_screenshot("google_full")
        assert os.path.exists(path)

    def test_full_page_screenshot_w3schools(self, driver):
        self.page.open_w3schools()
        path = self.page.take_full_page_screenshot("w3schools_full")
        assert os.path.exists(path)

    def test_full_page_screenshot_github(self, driver):
        self.page.open_github()
        path = self.page.take_full_page_screenshot("github_full")
        assert os.path.exists(path)

    def test_element_screenshot(self, driver):
        self.page.open_google()
        path = self.page.take_element_screenshot(*ScreenshotPage.HERO_SECTION, "google_body")
        assert os.path.exists(path)

    def test_screenshot_file_size(self, driver):
        self.page.open_google()
        path = self.page.take_full_page_screenshot("google_size_check")
        size = os.path.getsize(path)
        assert size > 0

    def test_screenshot_dimensions(self, driver):
        self.page.open_google()
        self.page.take_full_page_screenshot("google_dims")
        from PIL import Image
        img = Image.open("screenshots/google_dims.png")
        assert img.size[0] > 0 and img.size[1] > 0

    @pytest.mark.parametrize("url,name", [
        ("https://www.google.com", "google"),
        ("https://www.github.com", "github"),
        ("https://www.stackoverflow.com", "stackoverflow"),
    ])
    def test_multiple_site_screenshots(self, driver, url, name):
        driver.get(url)
        path = self.page.take_full_page_screenshot(name)
        assert os.path.exists(path)
