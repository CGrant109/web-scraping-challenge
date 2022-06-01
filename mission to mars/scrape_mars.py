# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import pandas as pd
import numpy as np
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo


##Part 1: Scraping

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html=browser.html
    soup=bs(html,'html.parser')

    # Retrieve the latest news title
    news_title=soup.find_all('div', class_='content_title')[0].text

    # Retrieve the latest news paragraph
    news_paragraph=soup.find('div', class_='article_teaser_body').text

    print(news_title)
    print('--------------------------------------------------------------------')
    print(news_paragraph)

    

    ### JPL Mars Space Images - Featured Image

    jpl_url="https://spaceimages-mars.com"
    browser.visit(jpl_url)

    # HTML object
    html=browser.html

    # Parse HTML
    soup=bs(html,"html.parser")

    # Retrieve image url
    image_path = soup.find_all('img')[1]["src"]
    featured_image_url = jpl_url + image_path
    featured_image_url
    

    ### Mars Fact

    # Scrape Mars facts from https://galaxyfacts-mars.com
    url_facts='https://galaxyfacts-mars.com'
    browser.visit(url_facts)
    html = browser.html

    #Visit the Mars Facts url and scrape the table holding facts using Pandas
    table = pd.read_html(url)
    mars_planet_profile = table[1]
    # mars_planet_profile

     # Rename Columns
    mars_planet_profile.columns = ['', 'Values']
    mars_planet_profile.set_index('', inplace = True)
    mars_planet_profile

     # Use Pandas to convert the data to a HTML table string.
    mars_planet_profile.to_html('table.html')

    
    
    ### Mars Hemispheres

    # Scrape Mars hemisphere title and image
    hems_url='https://marshemispheres.com/'
    browser.visit(hems_url)
    html=browser.html
    soup=bs(html,'html.parser')

    #Save the image URL string for the full resolution hemisphere image and the hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
    hemisphere_image_urls=[]
    products = soup.find ('div', class_='result-list')
    hemispheres = products.find_all('div',{'class':'item'})

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://marshemispheres.com/" + end_link    
        browser.visit(image_link)
        html_hemispheres = browser.html
        soup=bs(html_hemispheres, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})
            
    hemisphere_image_urls

    browser.quit()

    return hemisphere_image_urls