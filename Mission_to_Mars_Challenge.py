#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
# Need to use Pandas' read_html() function.
import pandas as pd


# In[2]:


# Create ChromeDriver executable path.
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Scrape the news data.

# In[3]:


# Visit the URL.
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page.
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Set up HTML parser.
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


# Find the data from the slide_elem - content title.
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[6]:


# Find the paragraph text from the slide_elem.
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Scrape the image.

# In[7]:


# Visit the URL.
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[8]:


# Find and click the "Full Image" button.
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[9]:


# New webpage means we have to parse the HTML again.
html = browser.html
img_soup = soup(html, 'html.parser')


# In[10]:


# Find the relative image url (ever-changing).
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[11]:


# Use the base URL to create an absolute URL.
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Scrape table of data.

# In[12]:


# Read the data from the website, store the first table element as a DataFrame
df = pd.read_html('https://galaxyfacts-mars.com')[0]
# Name the columns in the new DF.
df.columns = ['description', 'Mars', 'Earth']
# Set the index to the different categories/descriptors.
df.set_index('description', inplace=True)
df


# In[13]:


# View the DataFrame as HTML.
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# In[14]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(url)


# In[15]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Parse the html.
html = browser.html
page_soup = soup(html, 'html.parser')

# Find all the 
image_divs = page_soup.find_all('div', class_='description')
for image in image_divs:
    #Create empty dictionary to store title and URL.
    hemisphere_dict = {}
    
    # Get the title of the image.
    title = image.find('h3').text
    
    # Create the URL to access the page with the HD image, and visit it.
    create_url = f"https://astrogeology.usgs.gov{image.find('a').get('href')}"
    browser.visit(create_url)
    
    # Parse the image webpage.
    image_page_soup = soup(browser.html, 'html.parser')
    
    # Get the url of the image, combine into a full URL.
    full_res_url = image_page_soup.find('div', class_='downloads').find('a').get('href')

    # Populate the dictionary and add it to the main list.
    hemisphere_dict['img_url'] = full_res_url
    hemisphere_dict['title'] = title
    hemisphere_image_urls.append(hemisphere_dict)


# In[16]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[17]:


# 5. Quit the browser
browser.quit()

