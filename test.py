from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import requests
import re
import pandas as pd
from collections import defaultdict


# Headless/incognito Chrome driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
# chrome_options.add_argument("headless")
driver = webdriver.Chrome(
    executable_path="chromedriver.exe",
    chrome_options=chrome_options,
)

driver.get("https://www.instagram.com/")

# login
sleep(5)
username = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
password = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
username.clear()
password.clear()
username.send_keys("xxxxxx")
password.send_keys("123456")
login = driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
sleep(5)
