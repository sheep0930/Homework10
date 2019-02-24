
# coding: utf-8

# In[1]:


from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time

def scrape():

    all_dict = {}
    # In[2]:


    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'


    # In[3]:


    response = requests.get(url)


    # In[4]:


    soup = bs(response.text, 'html.parser')


    # In[5]:


    print(soup.prettify())


    # In[6]:


    results = soup.find_all('div', class_="slide")
    print(len(results))


    # In[7]:


    print(results[0].prettify())


    # In[8]:


    news_title = results[0].find('div', class_="content_title").text.strip()


    # In[9]:


    news_title


    # In[10]:


    news_p = results[0].find('div', class_="rollover_description_inner").text.strip()


    # In[11]:


    news_p

    all_dict['news_title'] = news_title
    all_dict['news_p'] = news_p

    # In[12]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[13]:


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)


    # In[14]:


    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)


    # In[15]:


    html = browser.html
    soup = bs(html, 'html.parser')
    imgurl = soup.find('img', class_='fancybox-image')['src']


    # In[16]:


    imgurl


    # In[17]:


    featured_image_url = 'https://www.jpl.nasa.gov' + imgurl
    featured_image_url
    browser.quit()

    all_dict['featured_mars_image'] = featured_image_url


    # In[18]:


    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    print(soup.prettify())


    # In[19]:


    results = soup.find_all('div', class_="js-tweet-text-container")
    print(len(results))


    # In[20]:


    for result in results:
        trash = result.find("a", class_="twitter-timeline-link")
        _ = trash.extract()
        mars_weathers = result.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text", lang="en").text
        
        if ('InSight' in mars_weathers):
            print(mars_weathers)
                
            break


    # In[21]:


    mars_weathers
    all_dict['mars_weathers'] = mars_weathers

    # In[22]:


    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    tables[0]


    # In[23]:


    df = tables[0]
    df.columns = ['Parameter', 'Value']
    df


    # In[24]:


    html_table = df.to_html(index = False)
    html_table


    # In[25]:


    html_table.replace('\n', '')
    all_dict['mars_facts'] = html_table

    # In[26]:


    # In[27]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[28]:


    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)


    # In[29]:


    html = browser.html
    soup = bs(html, 'html.parser')


    # In[30]:


    categories = soup.find_all('h3')
    categories


    # In[31]:


    category_list = []
    url_list = []
    hemisphere_image_urls = []
    this_dict = {
        'title': '',
        'img_url': ''
    }
    for category in categories:
        title = category.text.strip()
        category_list.append(title)
        browser.click_link_by_partial_text(title)
        time.sleep(5)
        soup = bs(browser.html, 'html.parser')
        img_url = soup.find('a', target="_blank")['href']
        url_list.append(img_url)
        this_dict['title'] = title
        this_dict['img_url'] = img_url
        hemisphere_image_urls.append(this_dict)
        browser.back()
    browser.quit()


    # In[32]:


    titles_and_urls = zip(category_list, url_list)


    # In[33]:


    print (hemisphere_image_urls)

    all_dict['mars_hemispheres'] = hemisphere_image_urls

    print (all_dict)

    return all_dict
