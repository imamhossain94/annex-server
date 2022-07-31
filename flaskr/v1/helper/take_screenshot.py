import asyncio
from pyppeteer import launch
from flaskr.v1.constants import *
import time


# https://stackoverflow.com/questions/61806240/pyppeteer-browser-closed-unexpectedly-in-heroku


async def take_screenshot(file_name, url, phpsessid):
    args = ['-window-size=1920,1080']
    browser = await launch(handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False, args=args)
    page = await browser.newPage()
    await page.goto(baseUrl)
    cookies = await page.cookies()
    cookies[0]['value'] = phpsessid
    await page.setCookie(cookies[0])
    await page.goto(url)
    time.sleep(3)
    await page.screenshot({
        'path': routineDirPath % file_name,
        'quality': 100,
        'fullPage': True
    })
    await browser.close()
