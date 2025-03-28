# Screenshot Functionality

AUTOCLICK provides comprehensive screenshot capabilities for capturing browser content during automation. This document explains how to use the screenshot functionality.

## Taking Screenshots

### From the Command Line

AUTOCLICK provides CLI commands for taking screenshots:

#### Page Screenshots

To take a screenshot of an entire page:

```bash
autoclick screenshot page https://example.com --name example_page
```

Options:

- `--name`: Name for the screenshot (without extension)
- `--output-dir`: Directory to save the screenshot
- `--browser`: Browser to use (default: chrome)
- `--headless`: Run in headless mode
- `--timeout`: Timeout in seconds (default: 30)
- `--wait`: Wait time in seconds before taking the screenshot

#### Element Screenshots

To take a screenshot of a specific element:

```bash
autoclick screenshot element https://example.com "#main-content" --name example_element
```

Options:

- `--name`: Name for the screenshot (without extension)
- `--output-dir`: Directory to save the screenshot
- `--browser`: Browser to use (default: chrome)
- `--headless`: Run in headless mode
- `--timeout`: Timeout in seconds (default: 30)
- `--wait`: Wait time in seconds before taking the screenshot

### From Automation Scripts

You can take screenshots directly from your automation scripts:

```python
def run(driver):
    # Navigate to a page
    driver.get("https://example.com")

    # Take a screenshot of the entire page
    screenshot_path = take_screenshot(driver, "example_page.png")

    # Find an element
    element = driver.find_element_by_css_selector("#main-content")

    # Take a screenshot of the element
    element_screenshot_path = take_element_screenshot(driver, element, "example_element.png")

    return {
        "status": "success",
        "screenshots": [
            str(screenshot_path),
            str(element_screenshot_path)
        ]
    }
```

### From the Automation Engine

The AutomationEngine class provides methods for taking screenshots:

```python
# Initialize the automation engine
engine = AutomationEngine()
engine.initialize(config)

# Initialize the driver
engine.driver = engine.driver_manager.initialize_driver()

# Navigate to a page
engine.driver.get("https://example.com")

# Take a screenshot of the entire page
screenshot_path = engine.take_screenshot("example_page")

# Find an element
element = engine.driver.find_element_by_css_selector("#main-content")

# Take a screenshot of the element
element_screenshot_path = engine.take_element_screenshot(element, "example_element")
```

## Screenshot Storage

Screenshots are stored in the configured screenshots directory:

- Default: `./screenshots`
- Configurable via `screenshots_dir` in the configuration

## Screenshot Naming

Screenshots can be named in several ways:

1. **Explicit Name**: Provide a name for the screenshot

   ```python
   engine.take_screenshot("example_page")
   ```

2. **Timestamp Naming**: Use timestamp-based naming
   ```python
   # Results in a filename like: screenshot_20230101_120000.png
   take_screenshot(driver, use_timestamp=True)
   ```

## Screenshot Metadata

Screenshot metadata is stored in JSON files alongside the screenshots:

```json
{
  "url": "https://example.com",
  "timestamp": "2023-01-01T12:00:00",
  "browser": "chrome",
  "title": "Example Domain",
  "window_size": { "width": 1920, "height": 1080 }
}
```

## Integration with Reporting

Screenshots can be included in reports:

```python
# Initialize the results handler
handler = ResultsHandler()
handler.initialize(config)

# Add a screenshot to a result
handler.add_screenshot(screenshot_path, result_index=0)
```

The screenshot will be copied to the reports directory and included in the report.
