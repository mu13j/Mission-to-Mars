import time
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # TODO: make sure to add your driver here     
    executable_path = {"executable_path": "C:/Users/J/AppData/Local/Programs/Python/Python36/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    #NASA Mars News
    results={}
    browser = init_browser()
    images_website = "https://mars.nasa.gov/news/"
    browser.visit(images_website)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results['news_title']=soup.find('div', class_="content_title").get_text()
    results['news_p']=soup.find('div', class_="article_teaser_body").get_text()
    #JPL Mars Space Images - Featured Image
    images_website = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(images_website)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    a=soup.find('article').get('style').split("'")[1]
    base_url="https://www.jpl.nasa.gov"
    results['featured_image_url']=base_url+a
    #Mars Weather
    images_website = "https://twitter.com/marswxreport?lang=en"
    browser.visit(images_website)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results['mars_weather']=soup.find('p',class_="TweetTextSize").get_text()
    #Mars Facts
    url = 'http://space-facts.com/mars/'
    tables = pd.read_html(url)
    a=tables[0]
    b={}
    for i in range(len(a[0])):
        b[a[0][i]]=a[1][i]
    results['facts']=b
    #Mars Hemispheres
    xpath = '//div[@class="item"]//a[@class="itemLink product-item"]/img'
    hemisphere_image_urls=[]
    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    for i in range(4):
        dictionary={}
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        dictionary['title']=soup.find_all('h3')[i].get_text()
        a = browser.find_by_xpath(xpath)
        img = a[i]
        img.click()
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        dictionary['img_url']=soup.find('a',text='Sample')['href']
        hemisphere_image_urls.append(dictionary)
    results['hemisphere_image_urls']=hemisphere_image_urls
    return results


