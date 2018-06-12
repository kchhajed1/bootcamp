# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser1 = Browser('chrome', **executable_path, headless=False)


    nasa_mars_news = 'https://mars.nasa.gov/news/'
    browser1.visit(nasa_mars_news)

    #get the source code of the browser
    html1 = browser1.html


    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html1, 'html.parser')

    # Examine the results, then determine element that contains sought info
    #print(soup.prettify())

    # results are returned as an iterable list
    news_title = soup.find('h3')
    news_p =soup.find('div', class_="article_teaser_body")

    news_title = news_title.text
    news_p = news_p.text

    browser1.quit()


    # #### Visit the url for JPL's Featured Space Image here.
    # ###### Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called 
    # ###### Make sure to find the image url to the full size .jpg image.
    # ###### Make sure to save a complete url string for this image

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser2 = Browser('chrome', **executable_path, headless=False)

    jpl_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser2.visit(jpl_image_url)

    html2 = browser2.html

    soup=BeautifulSoup(html2,"html.parser")

    browser2.click_link_by_id(id="full_image")

    html2 = browser2.html
    soup=BeautifulSoup(html2,"html.parser")

    image_path = str(soup.find("article", class_="carousel_item"))

    start = "('"
    end = "')"
    image_location = (image_path[image_path.find(start)+len(start):image_path.rfind(end)])
    featured_image_url = f"https://www.jpl.nasa.gov{image_location}"
    #print(featured_image_url)

    browser2.quit()

    # #### Mars Weather
    # 
    # 
    # Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.
    # 

    mars_weather_url = "https://twitter.com/marswxreport?lang=en"

    response = requests.get(mars_weather_url)

    soup3 = BeautifulSoup(response.text, "html.parser")


    mars_weather  = soup3.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    #print(mars_weather ) 


    # #### Mars Facts
    # 
    # 
    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string.

    # In[121]:


    mars_fact_url="https://space-facts.com/mars/"

    tables=pd.read_html(mars_fact_url)
    tables

    df=tables[0]
    df.columns=["description","value"]
    df.set_index("description",inplace=True)
    df


    html_table = df.to_html()
    html_table = html_table.replace("\n"," ")
    html_table


    # Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    # You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # Save both the image url string for the full resolution hemipshere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
    # Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    response = requests.get('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    soup4 = BeautifulSoup(response.text, "html.parser")


    hemisphere = soup4.find_all('div', class_='item')


    hemisphere_url_list = []

    for links in hemisphere:
        url = links.find('a')['href']
        hemisphere_url_list.append(f"https://astrogeology.usgs.gov/{url}")

    hemisphere_url_list


    hemisphere_dict =   {}
    hemisphere_image_urls = []

    for url in hemisphere_url_list:

            response = requests.get(url)
            soup5 = BeautifulSoup(response.text, "html.parser")
            title = soup5.find("h2", class_="title")

            image_path = str(soup5.find("img",class_="wide-image"))
            start = 'src="'
            end = '"/>'
            image_location = (image_path[image_path.find(start)+len(start):image_path.rfind(end)])

            hemisphere_dict["title"] = title.text
            hemisphere_dict["url"] = f"https://astrogeology.usgs.gov{image_location}"

            hemisphere_image_urls.append(hemisphere_dict)


    # In[129]:

    mars_db = {}
    mars_db["news_title"] = news_title
    mars_db["news_text"] = news_p
    mars_db["featured_image"] = featured_image_url
    mars_db["mars_weather"] = mars_weather
    mars_db["mars_facts"] = html_table
    mars_db["mars_images"] = hemisphere_image_urls
    return mars_db


from splinter import Browser
def init_browser():
    executable_path = {"executable_path", "/user/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless = False)
