import pytest
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.visual_utils import visual_assert, save_baseline, BASELINE_DIR


class TestBaselineManagement:
    """Tests for baseline creation and management workflow"""

    def test_baseline_created_on_first_run(self, driver):
        driver.set_window_size(1920, 1080)
        driver.get("https://demoqa.com")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        # delete baseline to simulate first run
        baseline_path = os.path.join(BASELINE_DIR, "baseline_test.png")
        if os.path.exists(baseline_path):
            os.remove(baseline_path)

        result = visual_assert(driver, "baseline_test")
        assert result.get("baseline_created") or result["passed"]
        assert os.path.exists(baseline_path), "Baseline file should be created"

    def test_baseline_file_is_valid_image(self, driver):
        driver.set_window_size(1920, 1080)
        driver.get("https://demoqa.com")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        path = save_baseline(driver, "valid_image_check")
        assert os.path.exists(path)
        assert os.path.getsize(path) > 1000, "Baseline PNG should not be empty"

    def test_identical_pages_pass_visual(self, driver):
        driver.set_window_size(1920, 1080)
        driver.get("https://demoqa.com")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        # take baseline, then compare same page immediately
        baseline_path = os.path.join(BASELINE_DIR, "identical_test.png")
        if os.path.exists(baseline_path):
            os.remove(baseline_path)

        # first run creates baseline
        visual_assert(driver, "identical_test")
        # second run compares same page
        result = visual_assert(driver, "identical_test")
        assert result["passed"], "Identical page should pass visual check"
        assert result["diff_ratio"] < 0.02, "Diff should be near zero for same page"

    def test_diff_image_generated_on_mismatch(self, driver):
        from PIL import Image
        from utils.visual_utils import CURRENT_DIR, DIFF_DIR, compare_images
        import numpy as np

        # create two different images manually
        img1 = Image.new("RGB", (100, 100), color=(255, 255, 255))
        img2 = Image.new("RGB", (100, 100), color=(0, 0, 0))

        os.makedirs(BASELINE_DIR, exist_ok=True)
        os.makedirs(CURRENT_DIR, exist_ok=True)
        os.makedirs(DIFF_DIR, exist_ok=True)

        b_path = os.path.join(BASELINE_DIR, "mismatch_baseline.png")
        c_path = os.path.join(CURRENT_DIR,  "mismatch_baseline.png")
        d_path = os.path.join(DIFF_DIR,     "mismatch_baseline_diff.png")

        img1.save(b_path)
        img2.save(c_path)

        result = compare_images(b_path, c_path, d_path, threshold=0.05)
        assert not result["passed"], "Black vs white image should fail visual check"
        assert os.path.exists(d_path), "Diff image should be generated"
