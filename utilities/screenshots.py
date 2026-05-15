import os
import time


FAILURE_SCREENSHOT_DIR = "utilities/screenshots/failures"
CLICK_SCREENSHOT_DIR   = "utilities/screenshots/clicks"

os.makedirs(FAILURE_SCREENSHOT_DIR, exist_ok=True)
os.makedirs(CLICK_SCREENSHOT_DIR, exist_ok=True)


def take_failure_screenshot(driver, test_name):
    """Called automatically on test failure."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(FAILURE_SCREENSHOT_DIR, f"FAIL_{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"\n❌ Failure screenshot saved: {path}")
    return path


def take_click_screenshot(driver, action_name):
    """Called manually after any click action."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(CLICK_SCREENSHOT_DIR, f"CLICK_{action_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"\n🖱️  Click screenshot saved: {path}")
    return path