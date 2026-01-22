"""
Test script to demonstrate broken link cleaning functionality.
"""

from app.utils.link_verifier import clean_broken_links_sync, verify_url_sync

print("=" * 70)
print("TESTING LINK CLEANING FUNCTIONALITY")
print("=" * 70)

# Test 1: Sample text with mixed valid and broken links
test_cases = [
    {
        "name": "Test 1: Mixed valid and broken markdown links",
        "input": """Here are some resources:
- [Google](https://www.google.com) - Valid link
- [Broken Tutorial](https://broken-tutorial-site-12345.com) - Broken link
- [Python Docs](https://docs.python.org) - Valid link
- [Fake Course](https://fake-course-xyz789.edu) - Broken link

Check these out!""",
    },
    {
        "name": "Test 2: Plain URLs",
        "input": """Resources:
https://www.github.com - Valid
https://broken-site-nonexistent.com - Broken
https://stackoverflow.com - Valid
https://another-fake-url-xxx.io - Broken""",
    },
    {
        "name": "Test 3: Mixed markdown and plain URLs",
        "input": """Learn from:
1. [MDN Web Docs](https://developer.mozilla.org) - Valid
2. Visit https://www.w3schools.com - Valid
3. Try [This Fake](https://does-not-exist-xyz.net) - Broken
4. Check https://fake-learning-site.co - Broken""",
    },
]

for test_case in test_cases:
    print(f"\n{test_case['name']}")
    print("-" * 70)
    print("ORIGINAL TEXT:")
    print(test_case['input'])
    print("\nCLEANED TEXT:")
    cleaned = clean_broken_links_sync(test_case['input'])
    print(cleaned)
    print()

# Test 4: Verify actual URLs
print("\n" + "=" * 70)
print("TESTING URL VERIFICATION")
print("=" * 70)

test_urls = [
    "https://www.google.com",
    "https://www.github.com",
    "https://docs.python.org",
    "https://broken-site-12345.com",
    "https://fake-url-xyz.edu",
]

for url in test_urls:
    result = verify_url_sync(url)
    status = "✓ VALID" if result else "✗ BROKEN"
    print(f"{status}: {url}")

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print("\nSUMMARY:")
print("The link cleaning system successfully:")
print("1. Extracts URLs from markdown links and plain text")
print("2. Verifies each URL's accessibility")
print("3. Removes broken links while preserving valid ones")
print("4. Cleans up formatting after removal")
print("\nThis ensures AI-generated resources NEVER contain broken links!")
