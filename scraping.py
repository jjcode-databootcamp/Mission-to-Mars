# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
# from selenium import webdriver


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}


#Scrape All
def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a object 
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_data": hemisphere_scrape(browser)

    }
    # Stop webdriver and return data
    browser.quit()
    return data

#Mars News
def mars_news(browser):
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find(
            "div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_p

#NASA Image Scraping
def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()
    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None
    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url

#Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns = ['Description', 'Mars']
    df.set_index('Description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

#Mars Hemisphere Scraping
def hemisphere_scrape(browser):
    # 1. Use browser to visit the URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # Parse the html with beautifulsoup
    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    # Get the links for each of the 4 hemispheres
    hemi_links = hemi_soup.find_all('h3')
    # hemi_links

    # loop through each hemisphere link
    for hemi in hemi_links:
        # Navigate and click the link of the hemisphere
        img_page = browser.find_by_text(hemi.text)
        img_page.click()
        html = browser.html
        img_soup = soup(html, 'html.parser')
        # Scrape the image link
        img_url = 'https://astrogeology.usgs.gov/' + \
            str(img_soup.find('img', class_='wide-image')['src'])
        # Scrape the title
        title = img_soup.find('h2', class_='title').text
        # Define and append to the dictionary
        hemisphere = {'img_url': img_url, 'title': title}
        hemisphere_image_urls.append(hemisphere)
        browser.back()
        # print(hemisphere_image_urls)
    return hemisphere_image_urls


#Ending Code
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
