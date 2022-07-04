from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from flaskr.v1.constants import *
import logging
import os
import time

videos_folder = r"./download"
# Set default download folder for ChromeDriver
if not os.path.exists(videos_folder):
    os.makedirs(videos_folder)
prefs = {"download.default_directory": videos_folder}


def open_url(file_name, address, phpsessid):
    # SELENIUM SETUP
    logging.getLogger('WDM').setLevel(logging.WARNING)  # just to hide not so rilevant webdriver-manager messages
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.implicitly_wait(1)
    driver.maximize_window()
    driver.get(address)
    # cookies = driver.get_cookie(name='PHPSESSID')
    # cookies['value'] = phpsessid
    # print(cookies)
    driver.add_cookie(cookie_dict={
        'domain': 'annex.bubt.edu.bd',
        'httpOnly': False,
        'name': 'PHPSESSID',
        'path': '/',
        'secure': True,
        'value': phpsessid
    })
    driver.get(address)
    driver.set_window_size(1920, 1080)  # to set the screenshot width
    # save_screenshot(driver, screenshotDirPath + file_name + '.png')
    save_screenshot(driver, '{}/Screenshot.png'.format(videos_folder))
    driver.quit()


def save_screenshot(driver, file_name):
    height, width = scroll_down(driver)
    driver.set_window_size(width, height)
    img_binary = driver.get_screenshot_as_png()
    img = Image.open(BytesIO(img_binary))
    img.save(file_name)
    # print(file_name)
    print("Screenshot saved!")


def scroll_down(driver):
    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")

    rectangles = []

    i = 0
    while i < total_height:
        ii = 0
        top_height = i + viewport_height

        if top_height > total_height:
            top_height = total_height

        while ii < total_width:
            top_width = ii + viewport_width

            if top_width > total_width:
                top_width = total_width

            rectangles.append((ii, i, top_width, top_height))

            ii = ii + viewport_width

        i = i + viewport_height

    previous = None
    part = 0

    for rectangle in rectangles:
        if not previous is None:
            driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
            time.sleep(0.5)
        # time.sleep(0.2)

        if rectangle[1] + viewport_height > total_height:
            offset = (rectangle[0], total_height - viewport_height)
        else:
            offset = (rectangle[0], rectangle[1])

        previous = rectangle

    return total_height, total_width


open_url(
    file_name="xyz-pqr",
    address="https://annex.bubt.edu.bd/ONSIS_SEITO/?page=routine",
    phpsessid="9fe2648172acdf697ae5e78cbb12c493"
)
