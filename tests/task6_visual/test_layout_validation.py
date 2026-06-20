import pytest
from pages.visual.screenshot_page import ScreenshotPage


@pytest.mark.visual
class TestLayoutValidation:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.page = ScreenshotPage(driver)

    def test_google_logo_visible(self, driver):
        self.page.open_google()
        assert self.page.is_visible(*ScreenshotPage.HERO_SECTION)

    def test_w3schools_navbar(self, driver):
        self.page.open_w3schools()
        assert self.page.is_visible(*ScreenshotPage.NAVBAR)

    def test_github_footer(self, driver):
        self.page.open_github()
        assert self.page.is_visible(*ScreenshotPage.FOOTER)

    def test_page_width_desktop(self, driver):
        self.page.set_viewport(1920, 1080)
        self.page.open_google()
        dims = self.page.get_page_dimensions()
        assert dims["width"] >= 1920

    def test_page_width_tablet(self, driver):
        self.page.set_viewport(768, 1024)
        self.page.open_google()
        dims = self.page.get_page_dimensions()
        assert dims["width"] >= 768

    def test_page_width_mobile(self, driver):
        self.page.set_viewport(375, 667)
        self.page.open_google()
        dims = self.page.get_page_dimensions()
        assert dims["width"] >= 375

    def test_screenshot_after_resize(self, driver):
        self.page.set_viewport(1280, 720)
        self.page.open_google()
        path = self.page.take_full_page_screenshot("resized_1280")
        from PIL import Image
        img = Image.open(path)
        assert img.size[0] <= 1280

    def test_responsive_layout_consistency(self, driver):
        widths = [1920, 1280, 768, 375]
        for w in widths:
            self.page.set_viewport(w, 1080)
            self.page.open_google()
            dims = self.page.get_page_dimensions()
            assert dims["width"] >= w
