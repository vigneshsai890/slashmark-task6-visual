import os
from PIL import Image, ImageChops
import math


BASELINE_DIR = os.path.join(os.path.dirname(__file__), "..", "baselines")
CURRENT_DIR  = os.path.join(os.path.dirname(__file__), "..", "screenshots", "current")
DIFF_DIR     = os.path.join(os.path.dirname(__file__), "..", "screenshots", "diff")


def save_screenshot(driver, name: str, directory: str) -> str:
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, f"{name}.png")
    driver.save_screenshot(path)
    return path


def save_baseline(driver, name: str) -> str:
    return save_screenshot(driver, name, BASELINE_DIR)


def save_current(driver, name: str) -> str:
    return save_screenshot(driver, name, CURRENT_DIR)


def compare_images(baseline_path: str, current_path: str, diff_path: str, threshold: float = 0.05) -> dict:
    """Compare two images. Returns dict with passed bool and diff_ratio."""
    os.makedirs(os.path.dirname(diff_path), exist_ok=True)

    baseline = Image.open(baseline_path).convert("RGB")
    current  = Image.open(current_path).convert("RGB")

    # resize current to baseline size if needed
    if baseline.size != current.size:
        current = current.resize(baseline.size, Image.LANCZOS)

    diff = ImageChops.difference(baseline, current)
    diff.save(diff_path)

    # calculate diff ratio
    pixels = list(diff.getdata())
    total = len(pixels) * 3
    diff_sum = sum(abs(v) for px in pixels for v in px)
    diff_ratio = diff_sum / (total * 255)

    return {
        "passed": diff_ratio <= threshold,
        "diff_ratio": diff_ratio,
        "threshold": threshold,
        "diff_path": diff_path,
    }


def visual_assert(driver, name: str, threshold: float = 0.05) -> dict:
    """Take screenshot, compare against baseline. Creates baseline if missing."""
    baseline_path = os.path.join(BASELINE_DIR, f"{name}.png")
    current_path  = os.path.join(CURRENT_DIR,  f"{name}.png")
    diff_path     = os.path.join(DIFF_DIR,      f"{name}_diff.png")

    if not os.path.exists(baseline_path):
        save_baseline(driver, name)
        return {"passed": True, "diff_ratio": 0.0, "baseline_created": True}

    save_current(driver, name)
    return compare_images(baseline_path, current_path, diff_path, threshold)
