import pytest
import os
from pages.visual.screenshot_page import ScreenshotPage
from utils.visual_comparator import VisualComparator


@pytest.mark.visual
class TestVisualRegression:
    @pytest.fixture(autouse=True)
    def setup(self, driver, update_baselines):
        self.page = ScreenshotPage(driver)
        self.comparator = VisualComparator(threshold=0.01)
        self.update_baselines = update_baselines
        os.makedirs("screenshots", exist_ok=True)

    def _take_and_compare(self, driver, url, baseline_name):
        self.page.driver.get(url)
        current_path = self.page.take_full_page_screenshot(f"current_{baseline_name}")

        if self.update_baselines:
            self.comparator.save_baseline(current_path, baseline_name)
            return {"match": True, "reason": "baseline_updated"}

        return self.comparator.compare(current_path, baseline_name)

    def test_google_regression(self, driver):
        result = self._take_and_compare(driver, "https://www.google.com", "google_home")
        assert result["match"], f"Visual mismatch: {result.get('mismatch_ratio', 'N/A')}"

    def test_github_regression(self, driver):
        result = self._take_and_compare(driver, "https://www.github.com", "github_home")
        assert result["match"], f"Visual mismatch: {result.get('mismatch_ratio', 'N/A')}"

    def test_w3schools_regression(self, driver):
        result = self._take_and_compare(driver, "https://www.w3schools.com", "w3schools_home")
        assert result["match"], f"Visual mismatch: {result.get('mismatch_ratio', 'N/A')}"

    def test_stackoverflow_regression(self, driver):
        result = self._take_and_compare(driver, "https://www.stackoverflow.com", "stackoverflow_home")
        assert result["match"], f"Visual mismatch: {result.get('mismatch_ratio', 'N/A')}"

    def test_baseline_not_found_returns_no_match(self, driver):
        self.page.open_google()
        current_path = self.page.take_full_page_screenshot("no_baseline_test")
        result = self.comparator.compare(current_path, "nonexistent_baseline")
        assert not result["match"]
        assert result["reason"] == "baseline_not_found"

    def test_diff_image_generated_on_mismatch(self, driver):
        self.page.open_google()
        current_path = self.page.take_full_page_screenshot("mismatch_test")
        self.comparator.save_baseline(current_path, "mismatch_baseline")

        driver.get("https://www.github.com")
        new_path = self.page.take_full_page_screenshot("mismatch_test_2")
        result = self.comparator.compare(new_path, "mismatch_baseline")

        if not result["match"]:
            assert result["diff_path"] is not None
            assert os.path.exists(result["diff_path"])
