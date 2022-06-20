# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
# from selenium import webdriver


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#----------Visit the NASA Mars News Site----------------

# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


#----------JPL Space Images Featured Image---------------
# Visit URL - The splinter package allows you to open a tab control the browser with functions
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


#-----------------Mars Facts---------------
#Grabs the table it found on the page and puts it into dataframe
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head(10)


df.columns = ['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()


#-------------D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles-------
# 1. Use browser to visit the URL
url = 'https://marshemispheres.com/'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

#create a foreloop to loop the page for matching elements
for i in range(4):
    #create a object to hold the scrap info
    hemispheres_obj = {}

    #identify the nested tag info
    browser.find_by_css('a.product-item h3')[i].click()
    element = browser.links.find_by_text('Sample').first
    img_url = element['href']
    title = browser.find_by_css("h2.title").text

    #add the image url, title info as 1 entry of the object
    hemispheres_obj["img_url"] = img_url
    hemispheres_obj["title"] = title

    #push the object into the inital array
    hemisphere_image_urls.append(hemispheres_obj)
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()
