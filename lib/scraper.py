"""Web scraping utilities using Beautiful Soup."""
from bs4 import BeautifulSoup
import requests


class Scraper:
    """A web scraper class for extracting data from HTML documents using Beautiful Soup."""
    
    def __init__(self, url=None):
        """Initialize the Scraper with an optional URL.
        
        Args:
            url (str, optional): The URL to scrape. If provided, will load the HTML.
        """
        self.soup = None
        self.html_content = None
        
        if url:
            self.load_from_url(url)
    
    def load_from_url(self, url, headers=None):
        """Load HTML content from a URL.
        
        Args:
            url (str): The URL to fetch HTML from.
            headers (dict, optional): HTTP headers for the request.
        
        Returns:
            self: Returns the instance for method chaining.
        """
        if headers is None:
            headers = {'user-agent': 'my-app/0.0.1'}
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        self.html_content = response.text
        self.soup = BeautifulSoup(response.text, 'html.parser')
        return self
    
    def load_html(self, html_string):
        """Load HTML content from a string.
        
        Args:
            html_string (str): The HTML content as a string.
        
        Returns:
            self: Returns the instance for method chaining.
        """
        self.html_content = html_string
        self.soup = BeautifulSoup(html_string, 'html.parser')
        return self
    
    def select(self, selector):
        """Select elements using a CSS selector.
        
        Args:
            selector (str): CSS selector string (e.g., '.class', '#id', 'tag').
        
        Returns:
            list: List of matching BeautifulSoup Tag objects.
        """
        if self.soup is None:
            raise ValueError("No HTML content loaded. Use load_from_url() or load_html() first.")
        
        return self.soup.select(selector)
    
    def select_one(self, selector):
        """Select a single element using a CSS selector.
        
        Args:
            selector (str): CSS selector string.
        
        Returns:
            Tag or None: The first matching element or None if not found.
        """
        if self.soup is None:
            raise ValueError("No HTML content loaded. Use load_from_url() or load_html() first.")
        
        return self.soup.select_one(selector)
    
    def find_all(self, tag_name, **kwargs):
        """Find all elements with a given tag name.
        
        Args:
            tag_name (str): The HTML tag name (e.g., 'div', 'span', 'li').
            **kwargs: Additional attributes to filter by (e.g., class_='name', id='id').
        
        Returns:
            list: List of matching Tag objects.
        """
        if self.soup is None:
            raise ValueError("No HTML content loaded. Use load_from_url() or load_html() first.")
        
        return self.soup.find_all(tag_name, **kwargs)
    
    def find(self, tag_name, **kwargs):
        """Find the first element with a given tag name.
        
        Args:
            tag_name (str): The HTML tag name.
            **kwargs: Additional attributes to filter by.
        
        Returns:
            Tag or None: The first matching element or None.
        """
        if self.soup is None:
            raise ValueError("No HTML content loaded. Use load_from_url() or load_html() first.")
        
        return self.soup.find(tag_name, **kwargs)
    
    def get_text(self, selector):
        """Get text content from elements matching a CSS selector.
        
        Args:
            selector (str): CSS selector string.
        
        Returns:
            str: The combined text content of all matching elements, stripped of whitespace.
        """
        elements = self.select(selector)
        texts = [el.get_text(strip=True) for el in elements]
        return ' '.join(texts)
    
    def get_text_from_element(self, element):
        """Get text content from a single BeautifulSoup element.
        
        Args:
            element: A BeautifulSoup Tag object.
        
        Returns:
            str: The text content, stripped of whitespace.
        """
        if element is None:
            return ""
        return element.get_text(strip=True)
    
    def get_attribute(self, selector, attribute):
        """Get an attribute value from elements matching a CSS selector.
        
        Args:
            selector (str): CSS selector string.
            attribute (str): The attribute name to retrieve.
        
        Returns:
            str or None: The attribute value or None if not found.
        """
        element = self.select_one(selector)
        if element:
            return element.get(attribute)
        return None
    
    def get_all_attributes(self, selector):
        """Get a list of attribute values from all matching elements.
        
        Args:
            selector (str): CSS selector string.
            attribute (str): The attribute name to retrieve.
        
        Returns:
            list: List of attribute values.
        """
        elements = self.select(selector)
        return [el.get(attribute) for el in elements if el]
    
    @property
    def title(self):
        """Get the page title.
        
        Returns:
            str: The text content of the <title> tag.
        """
        title_tag = self.soup.find('title') if self.soup else None
        return title_tag.get_text(strip=True) if title_tag else ""
    
    def __repr__(self):
        """Return a string representation of the Scraper."""
        return f"Scraper(html_loaded={self.html_content is not None})"


# Example usage functions based on README
def scrape_flatiron_courses():
    """Example function to scrape course information from Flatiron School website."""
    headers = {'user-agent': 'my-app/0.0.1'}
    html = requests.get("https://flatironschool.com/our-courses/", headers=headers)
    doc = BeautifulSoup(html.text, 'html.parser')
    
    courses = doc.select('.heading-60-black.color-black.mb-20')
    course_list = []
    
    for course in courses:
        course_text = course.contents[0].strip()
        course_list.append(course_text)
    
    return course_list


def scrape_heading_text():
    """Example function to scrape heading text from a page."""
    headers = {'user-agent': 'my-app/0.0.1'}
    html = requests.get("https://flatironschool.com/", headers=headers)
    doc = BeautifulSoup(html.text, 'html.parser')
    
    heading = doc.select('.heading-financier')
    if heading and heading[0].contents:
        return heading[0].contents[0].strip()
    return ""

