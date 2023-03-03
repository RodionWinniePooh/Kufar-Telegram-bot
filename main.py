import requests
import time
from bs4 import BeautifulSoup
import telebot
import datetime


url = 'https://www.kufar.by/l?cmp=0&ot=1&query=iphone&sort=lst.d'

urlNotDataSrc = 'https://yt3.googleusercontent.com/ytc/AL5GRJX7GhDQOABF8ZczSFvJv5O1y2kyB3T6VK7dYEijwQ=s900-c-k-c0x00ffffff-no-rj'

bot_token = '5990940764:AAE6sH2BmGeUGoFIzj8msPrq_NKIe5yrlu8'
bot = telebot.TeleBot(bot_token)

chat_id = '471142564'
group_id = '-816703142'

# The list to store the links of the ads
links_list = []

# Get the current date and time
now = datetime.datetime.now()

while True:
    # Make a request to the website and get the HTML content

    response = requests.get(url)
    html_content = response.content

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the <section> tags inside the <div data-name="listings"> tag
    listings_div = soup.find('div', {'data-name': 'listings'})
    sections = listings_div.find_all('section')

    # Iterate through the <section> tags and extract the link to the ad
    for section in sections[:20]:  # Only check the first 20 <section> tags
        ad_title = section.find("h3").text
        ad_price = section.find("p").text
        ad_location = section.find_all('p')[1].text
        ad_images = section.find('img', alt=ad_title)

        # print(ad_location)

        try:
            if section.find('img', {'data-src': False}):
                img_url = urlNotDataSrc
            ad_images = section.find('img', {'data-src': True})
            img_url = ad_images['data-src']
            print(img_url)

        except TypeError:
            print('No img tag with data-src attribute found.')

        ad_link = section.find('a')['href']
        ad_link = ad_link.split('?')[0]
        # ad_details = [section.get_text().strip(), ad_link]  # Store the ad details in a list
        print(ad_link)

        if ad_link not in links_list:
            links_list.append(ad_link)
            bot.send_photo(group_id,
                           img_url,
                           f"Объявление: {ad_title} \n"
                           f"Цена: {ad_price} \n" 
                           f"Ссылка: {ad_link} \n" 
                           f"Дата: {now.strftime('%Y-%m-%d')} \n"
                           f"Локация: {ad_location}"
                           )





    # Wait for 10 seconds before checking again
    time.sleep(10)
# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
# 	bot.reply_to(message, "Howdy, how are you doing?")
