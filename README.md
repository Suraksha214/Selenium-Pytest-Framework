# Selenium + Pytest Automation Framework

## Tech Stack
- Python
- Selenium WebDriver
- Pytest
- Page Object Model (POM)
- HTML Reports

## Features
- Login automation tests
- Search functionality tests
- Regression suite
- Screenshot capture on failure
- Reusable utilities
- Config-driven framework

## Project Structure
pages/
tests/
utilities/
reports/
screenshots/

## Run Tests
pytest tests/regression/regression.py -v

## Generate Reports
pytest --html=reports/report.html --self-contained-html
