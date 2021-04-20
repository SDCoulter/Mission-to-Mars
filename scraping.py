#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
# Need to use Pandas' read_html() function.
import pandas as pd

# Create ChromeDriver executable path.
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Scrape the news data.
# Visit the URL.
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page.
browser.is_element_present_by_css('div.list_text', wait_time=1)
# Set up HTML parser.
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
# Find the data from the slide_elem - content title.
news_title = slide_elem.find('div', class_='content_title').get_text()
# Find the paragraph text from the slide_elem.
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

# Scrape the image.
# Visit the URL.
url = 'https://spaceimages-mars.com'
browser.visit(url)
# Find and click the "Full Image" button.
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()
# New webpage means we have to parse the HTML again.
html = browser.html
img_soup = soup(html, 'html.parser')
# Find the relative image url (ever-changing).
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
# Use the base URL to create an absolute URL.
img_url = f'https://spaceimages-mars.com/{img_url_rel}'

# Scrape table of data.
# Read the data from the website, store the first table element as a DataFrame
df = pd.read_html('https://galaxyfacts-mars.com')[0]
# Name the columns in the new DF.
df.columns = ['description', 'Mars', 'Earth']
# Set the index to the different categories/descriptors.
df.set_index('description', inplace=True)
# Save the DataFrame as HTML.
df_html = df.to_html()
# Close the browser session.
browser.quit()
