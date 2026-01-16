"""Test module for web scraper functionality."""
from bs4 import BeautifulSoup
import requests
import pytest


# Sample HTML for testing (simulating a web page structure)
SAMPLE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1 class="heading-financier">Welcome to Test Page</h1>
    <div class="course-list">
        <h2 class="heading-60-black color-black mb-20">Software Engineering</h2>
        <h2 class="heading-60-black color-black mb-20">Data Science</h2>
        <h2 class="heading-60-black color-black mb-20">Product Design</h2>
    </div>
    <ul id="items">
        <li>Item 1</li>
        <li>Item 2</li>
        <li>Item 3</li>
    </ul>
</body>
</html>
"""

headers = {'user-agent': 'my-app/0.0.1'}


def test_codegrade_placeholder():
    """Codegrade placeholder test"""
    assert 1 == 1


def test_scraper_import():
    """Test that scraper module can be imported"""
    try:
        from lib.scraper import Scraper
        assert True
    except ImportError:
        assert False, "Failed to import Scraper class from lib.scraper"


def test_scraper_initialization():
    """Test Scraper class initialization"""
    from lib.scraper import Scraper
    scraper = Scraper()
    assert scraper is not None


def test_scraper_select_single_element():
    """Test selecting a single element from HTML"""
    from lib.scraper import Scraper
    scraper = Scraper()
    scraper.load_html(SAMPLE_HTML)
    result = scraper.select('.heading-financier')
    assert len(result) == 1
    assert 'Welcome to Test Page' in result[0]


def test_scraper_select_multiple_elements():
    """Test selecting multiple elements from HTML"""
    from lib.scraper import Scraper
    scraper = Scraper()
    scraper.load_html(SAMPLE_HTML)
    result = scraper.select('.heading-60-black.color-black.mb-20')
    assert len(result) == 3


def test_scraper_get_text():
    """Test extracting text from selected elements"""
    from lib.scraper import Scraper
    scraper = Scraper()
    scraper.load_html(SAMPLE_HTML)
    text = scraper.get_text('.heading-financier')
    assert 'Welcome to Test Page' in text


def test_scraper_iterate_elements():
    """Test iterating over multiple elements"""
    from lib.scraper import Scraper
    scraper = Scraper()
    scraper.load_html(SAMPLE_HTML)
    courses = scraper.select('.heading-60-black.color-black.mb-20')
    course_names = [scraper.get_text_from_element(course) for course in courses]
    assert 'Software Engineering' in course_names
    assert 'Data Science' in course_names
    assert 'Product Design' in course_names


def test_scraper_get_attribute():
    """Test getting attributes from elements"""
    from lib.scraper import Scraper
    scraper = Scraper()
    scraper.load_html(SAMPLE_HTML)
    items = scraper.select('#items')
    assert len(items) == 1
    assert items[0].get('id') == 'items'


def test_scraper_find_all():
    """Test finding all elements with a tag"""
    from lib.scraper import Scraper
    scraper = Scraper()
    scraper.load_html(SAMPLE_HTML)
    all_li = scraper.find_all('li')
    assert len(all_li) == 3

