#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
# Need to use Pandas' read_html() function.
import pandas as pd
# For saving last modified date.
import datetime as dt


# Main function to initialize the browser.
def scrape_all():
    # Create ChromeDriver executable path.
    executable_path = {'executable_path': ChromeDriverManager().install()}
    # Set to true as we don't want to see the browser opening and scraping.
    browser = Browser('chrome', **executable_path, headless=True)
    # Set news title and paragraph variables.
    news_title, news_paragraph = mars_news(browser)
    # Run all the scraping functions and create a dictionary of results.
    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now(),
        'hemispheres': mars_hemispheres(browser)
    }
    # Close the browser session and return the dict.
    browser.quit()
    return data


# Make a function to scrape the news data.
def mars_news(browser):
    # Visit the URL.
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page.
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    # Set up HTML parser.
    html = browser.html
    news_soup = soup(html, 'html.parser')
    # Add TRY-EXCEPT to handle website updates.
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Find the data from the slide_elem - content title.
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Find the paragraph text from the slide_elem.
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    return news_title, news_p


# Function to scrape the image.
def featured_image(browser):
    # Visit the URL.
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    # Find and click the "Full Image" button.
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    # New webpage means we have to parse the HTML again.
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # Handle web errors.
    try:
        # Find the relative image url (ever-changing).
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    # Use the base URL to create an absolute URL.
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url


# Function to scrape table of data.
def mars_facts():
    # Handle errors.
    try:
        # Read the data from the website, store the first table element as a DataFrame.
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    # Name the columns in the new DF.
    df.columns = ['description', 'Mars', 'Earth']
    # Set the index to the different categories/descriptors.
    df.set_index('description', inplace=True)

    # Remove the index name - for formatting purposes.
    df.index.name = None

    # Save the DataFrame as HTML. (Pass Bootstrap class to html tags.)
    df_html = df.to_html(classes="table table-striped")
    return df_html


# Function to scrape hemisphere data (Titles and Images).
def mars_hemispheres(browser):
    # Visit the hemispheres URL - use browser argument to access.
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Write code to retrieve the image urls and titles for each hemisphere.
    # Parse the html.
    html = browser.html
    page_soup = soup(html, 'html.parser')

    # Find all the divs with a class of 'description'.
    image_divs = page_soup.find_all('div', class_='description')
    # Loop through all the divs.
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

    # Return the dictionary.
    return hemisphere_image_urls


if __name__ == '__main__':
    # If running script, print scraped data.
    print(scrape_all())
