#!/usr/bin/env python3
"""Test script to check if icons are in the rendered HTML."""
import sys
sys.path.insert(0, '.')

from judinfo_web import app

# Create test client
client = app.test_client()

# Fetch the homepage
response = client.get('/')
html = response.get_data(as_text=True)

# Check for icon classes
checks = {
    'FA7 CDN link': 'font-awesome/7.0.1/css/all.min.css' in html,
    'fa-solid fa-lightbulb': 'fa-solid fa-lightbulb' in html,
    'fa-solid fa-magnifying-glass': 'fa-solid fa-magnifying-glass' in html,
    'fa-solid fa-circle-check': 'fa-solid fa-circle-check' in html,
    'fa-brands fa-github': 'fa-brands fa-github' in html,
    'fa-solid fa-spinner fa-spin-pulse': 'fa-solid fa-spinner fa-spin-pulse' in html,
    'fa-solid fa-circle-xmark': 'fa-solid fa-circle-xmark' in html,
    'fa-solid fa-circle-info': 'fa-solid fa-circle-info' in html,
}

print("=" * 60)
print("ICON VERIFICATION RESULTS")
print("=" * 60)
for check_name, result in checks.items():
    status = "✓ FOUND" if result else "✗ MISSING"
    print(f"{check_name:40} {status}")

print("=" * 60)
all_passed = all(checks.values())
if all_passed:
    print("✓ All icons are present in the HTML!")
else:
    print("✗ Some icons are missing. Details above.")
    # Print first 3000 chars for debugging
    print("\nFirst 3000 characters of HTML:")
    print(html[:3000])

sys.exit(0 if all_passed else 1)
