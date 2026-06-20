from PIL import Image
import os
from datetime import datetime


class VisualComparator:
    def __init__(self, baseline_dir="baselines", diff_dir="diffs", threshold=0.01):
        self.baseline_dir = baseline_dir
        self.diff_dir = diff_dir
        self.threshold = threshold
        os.makedirs(baseline_dir, exist_ok=True)
        os.makedirs(diff_dir, exist_ok=True)

    def compare(self, current_path, baseline_name):
        baseline_path = os.path.join(self.baseline_dir, f"{baseline_name}.png")

        if not os.path.exists(baseline_path):
            return {
                "match": False,
                "reason": "baseline_not_found",
                "baseline_path": baseline_path,
                "current_path": current_path,
            }

        baseline = Image.open(baseline_path).convert("RGB")
        current = Image.open(current_path).convert("RGB")

        if baseline.size != current.size:
            current = current.resize(baseline.size)

        diff_image, mismatched_pixels, total_pixels = self._calculate_diff(baseline, current)
        mismatch_ratio = mismatched_pixels / total_pixels if total_pixels > 0 else 0

        diff_path = None
        if mismatched_pixels > 0:
            diff_path = os.path.join(self.diff_dir, f"diff_{baseline_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            diff_image.save(diff_path)

        return {
            "match": mismatch_ratio <= self.threshold,
            "mismatch_ratio": round(mismatch_ratio, 6),
            "mismatched_pixels": mismatched_pixels,
            "total_pixels": total_pixels,
            "threshold": self.threshold,
            "baseline_path": baseline_path,
            "current_path": current_path,
            "diff_path": diff_path,
        }

    def _calculate_diff(self, baseline, current):
        baseline_pixels = list(baseline.getdata())
        current_pixels = list(current.getdata())

        diff_image = Image.new("RGB", baseline.size)
        diff_pixels = []

        mismatched = 0
        total = len(baseline_pixels)

        for i, (b, c) in enumerate(zip(baseline_pixels, current_pixels)):
            if b != c:
                mismatched += 1
                diff_pixels.append((255, 0, 0))
            else:
                diff_pixels.append(b)

        diff_image.putdata(diff_pixels)
        return diff_image, mismatched, total

    def save_baseline(self, current_path, baseline_name):
        baseline_path = os.path.join(self.baseline_dir, f"{baseline_name}.png")
        img = Image.open(current_path)
        img.save(baseline_path)
        return baseline_path

    def get_all_baselines(self):
        if not os.path.exists(self.baseline_dir):
            return []
        return [f for f in os.listdir(self.baseline_dir) if f.endswith(".png")]

    def delete_baseline(self, baseline_name):
        path = os.path.join(self.baseline_dir, f"{baseline_name}.png")
        if os.path.exists(path):
            os.remove(path)
            return True
        return False
