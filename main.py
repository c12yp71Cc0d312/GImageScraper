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
key2 = Key.right

def scrapeimages(searchquery, noOfImages, delay, alreadyDownloaded):
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

        nErrors = 0
        i = 1       #index to iterate through images on page
        nDownloaded = alreadyDownloaded

        openImage = False

        while nDownloaded < (int(noOfImages) + alreadyDownloaded):

            if not openImage:
                try:
                    thumbnail = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img'))
                    )
                    thumbnail.click()

                except:
                    thumbnail = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="islrg"]/div[1]/div[2]/a[1]/div[1]/img'))
                    )
                    thumbnail.click()
                openImage = True

            else:
                keyboard.press(key2)
                keyboard.release(key2)

            pyperclip.copy('')

            try:
                imgContainer = WebDriverWait(driver, 5).until(
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

                while not pyperclip.paste():
                    time.sleep(0.1)

                try:
                    urllib.request.urlretrieve(pyperclip.paste(), downloadDir + '\\' + searchQuery + str(nDownloaded+1) + '.jpg')
                    nDownloaded += 1
                    print('Downloaded ' + str(nDownloaded - alreadyDownloaded) + '/' + noOfImages + '  (' + str(nErrors) + ' failed)')

                except:
                    print('urlretrieve request blocked - ' + pyperclip.paste())
                    nErrors += 1

            except:
                print('error - possibly, image container took more than 5 seconds to load')

            i += 1

    except:
        print('ERROR - took more than 10 seconds to load')


if __name__ == '__main__':
    searchQuery = input('Enter search term: ')
    downloadDir = os.path.dirname(os.path.abspath(__file__)) + '\\' + searchQuery

    if not os.path.isdir(downloadDir):
        os.mkdir(downloadDir)
        alreadyDownloaded = 0

    else:
        alreadyDownloaded = len(os.listdir(downloadDir))

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
    scrapeimages(searchQuery, n, loadDelay, alreadyDownloaded)
    print('')
    print('Task Completed')
