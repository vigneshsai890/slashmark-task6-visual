# Task 6 — Visual Automation Testing

Visual regression testing suite using Python + Selenium + pytest + Pillow. Captures baseline screenshots, compares against new captures, and generates pixel-level diff images.

## What's Tested

- **Screenshot Capture** — Full page, element-level, viewport screenshots
- **Visual Regression** — Baseline vs current comparison, pixel diff, threshold pass/fail
- **Diff Image Generation** — Highlighted visual differences between screenshots
- **Layout Validation** — Element positioning, visibility, responsive breakpoints
- **Cross-page Visual Checks** — Consistent UI across multiple pages

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create directories for visual testing
mkdir -p baselines diffs
```

## Run Tests

```bash
# All tests
pytest

# By category
pytest -m visual
pytest -m screenshot
pytest -m regression

# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# Update baselines (after intentional UI changes)
pytest --update-baselines
```

## Project Structure

```
├── conftest.py
├── tests/
├── pages/
├── utils/
│   └── visual_comparator.py    # Screenshot comparison logic
├── baselines/                  # Baseline screenshots (git-tracked)
├── diffs/                      # Generated diff images
└── screenshots/                # Current captures
```

## Tech Stack

- Python 3 + Selenium 4 + pytest
- Pillow (PIL) for image comparison
- Page Object Model design pattern
- WebDriver Manager for automatic browser driver management

## Intern

**M Vignesh Sai** — Slash Mark Internship (June 2026)
