import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.visual_utils import visual_assert


BREAKPOINTS = {
    "desktop":  (1920, 1080),
    "laptop":   (1366, 768),
    "tablet":   (768,  1024),
    "mobile":   (375,  812),
}

TEST_URLS = {
    "home":    "https://demoqa.com",
    "forms":   "https://demoqa.com/automation-practice-form",
    "tables":  "https://demoqa.com/webtables",
    "widgets": "https://demoqa.com/widgets",
}


class TestVisualRegressionDesktop:

    def test_homepage_desktop_visual(self, driver):
        w, h = BREAKPOINTS["desktop"]
        driver.set_window_size(w, h)
        driver.get(TEST_URLS["home"])
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        result = visual_assert(driver, "homepage_desktop")
        assert result["passed"], (
            f"Visual diff {result['diff_ratio']:.2%} exceeds threshold. "
            f"See diff: {result.get('diff_path')}"
        )

    def test_forms_page_desktop_visual(self, driver):
        w, h = BREAKPOINTS["desktop"]
        driver.set_window_size(w, h)
        driver.get(TEST_URLS["forms"])
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "firstName"))
        )
        result = visual_assert(driver, "forms_desktop")
        assert result["passed"], f"Visual diff {result['diff_ratio']:.2%} exceeds threshold"

    def test_tables_page_desktop_visual(self, driver):
        w, h = BREAKPOINTS["desktop"]
        driver.set_window_size(w, h)
        driver.get(TEST_URLS["tables"])
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ReactTable"))
        )
        result = visual_assert(driver, "tables_desktop")
        assert result["passed"], f"Visual diff {result['diff_ratio']:.2%} exceeds threshold"


class TestVisualRegressionResponsive:

    def test_homepage_mobile_visual(self, driver):
        w, h = BREAKPOINTS["mobile"]
        driver.set_window_size(w, h)
        driver.get(TEST_URLS["home"])
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        result = visual_assert(driver, "homepage_mobile", threshold=0.08)
        assert result["passed"], f"Mobile visual diff {result['diff_ratio']:.2%} too high"

    def test_homepage_tablet_visual(self, driver):
        w, h = BREAKPOINTS["tablet"]
        driver.set_window_size(w, h)
        driver.get(TEST_URLS["home"])
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        result = visual_assert(driver, "homepage_tablet", threshold=0.08)
        assert result["passed"], f"Tablet visual diff {result['diff_ratio']:.2%} too high"

    def test_forms_mobile_visual(self, driver):
        w, h = BREAKPOINTS["mobile"]
        driver.set_window_size(w, h)
        driver.get(TEST_URLS["forms"])
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        result = visual_assert(driver, "forms_mobile", threshold=0.08)
        assert result["passed"], f"Mobile forms visual diff too high"

    def test_tables_tablet_visual(self, driver):
        w, h = BREAKPOINTS["tablet"]
        driver.set_window_size(w, h)
        driver.get(TEST_URLS["tables"])
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        result = visual_assert(driver, "tables_tablet", threshold=0.08)
        assert result["passed"], f"Tablet tables visual diff too high"


class TestVisualRegressionLaptop:

    def test_homepage_laptop_visual(self, driver):
        w, h = BREAKPOINTS["laptop"]
        driver.set_window_size(w, h)
        driver.get(TEST_URLS["home"])
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        result = visual_assert(driver, "homepage_laptop")
        assert result["passed"], f"Laptop visual diff {result['diff_ratio']:.2%} too high"

    def test_widgets_laptop_visual(self, driver):
        w, h = BREAKPOINTS["laptop"]
        driver.set_window_size(w, h)
        driver.get(TEST_URLS["widgets"])
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        result = visual_assert(driver, "widgets_laptop")
        assert result["passed"], f"Widgets laptop visual diff too high"
