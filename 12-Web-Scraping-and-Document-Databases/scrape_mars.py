from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def init_browser():
    executable_path = {'executable_path': "/usr/local/bin/chromedrive"}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_dictionary = {}

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    NewsTitle = soup.find("ul", class_="item_list").find(
        "li", class_="slide").find("div", class_="content_title").text
    NewsP = soup.find("ul", class_="item_list").find(
        "li", class_="slide").find("div", class_="article_teaser_body").text

    mars_dictionary["title"] = NewsTitle
    mars_dictionary["Paragraph"] = NewsP

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    browser.find_by_id("full_image").click()
    browser.links.find_by_partial_href("/spaceimages/details").click()

    html = browser.html
    soup = bs(html, "html.parser")
    image_url = soup.find("img", class_="main_image")["src"]
    main_url = "https://www.jpl.nasa.gov"
    featured_image_url = main_url + image_url

    mars_dictionary["image_url"] = featured_image_url

    url = "https://space-facts.com/mars/"
    browser.visit(url)
    tables = pd.read_html(url)
    MarsFacts = tables[0]
    MarsFacts.columns = ["Description", "Answer"]

    mars_dictionary["table"] = MarsFacts

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    items = soup.find_all("div", class_="item")
    hemisphere_img = []
    hemisphere_url = "https://astrogeology.usgs.gov/"
    items = soup.find_all("div", class_="item")
    for item in items:
        title = item.find("h3").text
        image_url = item.find("a")["href"]
        browser.visit(hemisphere_url + image_url)
        image_html = browser.html
        soup = bs(image_html, 'html.parser')
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_img.append({
        "Title": title,
        "Image_url": image_url
    })

    mars_dictionary["image_url"] = image_url
    mars_dictionary["Title"] = title





    return mars_dictionary