import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import requests
import re
import pandas as pd
from collections import defaultdict
from fake_useragent import UserAgent


def setup():
    USERNAME = "xxxxxxxxxxxxx"
    PASSWORD = "xxxxxxxxxxxxxxxxx"

    # Headless/incognito Chrome driver
    firefox_options = webdriver.FirefoxOptions()
    # firefox_options.add_argument("--incognito")
    firefox_options.add_argument("user-agent=" + UserAgent().random)
    # firefox_options.add_argument("headless")
    driver = webdriver.Firefox(
        executable_path="geckodriver.exe",
        options=firefox_options,
    )

    driver.get("https://www.instagram.com/")

    # login
    time.sleep(5)
    username = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
    password = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
    username.clear()
    password.clear()
    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)
    login = driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # save your login info?
    time.sleep(5)
    not_now = driver.find_elements(By.XPATH, "//button[contains(text(), 'Not Now')]")
    if not_now:
        not_now[0].click()
    return driver


# search profile
def search_profile(driver, username):
    result = {
        "username": username,
        "full_name": "",
        "post_count": "",
        "followers_count": "",
        "following_count": "",
        "bio": "",
        "date_joined": "",
        "account_based_in": "",
        "website": "",
    }
    # searchbox
    time.sleep(2)
    searchbox = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search']")
    searchbox.clear()
    searchbox.send_keys(username)
    time.sleep(2)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(2)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(5)

    # scrape followers,following and post count, bio
    count_div = driver.find_element(
        By.CSS_SELECTOR,
        ".xieb3on",
    ).text.split("\n")

    post_count, followers_count, following_count = [x.split(" ")[0] for x in count_div]
    result["followers_count"] = followers_count
    result["following_count"] = following_count
    result["post_count"] = post_count

    # get the bio,website and fullname if available
    full_bio_web = driver.find_element(
        By.CSS_SELECTOR,
        "._aa_c",
    )

    # check for website
    website = full_bio_web.find_elements(
        By.CSS_SELECTOR,
        "._aacz",
    )
    if website:
        result["website"] = website[0].text

    # check for bio
    bio = full_bio_web.find_elements(
        By.CSS_SELECTOR,
        "._aacu",
    )
    if bio:
        result["bio"] = bio[0].text

    # get full name
    full_name = full_bio_web.find_element(
        By.CSS_SELECTOR,
        "._aad7",
    ).text
    result["full_name"] = full_name

    is_verified = driver.find_elements(By.CSS_SELECTOR, "._9ys7")
    if is_verified:
        result["is_verified"] = True
    else:
        result["is_verified"] = False

    # find account_based_in  and joined date
    driver.find_element(By.CSS_SELECTOR, "h2._aacx").click()
    time.sleep(3)
    account_based_in = driver.find_element(
        By.XPATH, "//div[@data-testid='ata_country_row']"
    ).text
    date_joined = driver.find_element(
        By.XPATH, "//div[@data-testid='ata_date_joined_row']"
    ).text
    result["account_based_in"] = account_based_in.split("\n")[1]
    result["date_joined"] = date_joined.split("\n")[1]
    return result

    # # scroll
    # scrolldown = driver.execute_script(
    #     "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;"
    # )
    # match = False
    # while match == False:
    #     last_count = scrolldown
    #     time.sleep(3)
    #     scrolldown = driver.execute_script(
    #         "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;"
    #     )
    #     if last_count == scrolldown:
    #         match = True


def main():
    driver = setup()
    time.sleep(3)
    data = search_profile(driver, "cristiano")
    print(data)


if __name__ == "__main__":
    main()
