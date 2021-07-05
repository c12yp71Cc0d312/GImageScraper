import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pynput.keyboard import Key, Controller
import pyperclip
import urllib.request
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"

keyboard = Controller()
key = 'o'

def scrapeimages(searchquery, noOfImages, delay):
    driver = webdriver.Chrome(PATH)
    driver.get("https:images.google.com")
    search = driver.find_element_by_name('q')
    search.clear()
    search.send_keys(searchquery)
    search.send_keys(Keys.RETURN)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mJxzWe"))
        )

        time.sleep(1)        #waiting to fully load page

        nDownloaded = 1
        for i in range(1, int(noOfImages) + 1):
            try:
                thumbnail = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="islrg"]/div[1]/div[' + str(i) + ']/a[1]/div[1]/img'))
                )
                thumbnail.click()
            except:
                bodyEle = driver.find_element_by_tag_name('body')
                bodyEle.send_keys(Keys.PAGE_UP)
                time.sleep(1)
                thumbnail = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="islrg"]/div[1]/div[' + str(i) + ']/a[1]/div[1]/img'))
                )
                thumbnail.click()

            try:
                imgContainer = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]'))
                )
                if loadDelay is not None:
                    time.sleep(float(delay))  # time to fully load image
                rClick = ActionChains(driver)
                rClick.context_click(imgContainer)
                rClick.perform()
                keyboard.press(key)
                keyboard.release(key)
                driver.back()
                try:
                    urllib.request.urlretrieve(pyperclip.paste(), downloadDir + '\\' + searchQuery + str(nDownloaded) + '.jpg')
                    print('Downloaded ' + str(nDownloaded) + '/' + noOfImages)
                    nDownloaded += 1
                except:
                    print('urlretrieve request blocked')
            except:
                print('error - possibly, image took more than 10 seconds to load')

    except:
        print('ERROR - took more than 10 seconds to load')


if __name__ == '__main__':
    searchQuery = input('Enter search term: ')
    downloadDir = os.path.dirname(os.path.abspath(__file__)) + '\\' + searchQuery
    os.mkdir(downloadDir)
    n = input('Enter no of images: ')
    loadDelay = input('Enter image load delay (in secs): ')
    try:
        loadDelay = float(loadDelay)
        if(loadDelay < 0):
            print('using min delay')
            loadDelay = None
    except:
        print('using min delay')
        loadDelay = None
    print('')
    scrapeimages(searchQuery, n, loadDelay)
    print('')
    print('Task Completed')
