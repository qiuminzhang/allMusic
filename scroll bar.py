#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/12/2018 4:21 PM
# @Author  : Qiumin Zhang
# @Site    : 
# @File    : scroll bar.py
# @Software: PyCharm

from selenium import webdriver
import pprint
import time
import json
import pymongo

# Genre xpath seed
# Next time use ''' xxx '''
genre_xpath = {
    "Avant-Garde": "//*[@id=\"genreid:MA0000012170\"]",
    "Blues": "//*[@id=\"genreid:MA0000002467\"]",
    "Children's": "//*[@id=\"genreid:MA0000002944\"]",
    "Classical": "//*[@id=\"genreid:MA0000002521\"]",
    "Comedy_Spoken": "//*[@id=\"genreid:MA0000004433\"]",
    "County": "//*[@id=\"genreid:MA0000002532\"]",
    "Easy Listening": "//*[@id=\"genreid:MA0000002567\"]",
    "Electronic": "//*[@id=\"genreid:MA0000002572\"]",
    "Folk": "//*[@id=\"genreid:MA0000002592\"]",
    "Holiday": "//*[@id=\"genreid:MA0000012075\"]",
    "International": "//*[@id=\"genreid:MA0000002660\"]",
    "Jazz": "//*[@id=\"genreid:MA0000002674\"]",
    "Latin": "//*[@id=\"genreid:MA0000002692\"]",
    "New Age": "//*[@id=\"genreid:MA0000002745\"]",
    "Pop_Rock": "//*[@id=\"genreid:MA0000002613\"]",
    "R&B": "//*[@id=\"genreid:MA0000002809\"]",
    "Rap": "//*[@id=\"genreid:MA0000002816\"]",
    "Reggae": "//*[@id=\"genreid:MA0000002820\"]",
    "Religious": "//*[@id=\"genreid:MA0000004431\"]",
    "Stage & Screen": "//*[@id=\"genreid:MA0000004432\"]",
    "Vocal": "//*[@id=\"genreid:MA0000011877\"]"
}

# Initialize dictionary keys
keys = ["artist", "album", "album_url", "release_year", "image", "genre", "style"]

# Interval
LOAD_TIME = 3


def scroll_down(driver):
    """
    Scroll down web page to bottom in order to click NEXT >> and go to next page
    :param driver: Webdriver, Chrome version
    :return: None
    """
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(LOAD_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def scroll_up(driver):
    driver.execute_script("window.scrollTo(0, 0)")

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, 0)")

        # Wait to load page
        time.sleep(LOAD_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def spider(driver, genre, page_num, start):
    """
    Construct result data.
    ** One album could have several genres
    ** One album will have several styles, and I'll get them by album_url later
    ** Go to album link and get clear image
    ** The last two will be done in another crawler
    :param driver:
    :param genre: Current genre. Pass genre to result["genre"]
    :return:
    """
    for i in range(1, 41):
        # Initialize a dictionary for each result
        result = {key: None for key in keys}
        result["genre"] = [genre]
        piece_xpath = '''//*[@id="cmn_wrap"]/div[1]/div[2]/section[2]/div[1]/table/tbody/tr[{0}]'''.format(str(i))
        artist_xpath = piece_xpath + '''/td[3]/a'''
        album_xpath = piece_xpath + '''/td[4]/a[1]'''
        year_xpath = piece_xpath + '''/td[2]'''

        try:
            artist = driver.find_element_by_xpath(artist_xpath).text
            album = driver.find_element_by_xpath(album_xpath).text
            album_url = driver.find_element_by_xpath(album_xpath).get_attribute("href")
            year = driver.find_element_by_xpath(year_xpath).text
        except:
            break
        finally:
            end = time.time()
            interval = end - start

        result["artist"] = artist
        result["album"] = album
        result["album_url"] = album_url
        result["release_year"] = year

        pprint.pprint(result)
        with open(genre + '_' + str(page_num) + '.txt', 'a') as f:
            f.write(json.dumps(result))
            f.write('\n')


def mongodb(result):
    pass


start_all = time.time()

# The chromedriver.exe can be anywhere, system will find it automatically
driver = webdriver.Chrome('chromedriver')

driver.get('https://www.allmusic.com/advanced-search')

assert "Advanced Music Search" in driver.title

try:
    for key, value in genre_xpath.items():
        first_page = True
        start = time.time()

        ele = driver.find_element_by_xpath(value)
        driver.execute_script("arguments[0].scrollIntoView();", ele)
        scroll_up(driver)
        ele.click()

        while True:
            time.sleep(LOAD_TIME)
            # spider()

            scroll_down(driver)

            try:
                if first_page:
                    nextPage = driver.find_element_by_xpath('''//*[@id="cmn_wrap"]/div[1]/div[2]/section[2]/div[3]/div/span[2]/a''')
                    nextPage.click()
                    first_page = False

                    # delete
                    break
                else:
                    nextPage = driver.find_element_by_xpath('''//*[@id="cmn_wrap"]/div[1]/div[2]/section[2]/div[3]/div/span[3]/a''')
                    nextPage.click()
            except:
                break

        print("Genre:", key)

        # Uncheck the checkbox before go to next checkbox.
        # clear() is not available here, because clear() works on textfield.
        ele = driver.find_element_by_xpath(value)
        ele.click()

        # # Scroll down the filter to the target element to enable clicking operation.
        # # Don't ask me why the code below looks sooo stupid.
        # # I was wondering
        # if key == "Electronic":
        #     ele = driver.find_element_by_xpath("//*[@id=\"genreid:MA0000002944\"]")
        #     driver.execute_script("arguments[0].scrollIntoView();", ele)
        # if key == "International":
        #     ele = driver.find_element_by_xpath("//*[@id=\"genreid:MA0000004433\"]")
        #     driver.execute_script("arguments[0].scrollIntoView();", ele)
        # if key == "Latin":
        #     ele = driver.find_element_by_xpath("//*[@id=\"genreid:MA0000002572\"]")
        #     driver.execute_script("arguments[0].scrollIntoView();", ele)
        # if key == "Pop/Rock":
        #     ele = driver.find_element_by_xpath("//*[@id=\"genreid:MA0000004433\"]")
        #     driver.execute_script("arguments[0].scrollIntoView();", ele)
        # if key == "R&B":
        #     ele = driver.find_element_by_xpath("//*[@id=\"genreid:MA0000002745\"]")
        #     driver.execute_script("arguments[0].scrollIntoView();", ele)

except Exception as e:
    print(e)
    driver.save_screenshot(key + '.png')



